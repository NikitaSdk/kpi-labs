import tkinter as tk
from tkinter import messagebox
from tree import decision_tree

class ExpertSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Експертна система профорієнтації")
        self.history = []
        self.weights = []
        self.result = ""
        self.current_node = "root"
        self.selected_answer = None


        self.question_label = tk.Label(self.root, text="", font=("Arial", 14), wraplength=400)
        self.question_label.pack(pady=20)

        self.options_frame = tk.Frame(self.root)
        self.options_frame.pack(pady=10)

        self.next_button = tk.Button(self.root, text="Далі", command=self.next_question, state=tk.DISABLED)
        self.next_button.pack(pady=20)

        self.show_question()

    def show_question(self):

        for widget in self.options_frame.winfo_children():
            widget.destroy()

        node = decision_tree.get(self.current_node)
        if not node:
            self.show_result()
            return

        self.question_label.config(text=node["question"])
        self.selected_answer = None
        self.next_button.config(state=tk.DISABLED)


        if node["question"] == "Яку ви хочете мати зарплатню у майбутньому (у доларах)?":
            self.salary_entry = tk.Entry(self.options_frame)
            self.salary_entry.pack(pady=10)
            self.salary_entry.bind("<KeyRelease>", self.enable_next_button)
        else:
            self.answer_var = tk.StringVar(value="init")
            for answer, data in node["answers"].items():
                button = tk.Radiobutton(
                    self.options_frame,
                    text=f"{answer} (вага: {data['weight']})",
                    variable=self.answer_var,
                    value=answer,
                    command=self.enable_next_button
                )
                button.pack(anchor="w", pady=5)

    def enable_next_button(self, event=None):
        """Активує кнопку 'Далі', коли користувач робить вибір або вводить значення."""
        if self.answer_var.get() != "init" or (hasattr(self, "salary_entry") and self.salary_entry.get().isdigit()):
            self.next_button.config(state=tk.NORMAL)

    def next_question(self):
        """Обробляє перехід до наступного питання після натискання кнопки 'Далі'."""
        node = decision_tree[self.current_node]


        if node["question"] == "Яку ви хочете мати зарплатню у майбутньому (у доларах)?":
            salary_input = self.salary_entry.get()


            if not salary_input.isdigit():
                messagebox.showerror("Помилка вводу", "Будь ласка, введіть коректне число для зарплати.")
                return

            try:
                salary = int(salary_input)
            except ValueError:
                messagebox.showerror("Помилка вводу", "Неможливо обробити введене значення. Введіть число.")
                return


            if salary > 10_000_000:
                messagebox.showerror("Помилка вводу", "Введене значення занадто велике. Введіть реалістичну зарплату.")
                return


            self.history.append((node["question"], f"{salary} доларів"))
            if salary <= 1000:
                self.weights.append(0.5)
                self.result = "Редактор"
            elif 1000 < salary <= 3000:
                self.weights.append(0.7)
                self.result = "Копірайтер"
            else:
                self.weights.append(0.9)
                self.result = "Письменник"
            self.show_result()
            return


        selected_option = self.answer_var.get()
        if selected_option == "init":
            messagebox.showwarning("Попередження", "Будь ласка, оберіть відповідь.")
            return

        self.history.append((node["question"], selected_option))
        self.weights.append(node["answers"][selected_option].get("weight", 0))

        if "next" in node["answers"][selected_option]:
            self.current_node = node["answers"][selected_option]["next"]
            self.show_question()
        elif "result" in node["answers"][selected_option]:
            self.result = node["answers"][selected_option]["result"]
            self.show_result()

    def show_result_window(self):

        if not self.result:
            self.result = "Немає результату"


        total_weight = sum(self.weights)


        result_window = tk.Toplevel(self.root)
        result_window.title("Результат")
        result_window.geometry("600x500")


        result_label = tk.Label(
            result_window,
            text=f"Ваша професія: {self.result}",
            font=("Arial", 24, "bold"),
            wraplength=500,
            justify="center"
        )
        result_label.pack(pady=20)


        explanations_text = "\n".join([f"{q}: {a} (вага: {w})" for (q, a), w in zip(self.history, self.weights)])
        explanations_label = tk.Label(
            result_window,
            text=f"Пояснення:\n{explanations_text}",
            font=("Arial", 14),
            wraplength=500,
            justify="left"
        )
        explanations_label.pack(pady=10)


        total_weight_label = tk.Label(
            result_window,
            text=f"Вага: {total_weight:.2f}",
            font=("Arial", 14),
            wraplength=500,
            justify="center"
        )
        total_weight_label.pack(pady=10)

        close_button = tk.Button(result_window, text="Закрити", command=self.quit_program)
        close_button.pack(pady=20)

    def quit_program(self):
        self.root.quit()
        self.root.destroy()

    def show_result(self):
        self.show_result_window()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpertSystemGUI(root)
    root.mainloop()
