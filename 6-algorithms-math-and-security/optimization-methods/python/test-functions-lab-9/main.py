import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time


np.random.seed(42)


def goldstein_price(point):

    x, y = point

    part1 = 1 + (x + y + 1) ** 2 * (
        19 - 14 * x + 3 * x ** 2 - 14 * y + 6 * x * y + 3 * y ** 2
    )

    part2 = 30 + (2 * x - 3 * y) ** 2 * (
        18 - 32 * x + 12 * x ** 2 + 48 * y - 36 * x * y + 27 * y ** 2
    )

    return part1 * part2


def booth(point):

    x, y = point
    return (x + 2 * y - 7) ** 2 + (2 * x + y - 5) ** 2


def holder_table(point):
    x, y = point
    return -abs(
        np.sin(x) * np.cos(y) *
        np.exp(abs(1 - np.sqrt(x ** 2 + y ** 2) / np.pi))
    )


functions = {
    "Функція Гольдшейна-Прайса": {
        "func": goldstein_price,
        "bounds": (-2, 2),
        "known_min": 3.0,
        "known_point": (0, -1),
        "step": 0.25,
        "start_candidates": 300,
        "restarts": 30
    },
    "Функція Бута": {
        "func": booth,
        "bounds": (-10, 10),
        "known_min": 0.0,
        "known_point": (1, 3),
        "step": 0.8,
        "start_candidates": 300,
        "restarts": 30
    },
    "Таблична функція Хольдера": {
        "func": holder_table,
        "bounds": (-10, 10),
        "known_min": -19.2085,
        "known_point": (8.05502, 9.66459),
        "step": 0.8,
        "start_candidates": 1000,
        "restarts": 80
    }
}



def clip_point(point, bounds):
    low, high = bounds
    return np.clip(point, low, high)


def create_simplex(start, step, bounds):

    x0 = np.array(start, dtype=float)

    simplex = np.array([
        x0,
        x0 + np.array([step, 0.0]),
        x0 + np.array([0.0, step])
    ])

    return np.array([clip_point(p, bounds) for p in simplex])


def choose_good_start(func, bounds, candidates_count=300):

    low, high = bounds

    candidates = np.random.uniform(low, high, size=(candidates_count, 2))
    values = np.array([func(p) for p in candidates])

    best_index = np.argmin(values)
    return candidates[best_index]


def normalize_history(history, target_length):

    if len(history) == 0:
        return []

    if len(history) >= target_length:
        return history[:target_length]

    last_value = history[-1]
    return history + [last_value] * (target_length - len(history))


def make_safe_filename(text):

    return (
        text
        .replace(" ", "_")
        .replace(":", "")
        .replace("-", "_")
        .replace(",", "")
        .replace("(", "")
        .replace(")", "")
    )




def basic_modified_simplex_method(func, bounds, start=None, step=1.0, max_iter=300, eps=1e-9):

    if start is None:
        start = choose_good_start(func, bounds, candidates_count=300)

    alpha = 1.0
    gamma = 2.0
    beta = 0.5
    sigma = 0.5

    simplex = create_simplex(start, step, bounds)
    history = []

    for iteration in range(max_iter):
        values = np.array([func(p) for p in simplex])

        order = np.argsort(values)
        simplex = simplex[order]
        values = values[order]

        best = simplex[0]
        worst = simplex[-1]

        f_best = values[0]
        f_second_worst = values[1]
        f_worst = values[-1]

        history.append(f_best)

        if np.std(values) < eps:
            break

        centroid = np.mean(simplex[:-1], axis=0)

        # Відбиття
        reflected = centroid + alpha * (centroid - worst)
        reflected = clip_point(reflected, bounds)
        f_reflected = func(reflected)

        if f_reflected < f_best:
            # Розтягнення
            expanded = centroid + gamma * (reflected - centroid)
            expanded = clip_point(expanded, bounds)
            f_expanded = func(expanded)

            if f_expanded < f_reflected:
                simplex[-1] = expanded
            else:
                simplex[-1] = reflected

        elif f_reflected < f_second_worst:
            simplex[-1] = reflected

        else:
            # Стискання
            contracted = centroid + beta * (worst - centroid)
            contracted = clip_point(contracted, bounds)
            f_contracted = func(contracted)

            if f_contracted < f_worst:
                simplex[-1] = contracted
            else:
                # Редукція
                simplex[1:] = best + sigma * (simplex[1:] - best)
                simplex = np.array([clip_point(p, bounds) for p in simplex])

    values = np.array([func(p) for p in simplex])
    best_index = np.argmin(values)
    best_point = simplex[best_index]
    best_value = values[best_index]

    return best_point, best_value, history, len(history)



