import numpy as np
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


def sgn(x):
    return np.where(x >= 0, 1, -1)


class HopfieldNetwork:
    def __init__(self, size):
        self.size = size
        self.weights = np.zeros((size, size))

    def train_patterns(self, patterns):
        self.weights = np.zeros((self.size, self.size))  # Скидання ваг
        for pattern in patterns:
            pattern = pattern.reshape(self.size, 1)
            self.weights += np.dot(pattern, pattern.T)
        np.fill_diagonal(self.weights, 0)

    def recall(self, input_pattern, max_iterations=10):
        pattern = input_pattern.copy()
        for _ in range(max_iterations):
            new_pattern = sgn(np.dot(self.weights, pattern))
            if np.array_equal(new_pattern, pattern):
                break
            pattern = new_pattern
        return pattern


def preproc_pattern(grid):
    return np.where(np.array(grid).flatten() > 0, 1, -1)


def draw_grid(canvas, grid, size):
    canvas.delete("all")
    for i in range(size):
        for j in range(size):
            color = "black" if grid[i][j] == 1 else "white"
            canvas.create_rectangle(
                j * 30, i * 30, (j + 1) * 30, (i + 1) * 30,
                fill=color, outline="black"
            )


def cell_select(event, grid, canvas, rectangles, size):
    x, y = event.x // 30, event.y // 30
    if 0 <= x < size and 0 <= y < size:
        grid[y][x] = 1 if grid[y][x] == -1 else -1
        canvas.itemconfig(rectangles[y][x], fill="black" if grid[y][x] == 1 else "white")


def mouse_select(event, grid, canvas, rectangles, size):
    x, y = event.x // 30, event.y // 30
    if 0 <= x < size and 0 <= y < size:
        grid[y][x] = 1
        canvas.itemconfig(rectangles[y][x], fill="black")


