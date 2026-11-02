import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from scipy.optimize import minimize_scalar


def goldstein_price(x, y):
    a = 1 + (x + y + 1) ** 2 * (
        19 - 14 * x + 3 * x ** 2 - 14 * y + 6 * x * y + 3 * y ** 2
    )
    b = 30 + (2 * x - 3 * y) ** 2 * (
        18 - 32 * x + 12 * x ** 2 + 48 * y - 36 * x * y + 27 * y ** 2
    )
    return a * b


def booth(x, y):
    return (x + 2 * y - 7) ** 2 + (2 * x + y - 5) ** 2


def holder_table(x, y):
    return -np.abs(
        np.sin(x) * np.cos(y) *
        np.exp(np.abs(1 - np.sqrt(x ** 2 + y ** 2) / np.pi))
    )


def numerical_gradient(func, point, h=1e-5):
    x, y = point

    df_dx = (func(x + h, y) - func(x - h, y)) / (2 * h)
    df_dy = (func(x, y + h) - func(x, y - h)) / (2 * h)

    return np.array([df_dx, df_dy], dtype=float)



def project_to_bounds(point, bounds):
    x = np.clip(point[0], bounds[0][0], bounds[0][1])
    y = np.clip(point[1], bounds[1][0], bounds[1][1])
    return np.array([x, y], dtype=float)


def get_values_by_iterations(func, trajectory):
    return np.array([func(p[0], p[1]) for p in trajectory])



def gradient_descent_fixed(
        func,
        start_point,
        bounds,
        alpha=0.01,
        max_iter=1000,
        eps=1e-6
):
    start_time = time.time()

    point = np.array(start_point, dtype=float)
    trajectory = [point.copy()]

    for _ in range(max_iter):
        grad = numerical_gradient(func, point)
        grad_norm = np.linalg.norm(grad)

        if grad_norm < eps:
            break

        new_point = point - alpha * grad
        new_point = project_to_bounds(new_point, bounds)

        if np.allclose(new_point, point, atol=1e-12):
            break

        point = new_point
        trajectory.append(point.copy())

    elapsed_time = time.time() - start_time
    final_grad = numerical_gradient(func, point)

    return {
        "point": point,
        "value": func(point[0], point[1]),
        "iterations": len(trajectory) - 1,
        "trajectory": np.array(trajectory),
        "grad_norm": np.linalg.norm(final_grad),
        "time": elapsed_time
    }



def gradient_descent_adaptive(
        func,
        start_point,
        bounds,
        alpha=0.1,
        beta=0.5,
        max_iter=1000,
        eps=1e-6
):
    start_time = time.time()

    point = np.array(start_point, dtype=float)
    trajectory = [point.copy()]

    for _ in range(max_iter):
        grad = numerical_gradient(func, point)
        grad_norm = np.linalg.norm(grad)

        if grad_norm < eps:
            break

        current_value = func(point[0], point[1])
        current_alpha = alpha
        improved = False

        while current_alpha > 1e-12:
            new_point = point - current_alpha * grad
            new_point = project_to_bounds(new_point, bounds)

            new_value = func(new_point[0], new_point[1])

            if new_value < current_value:
                point = new_point
                trajectory.append(point.copy())
                alpha = current_alpha
                improved = True
                break

            current_alpha *= beta

        if not improved:
            break

    elapsed_time = time.time() - start_time
    final_grad = numerical_gradient(func, point)

    return {
        "point": point,
        "value": func(point[0], point[1]),
        "iterations": len(trajectory) - 1,
        "trajectory": np.array(trajectory),
        "grad_norm": np.linalg.norm(final_grad),
        "time": elapsed_time
    }



def steepest_descent(
        func,
        start_point,
        bounds,
        alpha_max=0.5,
        max_iter=1000,
        eps=1e-6
):
    start_time = time.time()

    point = np.array(start_point, dtype=float)
    trajectory = [point.copy()]

    for _ in range(max_iter):
        grad = numerical_gradient(func, point)
        grad_norm = np.linalg.norm(grad)

        if grad_norm < eps:
            break

        direction = -grad / grad_norm
        current_value = func(point[0], point[1])

        def line_function(alpha):
            test_point = point + alpha * direction
            test_point = project_to_bounds(test_point, bounds)
            return func(test_point[0], test_point[1])

        result = minimize_scalar(
            line_function,
            bounds=(0, alpha_max),
            method="bounded"
        )

        alpha_opt = result.x

        new_point = point + alpha_opt * direction
        new_point = project_to_bounds(new_point, bounds)
        new_value = func(new_point[0], new_point[1])

        if new_value >= current_value:
            improved = False
            alpha_temp = alpha_max

            while alpha_temp > 1e-12:
                test_point = point + alpha_temp * direction
                test_point = project_to_bounds(test_point, bounds)
                test_value = func(test_point[0], test_point[1])

                if test_value < current_value:
                    new_point = test_point
                    new_value = test_value
                    improved = True
                    break

                alpha_temp *= 0.5

            if not improved:
                break

        point = new_point
        trajectory.append(point.copy())

    elapsed_time = time.time() - start_time
    final_grad = numerical_gradient(func, point)

    return {
        "point": point,
        "value": func(point[0], point[1]),
        "iterations": len(trajectory) - 1,
        "trajectory": np.array(trajectory),
        "grad_norm": np.linalg.norm(final_grad),
        "time": elapsed_time
    }



