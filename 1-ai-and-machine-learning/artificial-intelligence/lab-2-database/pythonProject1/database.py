import sqlite3
import os

DB_NAME = "career_guidance.db"

# Підключення до бази даних
def connect():
    return sqlite3.connect(DB_NAME)

# Створення таблиць у базі даних
def create_tables():
    conn = connect()
    cursor = conn.cursor()

    # Таблиця предметів
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)

    # Таблиця професій
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS professions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)

    # Таблиця зв'язків між професіями та предметами
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profession_subjects (
        profession_id INTEGER,
        subject_id INTEGER,
        certificate TEXT,
        hobby TEXT,
        self_learning TEXT,
        additional_section TEXT,
        FOREIGN KEY (profession_id) REFERENCES professions(id),
        FOREIGN KEY (subject_id) REFERENCES subjects(id)
    )
    """)

    # Таблиця сертифікатів
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS certificates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)

    # Таблиця хобі
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hobbies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)

    # Таблиця схильності до самонавчання
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS self_learning (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        option TEXT NOT NULL UNIQUE
    )
    """)

    # Таблиця додаткових секцій
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS additional_sections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)

    conn.commit()
    conn.close()

# Видалення старої бази даних
def delete_database():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print("Стара база даних видалена.")

# Заповнення таблиці з предметами
def populate_subjects():
    subjects = [
        "Математика", "Інформатика", "Англійська мова", "Біологія", "Хімія",
        "Фізика", "Історія", "Географія", "Література", "Економіка",
        "Музика", "Мистецтво", "Правознавство", "Філософія", "Соціологія",
        "Фізична культура", "Технології", "Статистика", "Астрономія", "Екологія",
        "Психологія", "Фінанси", "Маркетинг", "Медицина", "Кулінарія"
    ]

    conn = connect()
    cursor = conn.cursor()
    cursor.executemany("INSERT OR IGNORE INTO subjects (name) VALUES (?)", [(s,) for s in subjects])
    conn.commit()
    conn.close()

# Заповнення таблиці з сертифікатами
def populate_certificates():
    certificates = [
        "Конкурс з математики", "Конкурс з інформатики", "Конкурс з англійської мови",
        "Конкурс з біології", "Конкурс з хімії", "Конкурс з фізики",
        "Конкурс з історії", "Конкурс з музики", "Конкурс з мистецтва",
        "Конкурс з економіки", "Конкурс з правознавства", "Конкурс з театрального мистецтва",
        "Конкурс з кулінарії", "Конкурс з логістики", "Конкурс з геології",
        "Конкурс з медицини", "Конкурс з психології", "Конкурс з соціології",
        "Конкурс з науки", "Конкурс з техніки"
    ]

    conn = connect()
    cursor = conn.cursor()
    cursor.executemany("INSERT OR IGNORE INTO certificates (name) VALUES (?)", [(c,) for c in certificates])
    conn.commit()
    conn.close()

# Заповнення таблиці з хобі
def populate_hobbies():
    hobbies = [
        "Математика", "Програмування", "Музика", "Спорт", "Малювання",
        "Читання", "Фотографія", "Подорожі", "Кулінарія", "Астрономія",
        "Екологія", "Література", "Наука", "Театр", "Технології",
        "Медицина", "Організація", "Навчання"
    ]

    conn = connect()
    cursor = conn.cursor()
    cursor.executemany("INSERT OR IGNORE INTO hobbies (name) VALUES (?)", [(h,) for h in hobbies])
    conn.commit()
    conn.close()

# Заповнення таблиці схильності до самонавчання
def populate_self_learning():
    options = ["Так", "Ні"]

    conn = connect()
    cursor = conn.cursor()
    cursor.executemany("INSERT OR IGNORE INTO self_learning (option) VALUES (?)", [(o,) for o in options])
    conn.commit()
    conn.close()

