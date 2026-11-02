import random
from math import gcd

def RabinMillerTest(n, k=5):
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    s, d = 0, n - 1
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


def Generate_num(bits):
    while True:
        my_number = random.getrandbits(bits) | (1 << bits - 1) | 1
        if RabinMillerTest(my_number):
            return my_number


def EuclideanAlgorithmExtend(a, b):
    if a == 0:
        return b, 0, 1
    gcd_value, x1, y1 = EuclideanAlgorithmExtend(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_value, x, y


def MultiplicateInv(e, phi):
    gcd_value, x, _ = EuclideanAlgorithmExtend(e, phi)
    if gcd_value != 1:
        raise Exception('Мультиплікативний обернений не існує.')
    return x % phi


def Gen_Keys(key_size):
    p = Generate_num(key_size // 2)
    q = Generate_num(key_size // 2)
    while p == q:
        q = Generate_num(key_size // 2)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    if gcd(e, phi) != 1:
        e = random.randrange(3, phi, 2)
        while gcd(e, phi) != 1:
            e = random.randrange(3, phi, 2)

    d = MultiplicateInv(e, phi)

    return (e, n), (d, n), p, q


def Encryption(public_key, data):
    e, n = public_key
    block_size = (n.bit_length() - 1) // 8
    encrypted_data = []
    for i in range(0, len(data), block_size):
        block = int.from_bytes(data[i:i + block_size], byteorder='big')
        encrypted_block = pow(block, e, n)
        encrypted_data.append(encrypted_block)
    return encrypted_data


def Decryption(private_key, encrypted_data):
    d, n = private_key
    decrypted_data = bytearray()
    for block in encrypted_data:
        decrypted_block = pow(block, d, n)
        decrypted_data.extend(decrypted_block.to_bytes((decrypted_block.bit_length() + 7) // 8, byteorder='big'))
    return decrypted_data


def save_encrypted(filename, encrypted_data):
    with open(filename, 'w') as f:
        for item in encrypted_data:
            f.write(f"{item}\n")


def load_encrypted(filename):
    with open(filename, 'r') as f:
        return [int(line.strip()) for line in f]


def Encrypt_File(input_filename, output_filename, public_key):
    with open(input_filename, 'rb') as f:
        file_data = f.read()

    encrypted_data = Encryption(public_key, file_data)
    save_encrypted(output_filename, encrypted_data)

    return input_filename, output_filename



def Decrypt_File(input_filename, output_filename, private_key):
    encrypted_data = load_encrypted(input_filename)
    decrypted_data = Decryption(private_key, encrypted_data)

    with open(output_filename, 'wb') as f:
        f.write(decrypted_data)

    return input_filename, output_filename


def main():
    key_size = int(input("Введіть довжину ключа (має ділитися на 64, рекомендована 1024): "))
    if key_size < 64 or key_size > 2048 or key_size % 64 != 0:
        print("Довжина ключа має бути від 64 до 2048 біт і ділитися на 64.")
        return

    public_key, private_key, p, q = Gen_Keys(key_size)

    print("\nКомпоненти відкритого ключа:")
    print(f"n (модуль): {public_key[1]}")
    print(f"e (експонента): {public_key[0]}")

    print("\nКомпоненти закритого ключа:")
    print(f"n (модуль): {private_key[1]}")
    print(f"d (закрита експонента): {private_key[0]}")
    print(f"p (перше просте число): {p}")
    print(f"q (друге просте число): {q}")

    input_filename = input("\nВведіть ім'я файлу для шифрування: ")
    encrypted_filename = input("Введіть ім'я файлу для запису зашифрованої інформації: ")
    input_file, encrypted_file = Encrypt_File(input_filename, encrypted_filename, public_key)
    print(f"\nФайл '{input_file}' успішно зашифровано у файл '{encrypted_file}'.")

    decrypted_filename = input("\nВведіть ім'я файлу для розшифрування інформації: ")
    encrypted_file, decrypted_file = Decrypt_File(encrypted_filename, decrypted_filename, private_key)
    print(f"\nФайл '{encrypted_file}' успішно розшифровано у файл '{decrypted_file}'.")


if __name__ == "__main__":
    main()
