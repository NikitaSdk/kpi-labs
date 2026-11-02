from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import os

def show_file(file_path, action):
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            if len(content) <= 50:
                print(f"\nВміст файлу {file_path} {action}:")
                print(content)
            else:
                print(f"\nФайл {file_path} {action},великий розмір фацлу.")
    except Exception as e:
        print(f"Не вдалося прочитати файл {file_path}: {e}")

def encrypt_des(key, input_file, output_file):
    try:
        cipher = DES.new(key, DES.MODE_ECB)
        with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
            plaintext = f_in.read()
            show_file(input_file, "до шифрування")
            ciphertext = cipher.encrypt(pad(plaintext, DES.block_size))
            f_out.write(ciphertext)
        print(f"Файл '{input_file}' зашифровано у '{output_file}'.")
    except FileNotFoundError:
        print(f"Файл для шифрування '{input_file}' не знайдено.")
    except Exception as e:
        print(f"Помилка під час шифрування: {e}")

def decrypt_des(key, input_file, output_file):
    try:
        cipher = DES.new(key, DES.MODE_ECB)
        with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
            ciphertext = f_in.read()
            plaintext = unpad(cipher.decrypt(ciphertext), DES.block_size)
            f_out.write(plaintext)
        print(f"Файл '{input_file}' розшифровано у '{output_file}'.")
        show_file(output_file, "після розшифрування")
    except FileNotFoundError:
        print(f"Файл для розшифрування '{input_file}' не знайдено.")
    except ValueError:
        print("Помилка при розшифруванні: некоректний формат або ключ.")
    except Exception as e:
        print(f"Невідома помилка під час розшифрування: {e}")

def create_signature(key, input_file):
    try:
        cipher = DES.new(key, DES.MODE_CBC, iv=b'\x00\x00\x00\x00\x00\x00\x00\x00')
        with open(input_file, 'rb') as f_in:
            plaintext = f_in.read()
            padded_plaintext = pad(plaintext, DES.block_size)
            ciphertext = cipher.encrypt(padded_plaintext)
        print(f"Цифровий підпис створено для файлу '{input_file}'.")
        return ciphertext[-DES.block_size:]
    except FileNotFoundError:
        print(f"Файл '{input_file}' не знайдено.")
    except Exception as e:
        print(f"Помилка при створенні цифрового підпису: {e}")
        return None

def save_signature(signature, output_file):
    try:
        with open(output_file, 'wb') as f:
            f.write(signature)
        print(f"Цифровий підпис збережено у файлі {output_file}.")
    except Exception as e:
        print(f"Помилка при збереженні цифрового підпису: {e}")

def load_signature(input_file):
    if os.path.exists(input_file):
        try:
            with open(input_file, 'rb') as f:
                signature = f.read()
            print(f"Цифровий підпис зчитано з файлу {input_file}.")
            return signature
        except Exception as e:
            print(f"Помилка при зчитуванні цифрового підпису: {e}")
            return None
    else:
        print(f"Файл із цифровим підписом {input_file} не знайдено.")
        return None

def verify_signature(key, input_file, provided_signature):
    try:
        cipher = DES.new(key, DES.MODE_CBC, iv=b'\x00\x00\x00\x00\x00\x00\x00\x00')
        with open(input_file, 'rb') as f_in:
            plaintext = f_in.read()
            padded_plaintext = pad(plaintext, DES.block_size)
            ciphertext = cipher.encrypt(padded_plaintext)
            calculated_signature = ciphertext[-DES.block_size:]
        if calculated_signature == provided_signature:
            print("Цифровий підпис підтверджено.")
        else:
            print("Цифровий підпис недійсний.")
    except FileNotFoundError:
        print(f"Файл '{input_file}' не знайдено.")
    except Exception as e:
        print(f"Помилка при перевірці підпису: {e}")

def main():
    while True:
        print("1 - Шифрування")
        print("2 - Розшифрування")
        print("3 - Цифровий підпис")
        print("4 - Перевірка підпису")
        print("5 - Завершення роботи")

        choice = input("Що будемо робити: ").strip()
        if choice == "5":
            print("Завершеня роботи")
            break

        key = input("Введіть ключ шифрування (8 символів): ").encode()
        if len(key) != 8:
            print("Ключ має бути рівно 8 байтів! Спробуйте знову.")
            continue

        if choice == "1":
            print("Шифрування")
            input_file = input("Введіть ім'я файлу для шифрування: ").strip()
            output_file = input("Введіть ім'я файлу для збереження зашифрованих даних: ").strip()
            encrypt_des(key, input_file, output_file)

        elif choice == "2":
            print("Розшифрування")
            input_file = input("Введіть ім'я файлу для розшифрування: ").strip()
            output_file = input("Введіть ім'я файлу для збереження розшифрованих даних: ").strip()
            decrypt_des(key, input_file, output_file)

        elif choice == "3":
            print("Цифровий підпис")
            input_file = input("Введіть ім'я файлу для створення цифрового підпису: ").strip()
            signature = create_signature(key, input_file)
            if signature:
                signature_file = input("Введіть ім'я файлу для збереження цифрового підпису: ").strip()
                save_signature(signature, signature_file)

        elif choice == "4":
            print("Перевірка підпису ")
            input_file = input("Введіть ім'я файлу для перевірки цифрового підпису: ").strip()
            signature_file = input("Введіть ім'я файлу з цифровим підписом: ").strip()
            signature = load_signature(signature_file)
            if signature:
                verify_signature(key, input_file, signature)
        else:
            print("Введіть число від 1 до 5.")

if __name__ == "__main__":
    main()
