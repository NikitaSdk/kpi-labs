import random

def is_fermat_prime(n, k=5):

    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False

    return True

def is_rabin_miller_prime(n, k=5):

    if n % 2 == 0:
        return False

    s = 0
    d = n - 1

    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True

def generate_large_numbers(count):
    numbers = []
    for _ in range(count):
        num_digits = random.randint(45, 55)
        candidate = random.randint(10 ** (num_digits - 1), 10 ** num_digits - 1)
        numbers.append(candidate)
    return numbers

def check_prime(candidate):
    fermat_result = is_fermat_prime(candidate)
    rabin_miller_result = is_rabin_miller_prime(candidate)

    if fermat_result and rabin_miller_result:
        return "Є простим"
    else:
        return "Не є простим"

def find_primes():
    while True:
        numbers_to_test = generate_large_numbers(10)
        print("\nЗгенеровані числа:")
        for number in numbers_to_test:
            print(f"Число: {number}")

        print("\nАналіз чисел на простоту:\n")

        prime_found = False
        for number in numbers_to_test:
            result = check_prime(number)
            print(f"Число {number} {result}")
            if result == "Є простим":
                prime_found = True

        if prime_found:
            break
        else:
            print("\nСеред згенерованих чисел немає простих. Генерація нових чисел...\n")

find_primes()
