class ExpertSystem:
    def __init__(self):
        self.history = []
        self.weights = []
        self.result = ""

    def ask_question(self, question, options, weights):
        print(question)
        for i, option in enumerate(options):
            print(f"{i + 1}. {option}")
        choice = int(input("Ваш вибір (введіть номер): ")) - 1
        self.history.append((question, options[choice]))
        self.weights.append(weights[choice])
        return options[choice]

    def evaluate(self):
        score = sum(self.weights)
        return score

    def run(self):
        # Гілка 1-5
        answer = self.ask_question(
            "Чи є обмеження по часу у навчанні?",
            ["Так", "Ні"],
            [0.6, 0.4]
        )

        if answer == "Так":
            hours = self.ask_question(
                "Скільки годин ви можете присвячувати навчанню?",
                ["1 годину на день", "Від 2 до 3 годин на день"],
                [0.7, 0.9]
            )
            if hours == "1 годину на день":
                interest = self.ask_question(
                    "Чи цікавить вас ремонт техніки?",
                    ["Так", "Ні"],
                    [0.8, 0.5]
                )
                if interest == "Так":
                    self.result = "Технік-консультант"
                else:
                    self.result = "Оператор call-центру"
            elif hours == "Від 2 до 3 годин на день":
                help_others = self.ask_question(
                    "Чи подобається вам допомагати іншим у вирішенні проблем?",
                    ["Так", "Ні"],
                    [0.9, 0.9]
                )
                if help_others == "Так":
                    interest = self.ask_question(
                        "Чи цікавить вас ремонт техніки?",
                        ["Так", "Ні"],
                        [0.8, 0.5]
                    )
                    if interest == "Так":
                        self.result = "Технік-консультант"
                    else:
                        self.result = "Оператор call-центру"
                else:
                    self.result = "Ювелір"

        # Гілка 6-21
        else:
            science = self.ask_question(
                "Які науки вам більш до вподоби?",
                ["Гуманітарні", "Технічні"],
                [0.5, 0.5]
            )
            if science == "Гуманітарні":
                subject = self.ask_question(
                    "Який гуманітарний предмет вам більше цікавий?",
                    ["Історія", "Література"],
                    [0.7, 0.8]
                )
                if subject == "Історія":
                    research = self.ask_question(
                        "Чи вам цікаво займатися історичними дослідженнями чи викладанням?",
                        ["Дослідження", "Викладання"],
                        [0.9, 0.8]
                    )
                    if research == "Дослідження":
                        self.result = "Археолог"
                    else:
                        self.result = "Викладач Історії"
                elif subject == "Література":
                    work_with_people = self.ask_question(
                        "Чи полюбляєте ви працювати з людьми?",
                        ["Так", "Ні"],
                        [0.8, 0.6]
                    )
                    if work_with_people == "Так":
                        self.result = "Системний адміністратор"
                    else:
                        salary = self.ask_question(
                            "Яку ви хочете мати зарплатню у майбутньому (у доларах)?",
                            ["1000", "1500-3000", "понад 5000"],
                            [0.5, 0.7, 0.9]
                        )
                        if salary == "1000":
                            self.result = "Редактор"
                        elif salary == "1500-3000":
                            self.result = "Копірайтер"
                        else:
                            self.result = "Письменник"
            elif science == "Технічні":
                subject = self.ask_question(
                    "Який технічний предмет вам більше цікавий?",
                    ["Математика", "Фізика", "Інформатика"],
                    [0.7, 0.8, 0.9]
                )
                if subject == "Математика":
                    analysis = self.ask_question(
                        "Чи подобається вам аналіз даних та розв'язання задач?",
                        ["Так", "Ні"],
                        [0.8, 0.4]
                    )
                    if analysis == "Ні":
                        self.result = "Економіст"
                    else:
                        approach = self.ask_question(
                            "Вам більше подобається теоретичний чи прикладний підхід?",
                            ["Теоретичний", "Прикладний"],
                            [0.6, 0.7]
                        )
                        if approach == "Прикладний":
                            self.result = "Аналітик даних"
                        else:
                            research = self.ask_question(
                                "Чи готові ви займатися науковими дослідженнями?",
                                ["Так", "Ні"],
                                [0.9, 0.5]
                            )
                            if research == "Так":
                                self.result = "Науковий математик"
                            else:
                                self.result = "Викладач математики"
                elif subject == "Фізика":
                    experiments = self.ask_question(
                        "Чи подобається вам проводити експерименти в лабораторії?",
                        ["Так", "Ні"],
                        [0.9, 0.6]
                    )
                    if experiments == "Так":
                        self.result = "Фізик-дослідник"
                    else:
                        design = self.ask_question(
                            "Чи хочете ви займатися проєктуванням механізмів?",
                            ["Так", "Ні"],
                            [0.8, 0.5]
                        )
                        if design == "Так":
                            self.result = "Інженер-конструктор"
                        else:
                            self.result = "Механічний інженер"
                elif subject == "Інформатика":
                    choice = self.ask_question(
                        "Вам цікавіше програмування чи адміністрування?",
                        ["Програмування", "Адміністрування"],
                        [0.9, 0.7]
                    )
                    if choice == "Адміністрування":
                        self.result = "Системний адміністратор"
                    else:
                        mobile = self.ask_question(
                            "Чи цікавить вас розробка мобільних додатків?",
                            ["Так", "Ні"],
                            [0.8, 0.7]
                        )
                        if mobile == "Так":
                            self.result = "Мобільний розробник"
                        else:
                            self.result = "Розробник ПЗ"

        # Виведення результату
        print("\nРезультат: Ваша професія -", self.result)
        print("Причини вибору:")
        for q, a in self.history:
            print(f"{q}: {a}")
