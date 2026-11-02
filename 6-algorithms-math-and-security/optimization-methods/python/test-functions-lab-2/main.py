import math
import random
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

random.seed(42)
np.random.seed(42)


# =========================================================
# Тестові функції
# =========================================================
def goldstein_price(x, y):
    return (
        1 + (x + y + 1) ** 2 *
        (19 - 14 * x + 3 * x ** 2 - 14 * y + 6 * x * y + 3 * y ** 2)
    ) * (
        30 + (2 * x - 3 * y) ** 2 *
        (18 - 32 * x + 12 * x ** 2 + 48 * y - 36 * x * y + 27 * y ** 2)
    )


def booth(x, y):
    return (x + 2 * y - 7) ** 2 + (2 * x + y - 5) ** 2


def holder_table(x, y):
    return -abs(
        math.sin(x) * math.cos(y) *
        math.exp(abs(1 - math.sqrt(x ** 2 + y ** 2) / math.pi))
    )


# =========================================================
# Допоміжні функції
# =========================================================
def clip_point(point, bounds):
    lower, upper = bounds
    return np.clip(point, lower, upper)


def generate_population(size, bounds):
    lower, upper = bounds
    return [
        np.array([
            random.uniform(lower, upper),
            random.uniform(lower, upper)
        ], dtype=float)
        for _ in range(size)
    ]


def fitness(population, func):
    return np.array([func(ind[0], ind[1]) for ind in population], dtype=float)


def get_best_individual(population, func):
    values = fitness(population, func)
    best_index = np.argmin(values)
    return population[best_index].copy(), float(values[best_index])


def reached_target(history, target_value=None, target_tolerance=1e-6):
    if target_value is None:
        return False

    best_value = history[-1][0]
    return abs(best_value - target_value) <= target_tolerance


def stagnation_detected(history, tolerance=1e-8, patience=30, min_iterations=80):
    """
    Перевіряє, чи метод перестав покращувати результат.

    Але ця перевірка сама по собі не означає, що знайдено глобальний мінімум.
    Вона лише означає, що останні patience ітерацій майже не було покращення.
    """
    if len(history) < min_iterations:
        return False

    if len(history) < patience + 1:
        return False

    recent_best_values = [h[0] for h in history[-patience - 1:]]

    for i in range(1, len(recent_best_values)):
        if abs(recent_best_values[i] - recent_best_values[i - 1]) >= tolerance:
            return False

    return True


def should_stop(history, target_value=None, target_tolerance=1e-6,
                tolerance=1e-8, patience=30, min_iterations=80):
    if reached_target(history, target_value, target_tolerance):
        return True
    if target_value is None and stagnation_detected(history, tolerance, patience, min_iterations):
        return True

    return False


def analyze(history, best_point, elapsed_time, target_value=None):
    best_values = [h[0] for h in history]
    avg_values = [h[1] for h in history]

    delta_max = []
    delta_avg = []

    for i in range(1, len(history)):
        delta_max.append(abs(best_values[i] - best_values[i - 1]))
        delta_avg.append(abs(avg_values[i] - avg_values[i - 1]))

    convergence = best_values[0] - best_values[-1]

    error = None
    if target_value is not None:
        error = abs(best_values[-1] - target_value)

    return {
        "Best f(x)": float(best_values[-1]),
        "Збіжність": float(convergence),
        "Δmax": float(np.mean(delta_max)) if delta_max else 0.0,
        "Δavg": float(np.mean(delta_avg)) if delta_avg else 0.0,
        "Ітерації": len(history),
        "x": float(best_point[0]),
        "y": float(best_point[1]),
        "Похибка": float(error) if error is not None else None,
        "Час, с": float(elapsed_time)
    }


