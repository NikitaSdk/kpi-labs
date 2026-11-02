import os
import shutil
import hashlib
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 1. Підготовка папок
# ============================================================

PROJECT_DIR = "content_addressing_demo"
FILES_DIR = os.path.join(PROJECT_DIR, "files")
RESULTS_DIR = os.path.join(PROJECT_DIR, "results")

if os.path.exists(PROJECT_DIR):
    shutil.rmtree(PROJECT_DIR)

os.makedirs(FILES_DIR)
os.makedirs(RESULTS_DIR)


# ============================================================
# 2. Створення тестових файлів
# ============================================================

files = {
    "file1.txt": "Це тестовий файл для демонстрації адресації за вмістом.",
    "file2.txt": "Це інший файл, який має інший вміст.",
    "file3_copy.txt": "Це тестовий файл для демонстрації адресації за вмістом.",
    "file4.txt": "Це файл для перевірки роботи хешування."
}

for filename, text in files.items():
    path = os.path.join(FILES_DIR, filename)

    with open(path, "w", encoding="utf-8") as file:
        file.write(text)

print("1. Тестові файли створено.")


# ============================================================
# 3. Функція для обчислення SHA 256 хешу
# ============================================================

def sha256_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ============================================================
# 4. Класичний підхід: файл визначається за шляхом
# ============================================================

location_rows = []

for filename in sorted(os.listdir(FILES_DIR)):
    path = os.path.join(FILES_DIR, filename)
    size = os.path.getsize(path)

    location_rows.append({
        "Назва файлу": filename,
        "Шлях до файлу": path,
        "Розмір, байт": size
    })

df_location = pd.DataFrame(location_rows)

print("\n2. Класичний підхід: адресація за місцем зберігання")
print(df_location)

df_location.to_csv(
    os.path.join(RESULTS_DIR, "01_location_addressing.csv"),
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# 5. Адресація за вмістом: файл визначається за хешем
# ============================================================

content_storage = {}
content_rows = []

for filename in sorted(os.listdir(FILES_DIR)):
    path = os.path.join(FILES_DIR, filename)

    with open(path, "rb") as file:
        data = file.read()

    file_hash = sha256_hash(data)

    if file_hash not in content_storage:
        content_storage[file_hash] = data
        status = "Новий вміст"
    else:
        status = "Дублікат вмісту"

    content_rows.append({
        "Назва файлу": filename,
        "SHA 256 хеш": file_hash,
        "Статус": status,
        "Розмір, байт": len(data)
    })

df_content = pd.DataFrame(content_rows)

print("\n3. Адресація за вмістом")
print(df_content)

df_content.to_csv(
    os.path.join(RESULTS_DIR, "02_content_addressing.csv"),
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# 6. Пошук файлу за хешем
# ============================================================

requested_hash = list(content_storage.keys())[0]
found_data = content_storage[requested_hash]

print("\n4. Пошук файлу за SHA 256 хешем")
print("Запитаний хеш:")
print(requested_hash)
print("Знайдений вміст:")
print(found_data.decode("utf-8"))


# ============================================================
# 7. Розрахунок економії пам'яті
# ============================================================

original_size = sum(
    os.path.getsize(os.path.join(FILES_DIR, filename))
    for filename in os.listdir(FILES_DIR)
)

unique_content_size = sum(
    len(data)
    for data in content_storage.values()
)

saved_space = original_size - unique_content_size
saved_percent = saved_space / original_size * 100

summary = pd.DataFrame({
    "Показник": [
        "Початковий обсяг усіх файлів, байт",
        "Обсяг унікального вмісту, байт",
        "Зекономлено пам'яті, байт",
        "Економія пам'яті, %"
    ],
    "Значення": [
        original_size,
        unique_content_size,
        saved_space,
        round(saved_percent, 2)
    ]
})

print("\n5. Розрахунок економії пам'яті")
print(summary)

summary.to_csv(
    os.path.join(RESULTS_DIR, "03_storage_summary.csv"),
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# 8. Перевірка цілісності даних
# ============================================================

original_text = "Content addressing instead of IP"
changed_text = "Content addressing instead of ip"

original_hash = sha256_hash(original_text.encode("utf-8"))
changed_hash = sha256_hash(changed_text.encode("utf-8"))

integrity = pd.DataFrame({
    "Стан даних": [
        "Початкові дані",
        "Дані після зміни одного символу"
    ],
    "Текст": [
        original_text,
        changed_text
    ],
    "SHA 256 хеш": [
        original_hash,
        changed_hash
    ]
})

print("\n6. Перевірка цілісності даних")
print(integrity)

integrity.to_csv(
    os.path.join(RESULTS_DIR, "04_integrity_check.csv"),
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# 9. Побудова графіка
# ============================================================

total_files = len(df_content)
unique_files = len(content_storage)
duplicate_files = total_files - unique_files

plt.figure(figsize=(7, 5))
plt.bar(
    ["Усі файли", "Унікальний вміст", "Дублікати"],
    [total_files, unique_files, duplicate_files]
)

plt.title("Порівняння файлів за шляхом і за вмістом")
plt.xlabel("Показник")
plt.ylabel("Кількість")
plt.grid(axis="y")
plt.tight_layout()

chart_path = os.path.join(RESULTS_DIR, "chart_content_addressing.png")
plt.savefig(chart_path)
plt.show()


# ============================================================
# 10. Фінальний підсумок
# ============================================================

print("\nФінальний підсумок:")
print(f"Загальна кількість файлів: {total_files}")
print(f"Кількість унікальних об'єктів за вмістом: {unique_files}")
print(f"Кількість дублікатів: {duplicate_files}")
print(f"Початковий обсяг: {original_size} байт")
print(f"Обсяг після дедуплікації: {unique_content_size} байт")
print(f"Економія пам'яті: {saved_space} байт")
print(f"Економія пам'яті у відсотках: {round(saved_percent, 2)}%")
print(f"Результати збережено у папці: {RESULTS_DIR}")