def modified_simplex_method_with_random_restarts(
        func,
        bounds,
        restarts=30,
        step=1.0,
        max_iter=300,
        eps=1e-9
):

    best_point = None
    best_value = float("inf")
    best_history = []
    total_iterations = 0

    for restart in range(restarts):
        start = choose_good_start(func, bounds, candidates_count=80)

        point, value, history, iterations = basic_modified_simplex_method(
            func=func,
            bounds=bounds,
            start=start,
            step=step,
            max_iter=max_iter,
            eps=eps
        )

        total_iterations += iterations

        if value < best_value:
            best_value = value


            best_point = point
            best_history = history

    return best_point, best_value, best_history, total_iterations


def adaptive_modified_simplex_single_run(
        func,
        bounds,
        start=None,
        step=1.0,
        max_iter=300,
        eps=1e-9
):

    if start is None:
        start = choose_good_start(func, bounds, candidates_count=300)

    alpha = 1.0
    gamma = 2.0
    beta = 0.5
    sigma = 0.5

    simplex = create_simplex(start, step, bounds)
    history = []

    previous_best = float("inf")

    for iteration in range(max_iter):
        values = np.array([func(p) for p in simplex])

        order = np.argsort(values)
        simplex = simplex[order]
        values = values[order]

        best = simplex[0]
        worst = simplex[-1]

        f_best = values[0]
        f_second_worst = values[1]
        f_worst = values[-1]

        history.append(f_best)

        if np.std(values) < eps:
            break

        # Адаптація параметрів
        if f_best < previous_best:
            gamma = min(2.7, gamma * 1.03)
            beta = max(0.25, beta * 0.98)
            sigma = max(0.30, sigma * 0.98)
        else:
            gamma = max(1.2, gamma * 0.95)
            beta = min(0.75, beta * 1.03)
            sigma = min(0.80, sigma * 1.04)

        previous_best = f_best

        centroid = np.mean(simplex[:-1], axis=0)

        # Відбиття
        reflected = centroid + alpha * (centroid - worst)
        reflected = clip_point(reflected, bounds)
        f_reflected = func(reflected)

        if f_reflected < f_best:
            # Розтягнення
            expanded = centroid + gamma * (reflected - centroid)
            expanded = clip_point(expanded, bounds)
            f_expanded = func(expanded)

            if f_expanded < f_reflected:
                simplex[-1] = expanded
            else:
                simplex[-1] = reflected

        elif f_reflected < f_second_worst:
            simplex[-1] = reflected

        else:
            # Стискання
            contracted = centroid + beta * (worst - centroid)
            contracted = clip_point(contracted, bounds)
            f_contracted = func(contracted)

            if f_contracted < f_worst:
                simplex[-1] = contracted
            else:
                # Редукція
                simplex[1:] = best + sigma * (simplex[1:] - best)
                simplex = np.array([clip_point(p, bounds) for p in simplex])

    values = np.array([func(p) for p in simplex])
    best_index = np.argmin(values)
    best_point = simplex[best_index]
    best_value = values[best_index]

    return best_point, best_value, history, len(history)


def adaptive_modified_simplex_method(
        func,
        bounds,
        restarts=20,
        step=1.0,
        max_iter=300,
        eps=1e-9
):
    best_point = None
    best_value = float("inf")
    best_history = []
    total_iterations = 0

    for restart in range(restarts):
        start = choose_good_start(func, bounds, candidates_count=80)

        point, value, history, iterations = adaptive_modified_simplex_single_run(
            func=func,
            bounds=bounds,
            start=start,
            step=step,
            max_iter=max_iter,
            eps=eps
        )

        total_iterations += iterations

        if value < best_value:
            best_value = value
            best_point = point
            best_history = history

    return best_point, best_value, best_history, total_iterations