def plot_convergence(histories, title, run_type):
    plt.figure(figsize=(10, 6))

    for method_name, history in histories.items():
        best_values = [h[0] for h in history]
        plt.plot(best_values, label=method_name)

    plt.title(f"{run_type}: {title}")
    plt.xlabel("Кількість ітерацій")
    plt.ylabel("Найкраще значення функції f(x, y)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def print_table_with_summary(df):
    print(df.to_string(index=False))

    best_method = df.loc[df["Best f(x)"].idxmin(), "Метод"]
    fastest_method = df.loc[df["Ітерації"].idxmin(), "Метод"]
    most_stable_method = df.loc[df["Δmax"].idxmin(), "Метод"]

    print(f"\nНайточніший метод: {best_method}")
    print(f"Найшвидший метод: {fastest_method}")
    print(f"Найстабільніший за Δmax метод: {most_stable_method}")


# =========================================================
# Метод деформованих зірок
# =========================================================
def deformed_stars(
    func,
    bounds,
    pop_size=40,
    max_iterations=300,
    tolerance=1e-8,
    patience=30,
    min_iterations=80,
    target_value=None,
    target_tolerance=1e-6
):
    pop = generate_population(pop_size, bounds)
    history = []

    best, best_value = get_best_individual(pop, func)

    for t in range(max_iterations):
        center = np.mean(pop, axis=0)

        alpha = 0.35 * (1 - t / max_iterations)
        beta = 0.10 * (1 - t / max_iterations)

        for i in range(pop_size):
            direction_center = center - pop[i]
            direction_best = best - pop[i]
            noise = np.random.uniform(-1, 1, 2)

            new_point = (
                pop[i]
                + alpha * direction_center
                + 0.5 * alpha * direction_best
                + beta * noise
            )

            new_point = clip_point(new_point, bounds)

            if func(new_point[0], new_point[1]) < func(pop[i][0], pop[i][1]):
                pop[i] = new_point

        current_best, current_best_value = get_best_individual(pop, func)

        if current_best_value < best_value:
            best = current_best.copy()
            best_value = current_best_value

        worst_index = np.argmax(fitness(pop, func))
        pop[worst_index] = best.copy()

        values = fitness(pop, func)
        history.append((float(np.min(values)), float(np.mean(values))))

        if should_stop(history, target_value, target_tolerance, tolerance, patience, min_iterations):
            break

    return pop, history, best


# =========================================================
# Один крок МДБ Нелдера Міда
# =========================================================
def nelder_mead_step(
    simplex,
    func,
    bounds,
    alpha=1.0,
    gamma=2.0,
    rho=0.5,
    sigma=0.5
):
    simplex = sorted(simplex, key=lambda p: func(p[0], p[1]))

    best = simplex[0]
    good = simplex[1]
    worst = simplex[2]

    centroid = (best + good) / 2.0

    reflected = centroid + alpha * (centroid - worst)
    reflected = clip_point(reflected, bounds)

    f_best = func(best[0], best[1])
    f_good = func(good[0], good[1])
    f_worst = func(worst[0], worst[1])
    f_reflected = func(reflected[0], reflected[1])

    if f_best <= f_reflected < f_good:
        simplex[2] = reflected

    elif f_reflected < f_best:
        expanded = centroid + gamma * (reflected - centroid)
        expanded = clip_point(expanded, bounds)

        if func(expanded[0], expanded[1]) < f_reflected:
            simplex[2] = expanded
        else:
            simplex[2] = reflected

    else:
        contracted = centroid + rho * (worst - centroid)
        contracted = clip_point(contracted, bounds)

        if func(contracted[0], contracted[1]) < f_worst:
            simplex[2] = contracted
        else:
            simplex[1] = best + sigma * (simplex[1] - best)
            simplex[2] = best + sigma * (simplex[2] - best)

            simplex[1] = clip_point(simplex[1], bounds)
            simplex[2] = clip_point(simplex[2], bounds)

    simplex = sorted(simplex, key=lambda p: func(p[0], p[1]))
    return simplex


# =========================================================
# Метод деформованого багатогранника Нелдера Міда
# =========================================================
def mdb_nelder_mead(
    func,
    bounds,
    pop_size=40,
    max_iterations=300,
    tolerance=1e-8,
    patience=30,
    min_iterations=80,
    target_value=None,
    target_tolerance=1e-6
):
    lower, upper = bounds

    start = np.array([
        random.uniform(lower, upper),
        random.uniform(lower, upper)
    ], dtype=float)

    step = 0.15 * (upper - lower)

    simplex = [
        start,
        clip_point(start + np.array([step, 0.0]), bounds),
        clip_point(start + np.array([0.0, step]), bounds)
    ]

    history = []

    for _ in range(max_iterations):
        simplex = nelder_mead_step(simplex, func, bounds)

        values = fitness(simplex, func)
        history.append((float(np.min(values)), float(np.mean(values))))

        if should_stop(history, target_value, target_tolerance, tolerance, patience, min_iterations):
            break

    best, best_value = get_best_individual(simplex, func)
    return simplex, history, best


# =========================================================
# H алгоритм
# =========================================================
def h_algorithm(
    func,
    bounds,
    pop_size=40,
    max_iterations=300,
    tolerance=1e-8,
    patience=30,
    min_iterations=80,
    target_value=None,
    target_tolerance=1e-6
):
    pop = generate_population(pop_size, bounds)
    history = []

    best, best_value = get_best_individual(pop, func)

    for t in range(max_iterations):
        simplex = random.sample(pop, 3)
        simplex = [p.copy() for p in simplex]

        simplex = nelder_mead_step(simplex, func, bounds)

        local_scale = 0.20 * (1 - t / max_iterations) + 0.005

        candidate = simplex[0] + np.random.normal(0, local_scale, 2)
        candidate = clip_point(candidate, bounds)

        if func(candidate[0], candidate[1]) < func(simplex[0][0], simplex[0][1]):
            simplex[0] = candidate

        current_best, current_best_value = get_best_individual(simplex, func)

        if current_best_value < best_value:
            best = current_best.copy()
            best_value = current_best_value

        worst_index = np.argmax(fitness(pop, func))
        pop[worst_index] = best.copy()

        replace_indices = random.sample(range(pop_size), 3)

        for index, point in zip(replace_indices, simplex):
            if func(point[0], point[1]) < func(pop[index][0], pop[index][1]):
                pop[index] = point.copy()

        values = fitness(pop, func)
        history.append((float(np.min(values)), float(np.mean(values))))

        if should_stop(history, target_value, target_tolerance, tolerance, patience, min_iterations):
            break

    return pop, history, best


# =========================================================
# Поєднання МДБ та методу деформованих зірок
# =========================================================
def mdb_dz_combined(
    func,
    bounds,
    pop_size=40,
    max_iterations=300,
    tolerance=1e-8,
    patience=30,
    min_iterations=80,
    target_value=None,
    target_tolerance=1e-6
):
    lower, upper = bounds
    history = []

    start = np.array([
        random.uniform(lower, upper),
        random.uniform(lower, upper)
    ], dtype=float)

    step = 0.15 * (upper - lower)

    simplex = [
        start,
        clip_point(start + np.array([step, 0.0]), bounds),
        clip_point(start + np.array([0.0, step]), bounds)
    ]

    half = max_iterations // 2

    for _ in range(half):
        simplex = nelder_mead_step(simplex, func, bounds)

        values = fitness(simplex, func)
        history.append((float(np.min(values)), float(np.mean(values))))

        if should_stop(history, target_value, target_tolerance, tolerance, patience, min_iterations):
            break

    best, best_value = get_best_individual(simplex, func)

    pop = generate_population(pop_size, bounds)
    pop[0] = best.copy()

    remaining_iterations = max_iterations - len(history)

    for t in range(remaining_iterations):
        center = np.mean(pop, axis=0)

        alpha = 0.30 * (1 - t / max(1, remaining_iterations))
        beta = 0.08 * (1 - t / max(1, remaining_iterations))

        for i in range(pop_size):
            direction_center = center - pop[i]
            direction_best = best - pop[i]
            noise = np.random.uniform(-1, 1, 2)

            new_point = (
                pop[i]
                + alpha * direction_center
                + 0.5 * alpha * direction_best
                + beta * noise
            )

            new_point = clip_point(new_point, bounds)

            if func(new_point[0], new_point[1]) < func(pop[i][0], pop[i][1]):
                pop[i] = new_point

        current_best, current_best_value = get_best_individual(pop, func)

        if current_best_value < best_value:
            best = current_best.copy()
            best_value = current_best_value

        worst_index = np.argmax(fitness(pop, func))
        pop[worst_index] = best.copy()

        values = fitness(pop, func)
        history.append((float(np.min(values)), float(np.mean(values))))

        if should_stop(history, target_value, target_tolerance, tolerance, patience, min_iterations):
            break

    return pop, history, best


# =========================================================
# Одноразовий запуск
# =========================================================
def run_once(
    method,
    func,
    bounds,
    pop_size,
    max_iterations,
    tolerance,
    patience,
    min_iterations,
    target_value,
    target_tolerance
):
    start_time = time.time()

    pop, history, best_point = method(
        func,
        bounds,
        pop_size=pop_size,
        max_iterations=max_iterations,
        tolerance=tolerance,
        patience=patience,
        min_iterations=min_iterations,
        target_value=target_value,
        target_tolerance=target_tolerance
    )

    elapsed_time = time.time() - start_time

    return pop, history, best_point, elapsed_time


# =========================================================
# Багаторазовий запуск
# =========================================================
def run_with_restarts(
    method,
    func,
    bounds,
    runs,
    pop_size,
    max_iterations,
    tolerance,
    patience,
    min_iterations,
    target_value,
    target_tolerance
):
    best_overall_value = float("inf")
    best_pop = None
    best_history = None
    best_point = None
    best_time = None

    for _ in range(runs):
        pop, history, point, elapsed_time = run_once(
            method,
            func,
            bounds,
            pop_size,
            max_iterations,
            tolerance,
            patience,
            min_iterations,
            target_value,
            target_tolerance
        )

        value = func(point[0], point[1])

        if value < best_overall_value:
            best_overall_value = value
            best_pop = pop
            best_history = history
            best_point = point
            best_time = elapsed_time

    return best_pop, best_history, best_point, best_time


# =========================================================
# Основний запуск програми
# =========================================================
if __name__ == "__main__":

    functions = {
        "Функція Гольдштейна-Прайса": {
            "func": goldstein_price,
            "bounds": (-2, 2),
            "target": 3.0
        },
        "Функція Бута": {
            "func": booth,
            "bounds": (-10, 10),
            "target": 0.0
        },
        "Таблична функція Хольдера": {
            "func": holder_table,
            "bounds": (-10, 10),
            "target": -19.2085
        }
    }

    methods = {
        "Метод деформованих зірок": deformed_stars,
        "МДБ Нелдера-Міда": mdb_nelder_mead,
        "H-алгоритм": h_algorithm,
        "Поєднання МДБ-ДЗ": mdb_dz_combined
    }

    pop_size = 40
    max_iterations = 300
    tolerance = 1e-8
    patience = 30
    min_iterations = 80
    target_tolerance = 1e-4
    runs = 10

    # =====================================================
    # Одноразовий запуск
    # =====================================================
    print("\n============================================================")
    print("ОДНОРАЗОВИЙ ЗАПУСК")
    print("============================================================")

    for function_name, data in functions.items():
        func = data["func"]
        bounds = data["bounds"]
        target_value = data["target"]

        print("\n------------------------------------------------------------")
        print(f"Функція: {function_name}")
        print("------------------------------------------------------------")

        histories = {}
        table_rows = []

        for method_name, method in methods.items():
            pop, history, best_point, elapsed_time = run_once(
                method,
                func,
                bounds,
                pop_size,
                max_iterations,
                tolerance,
                patience,
                min_iterations,
                target_value,
                target_tolerance
            )

            metrics = analyze(history, best_point, elapsed_time, target_value)
            histories[method_name] = history

            table_rows.append({
                "Метод": method_name,
                "Best f(x)": round(metrics["Best f(x)"], 10),
                "Похибка": round(metrics["Похибка"], 10),
                "Збіжність": round(metrics["Збіжність"], 10),
                "Δmax": round(metrics["Δmax"], 10),
                "Δavg": round(metrics["Δavg"], 10),
                "Ітерації": metrics["Ітерації"],
                "x": round(metrics["x"], 6),
                "y": round(metrics["y"], 6),
                "Час, с": round(metrics["Час, с"], 6)
            })

        df = pd.DataFrame(table_rows)

        print("\nТаблиця порівняння методів:")
        print_table_with_summary(df)

        plot_convergence(
            histories,
            function_name,
            "Одноразовий запуск"
        )

    # =====================================================
    # Багаторазовий запуск
    # =====================================================
    print("\n============================================================")
    print("БАГАТОРАЗОВИЙ ЗАПУСК")
    print("============================================================")

    for function_name, data in functions.items():
        func = data["func"]
        bounds = data["bounds"]
        target_value = data["target"]

        print("\n------------------------------------------------------------")
        print(f"Функція: {function_name}")
        print("------------------------------------------------------------")

        histories = {}
        table_rows = []

        for method_name, method in methods.items():
            pop, history, best_point, elapsed_time = run_with_restarts(
                method,
                func,
                bounds,
                runs,
                pop_size,
                max_iterations,
                tolerance,
                patience,
                min_iterations,
                target_value,
                target_tolerance
            )

            metrics = analyze(history, best_point, elapsed_time, target_value)
            histories[method_name] = history

            table_rows.append({
                "Метод": method_name,
                "Best f(x)": round(metrics["Best f(x)"], 10),
                "Похибка": round(metrics["Похибка"], 10),
                "Збіжність": round(metrics["Збіжність"], 10),
                "Δmax": round(metrics["Δmax"], 10),
                "Δavg": round(metrics["Δavg"], 10),
                "Ітерації": metrics["Ітерації"],
                "x": round(metrics["x"], 6),
                "y": round(metrics["y"], 6),
                "Час, с": round(metrics["Час, с"], 6)
            })

        df = pd.DataFrame(table_rows)

        print("\nТаблиця порівняння методів:")
        print_table_with_summary(df)

        plot_convergence(
            histories,
            function_name,
            "Багаторазовий запуск"
        )