# Заповнення таблиці з додатковими секціями
def populate_additional_sections():
    sections = [
        "Математика", "Інформатика", "Англійська мова", "Біологія", "Хімія",
        "Фізика", "Історія", "Географія", "Література", "Музика",
        "Мистецтво", "Економіка", "Соціологія", "Філософія", "Технології",
        "Кулінарія", "Спорт", "Медицина", "Маркетинг", "Астрономія"
    ]

    conn = connect()
    cursor = conn.cursor()
    cursor.executemany("INSERT OR IGNORE INTO additional_sections (name) VALUES (?)", [(s,) for s in sections])
    conn.commit()
    conn.close()

# Заповнення таблиці з професіями
def populate_professions():
    professions = [
        "Вчитель математики","Вчитель англійської", "Програміст", "Хімік", "Фізик", "Лікар",
        "Інженер", "Юрист", "Музикант", "Астроном", "Журналіст",
        "Дизайнер", "Фінансовий аналітик", "Маркетолог", "SEO-спеціаліст",
        "Агроном", "Біолог", "Соціальний працівник", "Психолог", "Архітектор",
        "Фотограф", "Кулінар", "Спортсмен", "Еколог", "Історик","Вчений"
        "Викладач", "Тренер", "Менеджер з продажу", "Секретар", "Логіст", "Актор", "Пілот", "Хірург",
        "Фармацевт", "Геолог", "Електрик", "Механік", "Водій", "Садівник", "Редактор", "Бариста",
        "Фізіотерапевт", "Модератор", "Бухгалтер", "Нотаріус", "Філолог", "Вчений", "Викладач", "Математик",
        "Менеджер проєктів"
    ]

    conn = connect()
    cursor = conn.cursor()
    cursor.executemany("INSERT OR IGNORE INTO professions (name) VALUES (?)", [(p,) for p in professions])
    conn.commit()
    conn.close()

