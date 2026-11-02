import json
import os
import tkinter as tk
from tkinter import messagebox

class Model:
    def __init__(self, filename="database.json"):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):

        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        else:
            return {}

    def save_data(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def create_record(self, key, value):
        if key in self.data:
            return False, "Запис з таким ключем вже існує."
        self.data[key] = value
        self.save_data()
        return True, "Запис створено успішно."

    def read_records(self):
        return self.data

    def update_record(self, key, value):
        if key not in self.data:
            return False, "Запис з таким ключем не існує."
        self.data[key] = value
        self.save_data()
        return True, "Запис оновлено успішно."

    def delete_record(self, key):
        if key not in self.data:
            return False, "Запис з таким ключем не існує."
        del self.data[key]
        self.save_data()
        return True, "Запис видалено успішно."


class ConsoleView:
    def display_menu(self):
        print("Меню CRUD операцій")
        print("1. Створити запис")
        print("2. Показати записи")
        print("3. Оновити запис")
        print("4. Видалити запис")
        print("5. Вийти")

    def get_user_choice(self):
        return input("Введіть номер операції: ")

    def prompt_for_record(self):
        key = input("Введіть ключ запису: ")
        value = input("Введіть значення запису: ")
        return key, value

    def prompt_for_key(self):
        return input("Введіть ключ запису: ")

    def show_message(self, message):
        print(message)

    def display_records(self, records):
        if records:
            print("Записи в базі даних")
            for key, value in records.items():
                print(f"{key}: {value}")
        else:
            print("База даних порожня.")


class ConsoleController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        while True:
            self.view.display_menu()
            choice = self.view.get_user_choice()
            if choice == "1":
                key, value = self.view.prompt_for_record()
                success, msg = self.model.create_record(key, value)
                self.view.show_message(msg)
            elif choice == "2":
                records = self.model.read_records()
                self.view.display_records(records)
            elif choice == "3":
                key = self.view.prompt_for_key()
                new_value = input("Введіть нове значення: ")
                success, msg = self.model.update_record(key, new_value)
                self.view.show_message(msg)
            elif choice == "4":
                key = self.view.prompt_for_key()
                success, msg = self.model.delete_record(key)
                self.view.show_message(msg)
            elif choice == "5":
                self.view.show_message("Вихід з програми.")
                break
            else:
                self.view.show_message("Невірний вибір, спробуйте ще раз.")


class GUIView:
    def __init__(self, root):
        self.root = root
        self.root.title("Граф. інтерфейс")

        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.label_key = tk.Label(self.frame, text="Ключ:")
        self.label_key.grid(row=0, column=0, sticky="e")
        self.entry_key = tk.Entry(self.frame)
        self.entry_key.grid(row=0, column=1)

        self.label_value = tk.Label(self.frame, text="Значення:")
        self.label_value.grid(row=1, column=0, sticky="e")
        self.entry_value = tk.Entry(self.frame)
        self.entry_value.grid(row=1, column=1)

        self.btn_create = tk.Button(self.frame, text="Створити")
        self.btn_create.grid(row=2, column=0, pady=5)

        self.btn_update = tk.Button(self.frame, text="Оновити")
        self.btn_update.grid(row=2, column=1, pady=5)

        self.btn_delete = tk.Button(self.frame, text="Видалити")
        self.btn_delete.grid(row=3, column=0, pady=5)

        self.btn_read = tk.Button(self.frame, text="Показати всі записи")
        self.btn_read.grid(row=3, column=1, pady=5)

        self.text_display = tk.Text(root, height=10, width=40)
        self.text_display.pack(padx=10, pady=10)

    def get_key(self):
        return self.entry_key.get()

    def get_value(self):
        return self.entry_value.get()

    def clear_entries(self):
        self.entry_key.delete(0, tk.END)
        self.entry_value.delete(0, tk.END)

    def display_records(self, records):
        self.text_display.delete(1.0, tk.END)
        if records:
            for key, value in records.items():
                self.text_display.insert(tk.END, f"{key}: {value}\n")
        else:
            self.text_display.insert(tk.END, "База даних порожня.\n")

    def show_message(self, message):
        messagebox.showinfo("Інформація", message)


class GUIController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.btn_create.config(command=self.create_record)
        self.view.btn_read.config(command=self.read_records)
        self.view.btn_update.config(command=self.update_record)
        self.view.btn_delete.config(command=self.delete_record)

    def create_record(self):
        key = self.view.get_key()
        value = self.view.get_value()
        success, msg = self.model.create_record(key, value)
        self.view.show_message(msg)
        self.read_records()
        self.view.clear_entries()

    def read_records(self):
        records = self.model.read_records()
        self.view.display_records(records)

    def update_record(self):
        key = self.view.get_key()
        value = self.view.get_value()
        success, msg = self.model.update_record(key, value)
        self.view.show_message(msg)
        self.read_records()
        self.view.clear_entries()

    def delete_record(self):
        key = self.view.get_key()
        success, msg = self.model.delete_record(key)
        self.view.show_message(msg)
        self.read_records()
        self.view.clear_entries()


def main():
    model = Model()

    print("Оберіть інтерфейс:")
    print("1 - Графічний (GUI)")
    print("2 - Консольний")
    choice = input("Введіть 1 або 2: ")

    if choice == "1":
        root = tk.Tk()
        view = GUIView(root)
        controller = GUIController(model, view)
        root.mainloop()
    elif choice == "2":
        view = ConsoleView()
        controller = ConsoleController(model, view)
        controller.run()
    else:
        print("Невірний вибір. Завершення програми.")

if __name__ == "__main__":
    main()