problems = {
    "Гольдштейн-Прайс": {
        "func": goldstein_price,
        "bounds": [(-2, 2), (-2, 2)],
        "start": np.array([0.8, -0.4]),
        "known_min_text": "(0, -1), f = 3",
        "known_min_value": 3.0,
        "alpha_fixed": 1e-5,
        "alpha_adaptive": 0.01,
        "alpha_max": 0.5
    },

    "Бут": {
        "func": booth,
        "bounds": [(-10, 10), (-10, 10)],
        "start": np.array([-8.0, 8.0]),
        "known_min_text": "(1, 3), f = 0",
        "known_min_value": 0.0,
        "alpha_fixed": 0.05,
        "alpha_adaptive": 0.1,
        "alpha_max": 0.5
    },

    "Хольдер": {
        "func": holder_table,
        "bounds": [(-10, 10), (-10, 10)],
        "start": np.array([7.0, 8.0]),
        "known_min_text": "(±8.055, ±9.665), f ≈ -19.2085",
        "known_min_value": -19.2085,
        "alpha_fixed": 0.01,
        "alpha_adaptive": 0.1,
        "alpha_max": 0.5
    }
}


all_results = {}
all_rows = []

for problem_name, problem_data in problems.items():
    func = problem_data["func"]
    bounds = problem_data["bounds"]
    start = problem_data["start"]
    known_min_value = problem_data["known_min_value"]

    results = {
        "Фіксований крок": gradient_descent_fixed(
            func=func,
            start_point=start,
            bounds=bounds,
            alpha=problem_data["alpha_fixed"],
            max_iter=1000,
            eps=1e-6
        ),

        "Адаптивний крок": gradient_descent_adaptive(
            func=func,
            start_point=start,
            bounds=bounds,
            alpha=problem_data["alpha_adaptive"],
            beta=0.5,
            max_iter=1000,
            eps=1e-6
        ),

        "Найшвидший спуск": steepest_descent(
            func=func,
            start_point=start,
            bounds=bounds,
            alpha_max=problem_data["alpha_max"],
            max_iter=1000,
            eps=1e-6
        )
    }

    all_results[problem_name] = results

    for method_name, result in results.items():
        point = result["point"]
        value = result["value"]
        error = abs(value - known_min_value)

        all_rows.append({
            "Функція": problem_name,
            "Метод": method_name,
            "Старт": f"({start[0]:.2f}; {start[1]:.2f})",
            "x": round(point[0], 5),
            "y": round(point[1], 5),
            "f(x,y)": round(value, 6),
            "Похибка": round(error, 6),
            "Ітер.": result["iterations"],
            "||grad||": round(result["grad_norm"], 6),
            "Час, с": round(result["time"], 5),
            "Відомий мінімум": problem_data["known_min_text"]
        })

results_df = pd.DataFrame(all_rows)



pd.set_option("display.max_columns", None)
pd.set_option("display.width", 180)

compact_columns = [
    "Метод",
    "Старт",
    "x",
    "y",
    "f(x,y)",
    "Похибка",
    "Ітер.",
    "||grad||",
    "Час, с"
]

for problem_name in problems.keys():
    print("\n" + "=" * 110)
    print(f"РЕЗУЛЬТАТИ ДЛЯ ФУНКЦІЇ: {problem_name}")
    print(f"Відомий мінімум: {problems[problem_name]['known_min_text']}")
    print("=" * 110)

    function_table = (
        results_df[results_df["Функція"] == problem_name][compact_columns]
        .reset_index(drop=True)
    )

    print(function_table.to_string(index=False))



print("\n" + "=" * 135)
print("ЗАГАЛЬНА ПОРІВНЯЛЬНА ТАБЛИЦЯ")
print("=" * 135)

general_columns = [
    "Функція",
    "Метод",
    "x",
    "y",
    "f(x,y)",
    "Похибка",
    "Ітер.",
    "||grad||",
    "Час, с"
]

print(results_df[general_columns].to_string(index=False))



def plot_convergence(problem_name, problem_data, results):
    func = problem_data["func"]

    plt.figure(figsize=(9, 6))

    for method_name, result in results.items():
        trajectory = result["trajectory"]
        values = get_values_by_iterations(func, trajectory)

        best_values = np.minimum.accumulate(values)
        iterations = np.arange(len(best_values))

        plt.plot(
            iterations,
            best_values,
            linewidth=2,
            label=method_name
        )

    plt.title(f"Збіжність градієнтних методів: {problem_name}")
    plt.xlabel("Ітерація")
    plt.ylabel("Найкраще значення функції")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()



for problem_name, problem_data in problems.items():
    plot_convergence(
        problem_name=problem_name,
        problem_data=problem_data,
        results=all_results[problem_name]
    )



results_df.to_csv("results_gradient_methods.csv", index=False, encoding="utf-8-sig")

print("\nФайл збережено: results_gradient_methods.csv")