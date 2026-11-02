import tkinter as tk
from tkinter import messagebox

class ExpertSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Експертна система профорієнтації")
        self.history = []
        self.weights = []
        self.result = ""

        # Створення елементів інтерфейсу
        self.question_label = tk.Label(self.root, text="", font=("Arial", 14), wraplength=400)
        self.question_label.pack(pady=20)

        self.options_frame = tk.Frame(self.root)
        self.options_frame.pack(pady=10)

        self.next_button = tk.Button(self.root, text="Далі", command=self.next_question)
        self.next_button.pack(pady=20)

        self.questions = []
        self.current_question_index = 0
        self.create_questions()
        self.show_question()

    def create_questions(self):
        # Питання з варіантами відповідей та вагами
        self.questions = [
            ("Чи є обмеження по часу у навчанні?", ["Так", "Ні"], [0.6, 0.4]),
            ("Скільки годин ви можете присвячувати навчанню?", ["1 годину на день", "Від 2 до 3 годин на день"], [0.7, 0.9]),
            ("Чи цікавить вас ремонт техніки?", ["Так", "Ні"], [0.8, 0.5]),
            ("Чи подобається вам допомагати іншим у вирішенні проблем?", ["Так", "Ні"], [0.9, 0.9]),
            ("Які науки вам більш до вподоби?", ["Гуманітарні", "Технічні"], [0.5, 0.5]),
            ("Який гуманітарний предмет вам більше цікавий?", ["Історія", "Література"], [0.7, 0.8]),
            ("Який технічний предмет вам більше цікавий?", ["Математика", "Фізика", "Інформатика"], [0.7, 0.8, 0.9]),
        ]

    def show_question(self):
        # Очищення попередніх варіантів
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        if self.current_question_index < len(self.questions):
            question, options, weights = self.questions[self.current_question_index]
            self.question_label.config(text=question)

            # Створення кнопок для варіантів відповіді
            for i, option in enumerate(options):
                button = tk.Button(self.options_frame, text=option, command=lambda opt=option, w=weights[i]: self.record_answer(opt, w))
                button.pack(side="top", fill="x", pady=5)
        else:
            self.show_result()

    def record_answer(self, answer, weight):
        self.history.append((self.questions[self.current_question_index][0], answer))
        self.weights.append(weight)
        self.current_question_index += 1
        self.show_question()

    def next_question(self):
        self.show_question()

    def show_result(self):
        score = sum(self.weights)
        # Визначення професії на основі суми ваг
        if score >= 7.0:
            self.result = "Інженер-конструктор"
        elif 6.0 <= score < 7.0:
            self.result = "Мобільний розробник"
        elif 5.0 <= score < 6.0:
            self.result = "Фізик-дослідник"
        elif 4.0 <= score < 5.0:
            self.result = "Економіст"
        else:
            self.result = "Оператор call-центру"

        # Виведення результату
        messagebox.showinfo("Результат", f"Ваша професія: {self.result}\nПричини вибору:\n" + "\n".join([f"{q}: {a}" for q, a in self.history]))

        # Завершення роботи
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpertSystemGUI(root)
    root.mainloop()