# Заповнення таблиці зв'язків між професіями т а критеріями
def populate_profession_subjects():
    conn = connect()
    cursor = conn.cursor()

    profession_subjects = {
        # 10 професій з 3 критеріями
        "Хімік": ["Хімія", "Конкурс з хімії", "Наука"],
        "Фізик": ["Фізика", "Конкурс з фізики", "Астрономія"],
        "Біолог": ["Біологія", "Конкурс з біології", "Екологія"],
        "Лікар": ["Медицина", "Конкурс з медицини", "Медицина"],
        "Програміст": ["Інформатика", "Конкурс з інформатики", "Програмування"],
        "Математик": ["Математика", "Конкурс з математики", "Статистика"],
        "Музикант": ["Музика", "Конкурс з музики", "Музика"],
        "Журналіст": ["Література", "Конкурс з літератури", "Читання"],
        "Дизайнер": ["Мистецтво", "Конкурс з мистецтва", "Малювання"],
        "Фінансовий аналітик": ["Економіка", "Конкурс з економіки", "Фінанси"],

        # 10 професій з 4 критеріями
        "Вчитель математики": ["Математика", "Конкурс з математики", "Математика", "Так"],
        "Вчитель англійської": ["Англійська мова", "Конкурс з англійської мови", "Читання", "Так"],
        "Хірург": ["Біологія", "Конкурс з медицини", "Медицина", "Так"],
        "Архітектор": ["Математика", "Конкурс з мистецтва", "Малювання", "Так"],
        "Астроном": ["Астрономія", "Конкурс з фізики", "Астрономія", "Так"],
        "Еколог": ["Екологія", "Конкурс з біології", "Екологія", "Так"],
        "Соціальний працівник": ["Соціологія", "Конкурс з соціології", "Соціальні науки", "Ні"],
        "Менеджер з продажу": ["Економіка", "Конкурс з економіки", "Маркетинг", "Так"],
        "Логіст": ["Економіка", "Конкурс з логістики", "Подорожі", "Так"],
        "Редактор": ["Література", "Конкурс з літератури", "Читання", "Так"],

        # 30 професій з 5 критеріями
        "Інженер": ["Фізика", "Конкурс з фізики", "Технології", "Так", "Технології"],
        "Маркетолог": ["Соціологія", "Конкурс з маркетингу", "Маркетинг", "Так", "Маркетинг"],
        "SEO-спеціаліст": ["Інформатика", "Конкурс з інформатики", "Програмування", "Так", "Інформатика"],
        "Фармацевт": ["Хімія", "Конкурс з хімії", "Медицина", "Так", "Хімія"],
        "Кулінар": ["Кулінарія", "Конкурс з кулінарії", "Кулінарія", "Так", "Кулінарія"],
        "Спортсмен": ["Фізична культура", "Конкурс з спорту", "Спорт", "Так", "Спорт"],
        "Актор": ["Мистецтво", "Конкурс з театрального мистецтва", "Музика", "Так", "Мистецтво"],
        "Фізіотерапевт": ["Біологія", "Конкурс з медицини", "Спорт", "Так", "Медицина"],
        "Пілот": ["Фізика", "Конкурс з фізики", "Подорожі", "Так", "Астрономія"],
        "Фотограф": ["Мистецтво", "Конкурс з мистецтва", "Фотографія", "Так", "Мистецтво"],
        "Менеджер проєктів": ["Економіка", "Конкурс з менеджменту", "Організація", "Так", "Економіка"],
        "Садівник": ["Біологія", "Конкурс з біології", "Екологія", "Ні", "Біологія"],
        "Геолог": ["Географія", "Конкурс з геології", "Подорожі", "Так", "Географія"],
        "Електрик": ["Фізика", "Конкурс з техніки", "Технології", "Так", "Фізика"],
        "Водій": ["Географія", "Конкурс з географії", "Подорожі", "Ні", "Географія"],
        "Механік": ["Фізика", "Конкурс з механіки", "Технології", "Так", "Технології"],
        "Бариста": ["Кулінарія", "Конкурс з кулінарії", "Кулінарія", "Ні", "Кулінарія"],
        "Модератор": ["Інформатика", "Конкурс з інформатики", "Організація", "Так", "Інформатика"],
        "Бухгалтер": ["Математика", "Конкурс з економіки", "Фінанси", "Так", "Економіка"],
        "Нотаріус": ["Правознавство", "Конкурс з правознавства", "Соціальні науки", "Так", "Правознавство"],
        "Філолог": ["Література", "Конкурс з літератури", "Читання", "Так", "Література"]

    }

    for profession, criteria in profession_subjects.items():
        cursor.execute("SELECT id FROM professions WHERE name = ?", (profession,))
        profession_row = cursor.fetchone()

        if profession_row is None:
            print(f"Помилка: Професія '{profession}' не знайдена в таблиці 'professions'. Пропускаємо.")
            continue

        profession_id = profession_row[0]

        subject = criteria[0]
        certificate = criteria[1] if len(criteria) > 1 else None
        hobby = criteria[2] if len(criteria) > 2 else None
        self_learning = criteria[3] if len(criteria) > 3 else None
        section = criteria[4] if len(criteria) > 4 else None

        cursor.execute("""
            INSERT OR IGNORE INTO profession_subjects (profession_id, subject_id, certificate, hobby, self_learning, additional_section)
            VALUES (?, (SELECT id FROM subjects WHERE name = ?), ?, ?, ?, ?)
        """, (profession_id, subject, certificate, hobby, self_learning, section))

    conn.commit()
    conn.close()

# Ініціалізація бази даних
def initialize_database():
    delete_database()
    create_tables()
    populate_subjects()
    populate_certificates()
    populate_hobbies()
    populate_self_learning()
    populate_additional_sections()
    populate_professions()
    populate_profession_subjects()
    print("База даних успішно створена.")

