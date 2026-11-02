# Code extracted from the lab report (report.pdf)

import os
import random
import string
import time
import subprocess
import redis

HOST = "127.0.0.1"
MASTER_PORT = 6379
REPLICA_PORT = 6380
REDIS_PASSWORD = "a_strong_password"

LAB_ROOT = os.path.expanduser("~/lab1redis")
MASTER_DIR = os.path.join(LAB_ROOT, "primary")
REPLICA_DIR = os.path.join(LAB_ROOT, "replica")
REPLICA_RDB_FILE = os.path.join(REPLICA_DIR, "my_backup_file.rdb")

def generate_random_text(length: int = 14) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))

def redis_client(port: int) -> redis.Redis:
    return redis.Redis(
        host=HOST,
        port=port,
        password=REDIS_PASSWORD,
        decode_responses=True
    )

def calculate_aof_size(directory: str) -> int:
    total_size = 0

    for root, _, files in os.walk(directory):
        for file_name in files:
            full_path = os.path.join(root, file_name)
            lower_name = file_name.lower()

            if lower_name.endswith(".aof") or "appendonly" in lower_name:
                if os.path.isfile(full_path):
                    total_size += os.path.getsize(full_path)

    return total_size

def calculate_rdb_size(file_path: str) -> int:
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return os.path.getsize(file_path)
    return 0

def wait_until_replica_becomes_master(timeout_seconds: int = 90) -> float | None:
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        try:
            replica = redis_client(REPLICA_PORT)
            replication_info = replica.info("replication")

            if replication_info.get("role") == "master":
                return time.time() - start_time
        except Exception:
            pass

        time.sleep(0.5)

    return None

def stop_old_master() -> None:
    subprocess.run(
        ["redis-cli", "-p", str(MASTER_PORT), "-a", REDIS_PASSWORD, "shutdown", "nosave"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False
    )

def perform_probabilistic_load() -> tuple[int, int]:
    master = redis_client(MASTER_PORT)

    existing_keys = []
    created_count = 0
    updated_count = 0

    for i in range(5):
        key_name = f"nikita_base:{i}"
        master.set(key_name, generate_random_text())
        existing_keys.append(key_name)

    start_time = time.time()

    while time.time() - start_time < 60:
        create_new = False

        if created_count < 20 and updated_count >= 5:
            create_new = True
        elif created_count < 20 and updated_count < 5:
            create_new = random.random() < 0.7

        if create_new:
            key_name = f"nikita_new:{created_count}"
            value = generate_random_text()
            master.set(key_name, value)
            created_count += 1
        elif updated_count < 5 and existing_keys:
            key_name = random.choice(existing_keys)
            value = generate_random_text()
            master.set(key_name, value)
            updated_count += 1

        if created_count >= 20 and updated_count >= 5:
            break

        time.sleep(random.uniform(1.2, 2.8))

    return created_count, updated_count

def main():
    print("=== ЛАБОРАТОРНА РОБОТА 1. REDIS HA ===")

    try:
        created, updated = perform_probabilistic_load()
    except Exception as error:
        print(f"Помилка під час запису в master: {error}")
        return

    print("\n--- РЕЗУЛЬТАТИ НАВАНТАЖЕННЯ ---")
    print(f"Нових ключів створено: {created}")
    print(f"Існуючих ключів оновлено: {updated}")

    print("\nОчікування 35 секунд, щоб replica встигла створити RDB...")
    time.sleep(35)

    aof_bytes = calculate_aof_size(MASTER_DIR)
    rdb_bytes = calculate_rdb_size(REPLICA_RDB_FILE)

    print("\n--- РОЗМІРИ ФАЙЛІВ ---")
    print(f"Сумарний розмір AOF-файлів: {aof_bytes} байт")
    print(f"Розмір RDB-файлу replica: {rdb_bytes} байт")

    print("\n--- ПЕРЕВІРКА FAILOVER ---")
    print("Вимикаємо старий master...")

    stop_old_master()

    failover_duration = wait_until_replica_becomes_master()

    if failover_duration is not None:
        print(f"Новим master став вузол на порту {REPLICA_PORT}")
        print(f"Тривалість failover: {failover_duration:.3f} с")
    else:
        print("Не вдалося зафіксувати failover протягом 90 секунд")

if __name__ == "__main__":
    main()
