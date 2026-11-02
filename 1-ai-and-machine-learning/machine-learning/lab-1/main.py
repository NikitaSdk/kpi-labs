import csv
import numpy as np
import matplotlib.pyplot as plt

# Функція для завантаження тренувальних даних із візуалізацією
def load_train_data(filename):
    with open(filename, 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader)
        data_x, data_y = [], []
        for row in csvreader:
            _, x, y = row
            data_x.append(float(x))
            data_y.append(float(y))
    plt.scatter(data_x, data_y, color='blue', label='Training Data')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Training Data Visualization')
    plt.legend()
    plt.show()
    return data_x, data_y

# Функція для завантаження тестових даних
def load_test_data(filename):
    with open(filename, 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader)
        data_x, data_y = [], []
        for row in csvreader:
            _, x, y = row
            data_x.append(float(x))
            data_y.append(float(y))
    return data_x, data_y

# Функція для розрахунку середньоквадратичної помилки
def MSQ_ERROR(y, y_pred):
    return np.mean((y - y_pred) ** 2)


# Функція для тренування моделі лінійної регресії за допомогою градієнтного спуску
def gradient_d(x, y, learning_rate=0.05, epochs=1000, aim=0.00001):
    b0, b1 = 0, 0
    n = len(x)
    last_loss = None
    for epoch in range(epochs):
        y_pred = b1 * x + b0
        loss = MSQ_ERROR(y, y_pred)

        print(f'Epoch {epoch + 1}/{epochs}: Loss={loss}, b1(weight)={b1}, b0(intercept)={b0}')

        b1_gradient = (-2 / n) * np.sum(x * (y - y_pred))
        b0_gradient = (-2 / n) * np.sum(y - y_pred)
        b1 -= learning_rate * b1_gradient
        b0 -= learning_rate * b0_gradient

        if last_loss is not None and abs(last_loss - loss) < aim:
            print(f"Training stopped at epoch {epoch + 1}. Loss change {abs(last_loss - loss)} is less than aim {aim}.")
            break
        last_loss = loss

    return b1, b0

# Функція для візуалізації результатів
def show_res(x_train, y_train, x_test, y_test, b1, b0):
    x = np.concatenate((x_train, x_test))
    y = np.concatenate((y_train, y_test))
    y_pred = b1 * x + b0
    plt.figure(figsize=(10, 6))
    plt.scatter(x_train, y_train, label='Train Data', color='blue')
    plt.scatter(x_test, y_test, label='Test Data', color='red')
    plt.plot(x, y_pred, label='Regression Line', color='green')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Linear Regression')
    plt.legend()
    plt.grid(True)
    plt.show()

# Завантаження та візуалізація тренувальних даних
x_train, y_train = load_train_data('lab_1_train.csv')

#Завантаження тестових даних
x_test, y_test = load_test_data('lab_1_test.csv')

# Тренування моделі та оцінка точності на тестових даних
b1, b0 = gradient_d(np.array(x_train), np.array(y_train), learning_rate=0.05, epochs=1000, aim=0.00001)
y_pred_test = b1 * np.array(x_test) + b0
test_loss = MSQ_ERROR(np.array(y_test), y_pred_test)
print(f'Test Loss: {test_loss}')

# Візуалізація результатів
show_res(x_train, y_train, x_test, y_test, b1, b0)