methods = {
    "Базова реалізація модифікованого симплексного методу":
        basic_modified_simplex_method,

    "Модифікований симплексний метод з випадковими перезапусками":
        modified_simplex_method_with_random_restarts,

    "Адаптивний модифікований симплексний метод":
        adaptive_modified_simplex_method
}

all_results = []
all_histories = {}

for func_name, info in functions.items():
    func = info["func"]
    bounds = info["bounds"]
    known_min = info["known_min"]
    step = info["step"]
    start_candidates = info["start_candidates"]
    restarts = info["restarts"]

    all_histories[func_name] = {}

    for method_name, method in methods.items():
        start_time = time.time()

        if method_name == "Базова реалізація модифікованого симплексного методу":
            start = choose_good_start(func, bounds, candidates_count=start_candidates)

            point, value, history, iterations = method(
                func=func,
                bounds=bounds,
                start=start,
                step=step,
                max_iter=500,
                eps=1e-10
            )

        elif method_name == "Модифікований симплексний метод з випадковими перезапусками":
            point, value, history, iterations = method(
                func=func,
                bounds=bounds,
                restarts=restarts,
                step=step,
                max_iter=500,
                eps=1e-10
            )

        else:
            point, value, history, iterations = method(
                func=func,
                bounds=bounds,
                restarts=max(15, restarts // 2),
                step=step,
                max_iter=500,
                eps=1e-10
            )

        elapsed_time = time.time() - start_time
        error = abs(value - known_min)

        all_results.append({
            "Функція": func_name,
            "Метод": method_name,
            "x": point[0],
            "y": point[1],
            "f(x,y)": value,
            "Відомий мінімум": known_min,
            "Похибка": error,
            "Ітерації": iterations,
            "Час, с": elapsed_time
        })

        all_histories[func_name][method_name] = history



results_df = pd.DataFrame(all_results)
rounded_df = results_df.copy()

for col in ["x", "y", "f(x,y)", "Відомий мінімум", "Похибка", "Час, с"]:
    rounded_df[col] = rounded_df[col].astype(float).round(6)

print("\n" + "=" * 160)
print("ЗАГАЛЬНА ТАБЛИЦЯ РЕЗУЛЬТАТІВ")
print("=" * 160)
print(rounded_df.to_string(index=False))

rounded_df.to_csv("modified_simplex_results.csv", index=False, encoding="utf-8-sig")
print("\nФайл з результатами збережено як: modified_simplex_results.csv")



for func_name in functions.keys():
    print("\n" + "=" * 160)
    print(f"ТАБЛИЦЯ РЕЗУЛЬТАТІВ ДЛЯ: {func_name}")
    print("=" * 160)

    table = rounded_df[rounded_df["Функція"] == func_name][
        ["Метод", "x", "y", "f(x,y)", "Відомий мінімум", "Похибка", "Ітерації", "Час, с"]
    ]

    print(table.to_string(index=False))


for func_name, histories in all_histories.items():
    plt.figure(figsize=(15, 7))

    max_len = max(len(history) for history in histories.values())

    for method_name, history in histories.items():
        normalized = normalize_history(history, max_len)

        # У легенді виводиться повна назва методу
        plt.plot(normalized, label=method_name)

    plt.title(f"Графік збіжності для: {func_name}")
    plt.xlabel("Ітерація")
    plt.ylabel("Найкраще значення f(x,y)")
    plt.grid(True)
    plt.legend(fontsize=8)
    plt.tight_layout()

    filename = f"convergence_value_{make_safe_filename(func_name)}.png"
    plt.savefig(filename, dpi=300)

    print(f"Графік збережено як: {filename}")

    plt.show()


print("\n" + "=" * 160)
print("НАЙКРАЩІ РЕЗУЛЬТАТИ ДЛЯ КОЖНОЇ ФУНКЦІЇ")
print("=" * 160)

for func_name in functions.keys():
    subset = rounded_df[rounded_df["Функція"] == func_name]
    best_row = subset.loc[subset["Похибка"].idxmin()]

    print(f"\n{func_name}")
    print(f"Найкращий метод: {best_row['Метод']}")
    print(f"x = {best_row['x']}")
    print(f"y = {best_row['y']}")
    print(f"f(x,y) = {best_row['f(x,y)']}")
    print(f"Похибка = {best_row['Похибка']}")
    print(f"Ітерації = {best_row['Ітерації']}")
    print(f"Час, с = {best_row['Час, с']}")