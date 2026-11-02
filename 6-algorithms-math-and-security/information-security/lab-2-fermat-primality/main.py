import random

# Перевірка на простоту за допомогою малої теореми Ферма
def is_fermat_prime(n, k=5):
    if n < 2:
        print(f"Число {n} менше 2 не може бути простим.")
        return False

    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            print(f"Число {n} НЕ ПРОСТЕ (не пройшло тест для основи {a})")
            return False

    return True  # Повертаємо тільки True

# Перевірка на простоту за допомогою тесту Рабіна
def is_rabin_prime(n, k=5):
    if n < 2:
        print(f"Число {n} менше 2 не може бути простим.")
        return False

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, (n - 1) // 2, n)
        if x != 1 and x != n - 1:
            print(f"Число {n} НЕ ПРОСТЕ (не пройшло тест для основи {a})")
            return False

    return True  # Повертаємо тільки True

# Генерація випадкових великих чисел (від 45 до 55 розрядів)
def generate_large_numbers(count):
    numbers = []
    for _ in range(count):
        num_digits = random.randint(45, 55)  # Випадкова кількість розрядів від 45 до 55
        candidate = random.randint(10 ** (num_digits - 1), 10 ** num_digits - 1)
        numbers.append(candidate)
    return numbers

# Перевірка числа обома тестами
def check_prime(candidate):
    if not is_fermat_prime(candidate):
        return False  # Пояснення вже виведено через print

    if not is_rabin_prime(candidate):
        return False  # Пояснення вже виведено через print

    return True  # Повертаємо тільки True

# Основна логіка
def find_primes():
    while True:
        numbers_to_test = generate_large_numbers(10)  # Генерація 10 чисел
        print("\nЗгенеровані числа:")
        for number in numbers_to_test:
            print(f"Число: {number}")

        # Додаємо порожній рядок для відступу перед аналізом
        print("\nАналіз чисел на простоту:\n")

        prime_found = False
        for number in numbers_to_test:
            if check_prime(number):
                print(f"Число {number} є ПРОСТЕ (пройшло тести Ферма та Рабіна).")
                prime_found = True
            else:
                pass  # Тут не потрібен вивід, оскільки це вже обробляється в is_fermat_prime та is_rabin_prime

        if prime_found:
            break
        else:
            print("\nСеред згенерованих чисел немає простих. Генерація нових чисел...\n")

# Запуск основної програми
find_primes()
