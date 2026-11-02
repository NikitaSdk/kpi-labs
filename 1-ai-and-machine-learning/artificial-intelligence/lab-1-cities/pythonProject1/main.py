import tkinter as tk
from tkinter import messagebox
import random
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


current_canvas = None

def create_widgets(root):
    tk.Label(root, text="Кількість ітерацій:").grid(row=0, column=0)
    iterations_entry = tk.Entry(root)
    iterations_entry.grid(row=0, column=1)
    iterations_entry.insert(0, "100")

    tk.Label(root, text="Кількість міст:").grid(row=1, column=0)
    cities_entry = tk.Entry(root)
    cities_entry.grid(row=1, column=1)
    cities_entry.insert(0, "40")

    tk.Label(root, text="Відсоток мутації:").grid(row=2, column=0)
    mutation_entry = tk.Entry(root)
    mutation_entry.grid(row=2, column=1)
    mutation_entry.insert(0, "5")

    tk.Label(root, text="Розмір популяції:").grid(row=3, column=0)
    population_size_entry = tk.Entry(root)
    population_size_entry.grid(row=3, column=1)
    population_size_entry.insert(0, "100")

    start_button = tk.Button(root, text="Start",
                             command=lambda: start_algorithm(root, iterations_entry, cities_entry, mutation_entry,
                                                             population_size_entry))
    start_button.grid(row=4, columnspan=2)

def generate_cities(cities_num):
    cities = []
    for i in range(1, cities_num + 1):
        city = {
            'id': i,
            'pos': (random.randint(0, 100), random.randint(0, 100))
        }
        cities.append(city)
    return cities

def generate_population(population_size, cities):
    population = []
    for _ in range(population_size):
        individual = {
            'route': random.sample(cities, len(cities)),
            'distance': 0
        }
        population.append(individual)
    return population

def calculate_distance(city1, city2):
    x1, y1 = city1['pos']
    x2, y2 = city2['pos']
    delta_x = x2 - x1
    delta_y = y2 - y1
    return math.sqrt(delta_x ** 2 + delta_y ** 2)

def evaluate_route(individual):
    total_distance = 0
    for i in range(len(individual['route']) - 1):
        total_distance += calculate_distance(individual['route'][i], individual['route'][i + 1])
    total_distance += calculate_distance(individual['route'][-1], individual['route'][0])
    individual['distance'] = total_distance
    return total_distance

def select_parents(population):
    population.sort(key=lambda x: x['distance'])
    return population[0], population[-1]

def crossover(parent1, parent2, num_points=3):
    size = len(parent1['route'])
    points = sorted(random.sample(range(size), num_points))

    child1, child2 = [], []
    swap = False
    for i in range(size):
        if i in points:
            swap = not swap
        if swap:
            child1.append(parent2['route'][i])
            child2.append(parent1['route'][i])
        else:
            child1.append(parent1['route'][i])
            child2.append(parent2['route'][i])

    child1 = resolve_duplicates(child1, parent1['route'])
    child2 = resolve_duplicates(child2, parent2['route'])
    return {'route': child1, 'distance': 0}, {'route': child2, 'distance': 0}

def resolve_duplicates(child, parent):
    seen = set()
    new_child = []
    for city in child:

        if city['id'] not in seen:
            new_child.append(city)
            seen.add(city['id'])
        else:
            for p_city in parent:
                if p_city['id'] not in seen:
                    new_child.append(p_city)
                    seen.add(p_city['id'])
                    break
    return new_child


def mutate(individual, mutation_rate):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(individual['route'])), 2)
        individual['route'][i], individual['route'][j] = individual['route'][j], individual['route'][i]


def start_algorithm(root, iterations_entry, cities_entry, mutation_entry, population_size_entry):
    try:
        iterations = int(iterations_entry.get())
        cities_num = int(cities_entry.get())
        mutation_rate = float(mutation_entry.get()) / 100
        population_size = int(population_size_entry.get())

        if cities_num <= 0 or iterations <= 0 or mutation_rate < 0 or mutation_rate > 1 or population_size <= 0:
            raise ValueError

        print(f"Running algorithm with {iterations} iterations, {cities_num} cities, mutation rate: {mutation_rate}, population size: {population_size}")
        root.update()
        run_genetic_algorithm(root, cities_num, iterations, mutation_rate, population_size)

    except ValueError:
        messagebox.showerror("Помилка", "Будь ласка, введіть коректні значення.")

def run_genetic_algorithm(root, cities_num, iterations, mutation_rate, population_size):
    cities = generate_cities(cities_num)
    population = generate_population(population_size, cities)

    distance_history = []
    best_distance_history = []

    for individual in population:
        evaluate_route(individual)

    for _ in range(iterations):
        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = select_parents(population)
            child1, child2 = crossover(parent1, parent2)
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            evaluate_route(child1)
            evaluate_route(child2)
            new_population.append(child1)
            new_population.append(child2)

        population = sorted(new_population, key=lambda x: x['distance'])[:population_size]

        best_distance = population[0]['distance']
        distance_history.append(best_distance)
        best_distance_history.append(min(distance_history))

    best_route = population[0]
    plot_graph(root, cities, best_route, distance_history, best_distance_history)


def plot_graph(root, cities, best_route, distance_history, best_distance_history):
    global current_canvas

    if current_canvas is not None:
        current_canvas.get_tk_widget().destroy()

    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 3)
    ax3 = fig.add_subplot(1, 2, 2)

    for i in range(len(best_route['route']) - 1):
        city1 = best_route['route'][i]
        city2 = best_route['route'][i + 1]
        ax1.plot([city1['pos'][0], city2['pos'][0]], [city1['pos'][1], city2['pos'][1]], 'bo-')

    city1 = best_route['route'][-1]
    city2 = best_route['route'][0]
    ax1.plot([city1['pos'][0], city2['pos'][0]], [city1['pos'][1], city2['pos'][1]], 'bo-')

    start_city = best_route['route'][0]
    ax1.plot(start_city['pos'][0], start_city['pos'][1], 'ro', markersize=10)
    for city in cities:
        ax1.annotate(f"{city['id']}", (city['pos'][0], city['pos'][1]), textcoords="offset points", xytext=(0, 5), ha='center')
    ax1.set_title("Маршрут")

    ax2.plot(distance_history, color='green')
    ax2.set_xlabel("Ітерація")
    ax2.set_ylabel("Дистанція")
    ax2.set_title("Покращення дистанції")

    ax3.plot(best_distance_history, color='blue')
    ax3.set_xlabel("Ітерація")
    ax3.set_ylabel("Найкраща дистанція")
    ax3.set_title("Найкраща дистанція")

    plt.tight_layout(pad=2.0)
    plt.show()

    current_canvas = FigureCanvasTkAgg(fig, master=root)
    current_canvas.draw()
    current_canvas.get_tk_widget().grid(row=5, columnspan=2)



if __name__ == "__main__":
    root = tk.Tk()
    create_widgets(root)
    root.mainloop()
