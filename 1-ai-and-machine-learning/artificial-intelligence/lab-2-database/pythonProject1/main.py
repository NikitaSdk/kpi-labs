import tkinter as tk
from tkinter import messagebox
from database import initialize_database, connect, delete_database

# Видаляємо стару базу даних та створюємо нову
delete_database()
initialize_database()

class CareerGuidanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Експертна система профорієнтації")

        # Ініціалізація виборів користувача
        self.selected_subjects = []
        self.selected_certificates = []
        self.selected_hobbies = []
        self.self_learning_var = tk.StringVar(value="Ні")
        self.selected_sections = []

        # Завантаження даних з бази
        self.subjects = self.load_subjects() or []
        self.certificates = self.load_certificates() or []
        self.hobbies = self.load_hobbies() or []
        self.sections = self.load_sections() or []

        # Створення інтерфейсу
        self.create_widgets()
        self.update_results_display()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        tk.Button(self.root, text="Оберіть предмети", command=self.choose_subjects).pack(pady=5)
        tk.Button(self.root, text="Оберіть сертифікати", command=self.choose_certificates).pack(pady=5)
        tk.Button(self.root, text="Оберіть хобі", command=self.choose_hobbies).pack(pady=5)
        tk.Button(self.root, text="Схильність до самонавчання", command=self.choose_self_learning).pack(pady=5)
        tk.Button(self.root, text="Оберіть додаткові секції", command=self.choose_sections).pack(pady=5)

        # Рамка для відображення обраних параметрів
        self.results_frame = tk.Frame(self.root, relief=tk.GROOVE, borderwidth=2)
        self.results_frame.pack(padx=10, pady=10, fill=tk.BOTH)
        self.results_text = tk.Label(self.results_frame, text="Обрані параметри будуть відображатись тут.")
        self.results_text.pack(pady=5)

        tk.Button(self.root, text="Знайти професії", command=self.find_professions).pack(pady=20)

    def update_results_display(self):
        text = (
            f"Обрані предмети: {', '.join(self.selected_subjects)}\n"
            f"Обрані сертифікати: {', '.join(self.selected_certificates)}\n"
            f"Обрані хобі: {', '.join(self.selected_hobbies)}\n"
            f"Схильність до самонавчання: {self.self_learning_var.get()}\n"
            f"Обрані секції: {', '.join(self.selected_sections)}"
        )
        self.results_text.config(text=text)

    # Нова функція is_profession_match
    def is_profession_match(profession_criteria, selected_criteria):
        """
        Перевіряє, чи підходять критерії професії до обраних користувачем критеріїв.
        Враховує як повний збіг, так і частковий збіг критеріїв.
        """
        # Перевірка на повний збіг критеріїв
        if profession_criteria.issubset(selected_criteria):
            return True

        # Додаткова перевірка: якщо критерії професії перекривають обрані користувачем критерії частково
        if len(profession_criteria.intersection(selected_criteria)) >= len(profession_criteria) - 1:
            return True

        return False

    def load_subjects(self):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM subjects")
        subjects = [row[0] for row in cursor.fetchall()]
        conn.close()
        return subjects

    def load_certificates(self):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM certificates")
        certificates = [row[0] for row in cursor.fetchall()]
        conn.close()
        return certificates

    def load_hobbies(self):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM hobbies")
        hobbies = [row[0] for row in cursor.fetchall()]
        conn.close()
        return hobbies

    def load_sections(self):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM additional_sections")
        sections = [row[0] for row in cursor.fetchall()]
        conn.close()
        return sections

    def choose_subjects(self):
        window = self.create_selection_window("Оберіть предмети", self.subjects, self.selected_subjects)

    def choose_certificates(self):
        window = self.create_selection_window("Оберіть сертифікати", self.certificates, self.selected_certificates)

    def choose_hobbies(self):
        window = self.create_selection_window("Оберіть хобі", self.hobbies, self.selected_hobbies)

    def choose_self_learning(self):
        self_learning_window = tk.Toplevel(self.root)
        self_learning_window.title("Схильність до самонавчання")
        tk.Radiobutton(self_learning_window, text="Так", variable=self.self_learning_var, value="Так").pack(anchor=tk.W)
        tk.Radiobutton(self_learning_window, text="Ні", variable=self.self_learning_var, value="Ні").pack(anchor=tk.W)
        tk.Button(self_learning_window, text="Далі", command=lambda: [self.update_results_display(), self_learning_window.destroy()]).pack(pady=10)

    def choose_sections(self):
        window = self.create_selection_window("Оберіть додаткові секції", self.sections, self.selected_sections)

    def create_selection_window(self, title, options, selected_list):
        window = tk.Toplevel(self.root)
        window.title(title)
        vars_list = []

        for option in options:
            var = tk.BooleanVar()
            chk = tk.Checkbutton(window, text=option, variable=var)
            chk.pack(anchor=tk.W)
            vars_list.append((var, option))

        tk.Button(window, text="Далі", command=lambda: [self.update_selection(vars_list, selected_list), window.destroy()]).pack(pady=10)

    def update_selection(self, vars_list, selected_list):
        selected_list.clear()
        selected_list.extend([option for var, option in vars_list if var.get()])
        self.update_results_display()

    def find_professions(self):
        if not (
                self.selected_subjects or self.selected_certificates or self.selected_hobbies or self.selected_sections):
            messagebox.showwarning("Попередження", "Будь ласка, оберіть хоча б один критерій.")
            return

        conn = connect()
        cursor = conn.cursor()

        query = """
        SELECT p.name, s.name, ps.certificate, ps.hobby, ps.self_learning, ps.additional_section
        FROM professions p
        JOIN profession_subjects ps ON p.id = ps.profession_id
        LEFT JOIN subjects s ON ps.subject_id = s.id
        """
        cursor.execute(query)
        profession_data = cursor.fetchall()
        conn.close()

        selected_criteria = set(self.selected_subjects + self.selected_certificates + self.selected_hobbies +
                                self.selected_sections + (
                                    [self.self_learning_var.get()] if self.self_learning_var.get() == "Так" else []))

        matched_professions = []

        profession_criteria_map = {}
        for row in profession_data:
            profession_name = row[0]
            criteria = set(filter(None, row[1:]))

            if profession_name not in profession_criteria_map:
                profession_criteria_map[profession_name] = criteria
            else:
                profession_criteria_map[profession_name].update(criteria)

        for profession, criteria in profession_criteria_map.items():
            if self.is_profession_match(criteria, selected_criteria):
                matched_professions.append(profession)

        if matched_professions:
            self.show_results(matched_professions)
        else:
            messagebox.showinfo("Результат", "Немає професій, які відповідають обраним критеріям.")
    def show_results(self, matched_professions):
        result_window = tk.Toplevel(self.root)
        result_window.title("Результати пошуку")

        tk.Label(result_window, text="Ваші обрані критерії:", font=("Arial", 14)).pack(pady=5)
        tk.Label(result_window, text=", ".join(
            self.selected_subjects + self.selected_certificates + self.selected_hobbies + self.selected_sections),
                 font=("Arial", 12)).pack(pady=5)

        tk.Label(result_window, text="Професії, які задовольняють обраним критеріям:", font=("Arial", 14)).pack(pady=10)
        profession_listbox = tk.Listbox(result_window, font=("Arial", 12), width=50, height=10)
        for profession in matched_professions:
            profession_listbox.insert(tk.END, profession)
        profession_listbox.pack(pady=5)

        tk.Button(result_window, text="Закрити", command=result_window.destroy).pack(pady=10)

    def on_closing(self):
        delete_database()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CareerGuidanceApp(root)
    root.mainloop()
