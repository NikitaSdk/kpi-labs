# Code extracted from the lab report (report.pdf)

from pprint import pprint

from redis.cluster import ClusterNode, RedisCluster

STARTUP_NODES = [
    ClusterNode(host="127.0.0.1", port=7000),
]

def main() -> None:
    rc = RedisCluster(
        startup_nodes=STARTUP_NODES,
        decode_responses=True,
    )

    # 1) Hash–Slot map: те саме, що redis-cli CLUSTER SLOTS
    slots_raw = rc.execute_command("CLUSTER SLOTS")

    print("=== CLUSTER SLOTS (Hash–Slot Map) ===")
    pprint(slots_raw)
    print()

    # 2) Запис і читання ключів (різні слоти → різні шарди; клієнт ходить сам)
    keys_values = [
        ("foo", "alice"),
        ("name", "bob"),
        ("project", "lab2-bd"),
    ]
    print("=== SET / GET (KEYSLOT + значення) ===")
    for key, val in keys_values:
        rc.set(key, val)
        slot = rc.cluster_keyslot(key)
        print(f"{key!r}: KEYSLOT -> {slot}")

    print()
    for key, _ in keys_values:
        print(f"GET {key!r} -> {rc.get(key)}")

    rc.close()

if __name__ == "__main__":
    main()