def pattern_edit(size, canvas, editable=True):
    grid = [[-1 for _ in range(size)] for _ in range(size)]
    rectangles = [[None for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            rectangles[i][j] = canvas.create_rectangle(
                j * 30, i * 30, (j + 1) * 30, (i + 1) * 30,
                fill="white", outline="black"
            )
    if editable:
        canvas.bind("<Button-1>", lambda event: cell_select(event, grid, canvas, rectangles, size))
        canvas.bind("<B1-Motion>", lambda event: mouse_select(event, grid, canvas, rectangles, size))
    return grid, rectangles


def grid_to_image(grid, size):
    img = Image.new("RGB", (size, size), "white")
    pixels = img.load()
    for i in range(size):
        for j in range(size):
            if grid[i][j] == 1:
                pixels[j, i] = (0, 0, 0)
    img = img.resize((size * 30, size * 30))
    return img


def display_image(canvas, image):
    canvas.delete("all")
    tk_image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
    canvas.image = tk_image


def draw_training_sample(frame, grid, size):
    canvas = tk.Canvas(frame, width=size * 30, height=size * 30, bg="white")
    canvas.pack(side=tk.LEFT, padx=5)
    for i in range(size):
        for j in range(size):
            color = "black" if grid[i][j] == 1 else "white"
            canvas.create_rectangle(
                j * 30, i * 30, (j + 1) * 30, (i + 1) * 30,
                fill=color, outline="black"
            )
    return canvas

def draw_training_sample_with_label(frame, grid, size, label_text):

    sample_frame = tk.Frame(frame)
    sample_frame.pack(side=tk.LEFT, padx=5)

    canvas = tk.Canvas(sample_frame, width=size * 30, height=size * 30, bg="white")
    canvas.pack()

    for i in range(size):
        for j in range(size):
            color = "black" if grid[i][j] == 1 else "white"
            canvas.create_rectangle(
                j * 30, i * 30, (j + 1) * 30, (i + 1) * 30,
                fill=color, outline="black"
            )

    label = tk.Label(sample_frame, text=label_text, font=("Helvetica", 10))
    label.pack()


def add_trainpat():

    pattern = preproc_pattern(training_grid)  # Перетворення сітки у вектор
    patterns.append(pattern)
    hopfield_net.train_patterns(np.array(patterns))  # Тренування мережі

    sample_index = len(patterns)
    draw_training_sample_with_label(training_patterns_frame, training_grid, size, f"Еталон {sample_index}")

    clear_train_field()
    messagebox.showinfo("Інформація", "Зразок додано!", parent=root)


def clear_train_field():

    for i in range(size):
        for j in range(size):
            training_grid[i][j] = -1
            left_canvas.itemconfig(training_rectangles[i][j], fill="white")


def clear_rec_field():

    for i in range(size):
        for j in range(size):
            recognizing_grid[i][j] = -1
            middle_canvas.itemconfig(recognizing_rectangles[i][j], fill="white")


def clear_train_set():
    patterns.clear()
    hopfield_net.weights = np.zeros((size * size, size * size))
    for widget in training_patterns_frame.winfo_children():
        widget.destroy()
    messagebox.showinfo("Інформація", "Тренувальний набір очищено!", parent=root)


def rec_pattern():
    if not patterns:
        messagebox.showwarning("Попередження", "Немає доступних тренувальних зразків!", parent=root)
        return

    noisy_pattern = preproc_pattern(recognizing_grid)
    recovered_pattern = hopfield_net.recall(noisy_pattern)

    draw_grid(right_canvas, recovered_pattern.reshape(size, size).tolist(), size)



def initialize_training_samples_with_labels(frame):
    initial_samples = [

        [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
         [-1, -1, -1,  1,  1,  1,  1,  1, -1, -1],
         [-1, -1, -1,  1, -1, -1, -1,  1, -1, -1],
         [-1, -1, -1,  1, -1, -1, -1,  1, -1, -1],
         [-1, -1, -1,  1,  1,  1,  1,  1, -1, -1],
         [-1, -1, -1, -1, -1, -1,  1,  1, -1, -1],
         [-1, -1, -1, -1, -1,  1, -1,  1, -1, -1],
         [-1, -1, -1, -1,  1, -1, -1,  1, -1, -1],
         [-1, -1, -1,  1, -1, -1, -1,  1, -1, -1],
         [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]],

        [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
         [-1,  1,  1, -1, -1, -1, -1,  1,  1, -1],
         [-1,  1, -1,  1, -1, -1,  1, -1,  1, -1],
         [-1,  1, -1, -1,  1,  1, -1, -1,  1, -1],
         [-1,  1, -1, -1, -1, -1, -1, -1,  1, -1],
         [-1,  1, -1, -1, -1, -1, -1, -1,  1, -1],
         [-1,  1, -1, -1, -1, -1, -1, -1,  1, -1],
         [-1,  1, -1, -1, -1, -1, -1, -1,  1, -1],
         [-1,  1, -1, -1, -1, -1, -1, -1,  1, -1],
         [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]],

        [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
         [-1,  1,  1,  1,  1,  1,  1, -1, -1, -1],
         [-1,  1, -1, -1, -1, -1, -1,  1, -1, -1],
         [-1,  1, -1, -1, -1, -1, -1,  1, -1, -1],
         [-1,  1,  1,  1,  1,  1,  1, -1, -1, -1],
         [-1,  1, -1, -1, -1, -1, -1,  1, -1, -1],
         [-1,  1, -1, -1, -1, -1, -1,  1, -1, -1],
         [-1,  1, -1, -1, -1, -1, -1,  1, -1, -1],
         [-1,  1,  1,  1,  1,  1,  1, -1, -1, -1],
         [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]
    ]

    for idx, sample in enumerate(initial_samples):
        padded_sample = preproc_pattern(sample)
        patterns.append(padded_sample)
        hopfield_net.train_patterns(np.array(patterns))
        draw_training_sample_with_label(frame, sample, size, f"Еталон {idx + 1}")



def main():
    global size, hopfield_net, patterns, training_grid, recognizing_grid, training_patterns_frame, root, left_canvas, training_rectangles, middle_canvas, recognizing_rectangles, right_canvas

    root = tk.Tk()
    root.title("Мережа Хопфілда")

    size = 10
    hopfield_net = HopfieldNetwork(size * size)
    patterns = []

    left_canvas = tk.Canvas(root, width=size * 30, height=size * 30, bg="white")
    left_canvas.grid(row=2, column=0, padx=10, pady=10)
    training_grid, training_rectangles = pattern_edit(size, left_canvas, editable=True)


    middle_canvas = tk.Canvas(root, width=size * 30, height=size * 30, bg="white")
    middle_canvas.grid(row=2, column=1, padx=10, pady=10)
    recognizing_grid, recognizing_rectangles = pattern_edit(size, middle_canvas, editable=True)


    right_canvas = tk.Canvas(root, width=size * 30, height=size * 30, bg="white")
    right_canvas.grid(row=2, column=2, padx=10, pady=10)


    tk.Label(root, text="Еталонний зразок", font=("Helvetica", 12)).grid(row=1, column=0)
    tk.Label(root, text="Зразок для розпізнавання", font=("Helvetica", 12)).grid(row=1, column=1)
    tk.Label(root, text="Розпізнаний зразок", font=("Helvetica", 12)).grid(row=1, column=2)


    tk.Label(root, text="Набір еталоних зразків", font=("Helvetica", 12)).grid(row=3, column=0, columnspan=3)


    training_patterns_frame = tk.Frame(root)
    training_patterns_frame.grid(row=4, column=0, columnspan=3, pady=10)


    initialize_training_samples_with_labels(training_patterns_frame)


    buttons_frame = tk.Frame(root)
    buttons_frame.grid(row=5, column=0, rowspan=3, padx=10, pady=10)


    tk.Button(buttons_frame, text="Додати зразок", command=add_trainpat, width=30, height=2).grid(row=0, column=0, pady=5)
    tk.Button(buttons_frame, text="Очистити зразок ", command=clear_train_field, width=30, height=2).grid(row=1, column=0, pady=5)
    tk.Button(buttons_frame, text="Очистити еталонні зразки", command=clear_train_set, width=30, height=2).grid(row=2, column=0, pady=5)
    tk.Button(root, text="Очистити зразок для розпізнавання", command=clear_rec_field, width=30, height=2).grid(row=5, column=1, pady=10)
    tk.Button(root, text="Розпізнати", command=rec_pattern, width=30, height=2).grid(row=6, column=1, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
