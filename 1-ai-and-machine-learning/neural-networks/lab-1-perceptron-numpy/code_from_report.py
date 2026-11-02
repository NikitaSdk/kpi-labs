# Code extracted from the lab report (report.pdf)

# ---- fragment 1 ----
import numpy as np
import matplotlib.pyplot as plt

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def derSigmoid(x):
    return x * (1 - x)

def tanh(x):
    return np.tanh(x)

def derTanh(x):
    return 1 - np.tanh(x) ** 2

def relu(x):
    return np.maximum(0, x)

def derRelu(x):
    return np.where(x > 0, 1, 0)

def my_func(x):
    return np.sin(x)

def derMy_func(x):
    return np.cos(x)

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

def calculate_accuracy(predictions, Y):
    preds = (predictions > 0.5).astype(int)  # Округлення до 0 або 1
    return np.mean(preds == Y)  # Підрахунок відсотка правильних прогнозів

def train_network(activation_func, activation_derivative, epochs=10000, lr=0.1):
    np.random.seed(42)
    input_dim = 2
    hidden_dim = 4
    output_dim = 1

    W1 = np.random.randn(input_dim, hidden_dim) #ваги (коеф)
    b1 = np.zeros((1, hidden_dim)) #зміщення
    W2 = np.random.randn(hidden_dim, output_dim)
    b2 = np.zeros((1, output_dim))

    losses = []
    accuracies = []  # Додаємо список для збереження точності

    for epoch in range(epochs):
        Z1 = np.dot(X, W1) + b1
        A1 = activation_func(Z1)
        Z2 = np.dot(A1, W2) + b2
        A2 = sigmoid(Z2)

        loss = np.mean((y - A2) ** 2)
        losses.append(loss)

        dA2 = (A2 - y) * derSigmoid(A2)
        dW2 = np.dot(A1.T, dA2)
        db2 = np.sum(dA2, axis=0, keepdims=True)

        dA1 = np.dot(dA2, W2.T) * activation_derivative(A1)
        dW1 = np.dot(X.T, dA1)
        db1 = np.sum(dA1, axis=0, keepdims=True)

        W2 -= lr * dW2
        b2 -= lr * db2
        W1 -= lr * dW1
        b1 -= lr * db1

        # Кожні 1000 епох виводимо втрати та точність
        if epoch % 1000 == 0:
            predictions = (A2 > 0.5).astype(int)  # Округлення виходу
            acc = calculate_accuracy(predictions, y)  # Обчислення точності
            accuracies.append(acc)
            print(f"Epoch {epoch}, Loss: {loss:.4f}, Accuracy: {acc:.4f}")

    return W1, b1, W2, b2, losses, accuracies
activation_functions = {
    "Sigmoid": (sigmoid, derSigmoid),
    "Tanh": (tanh, derTanh),
    "ReLU": (relu, derRelu),
    "Custom (Sin)": (my_func, derMy_func)
}

results = {}
for name, (act_func, act_deriv) in activation_functions.items():
    print(f"\n--- Навчання з функцією активації: {name} ---")
    W1, b1, W2, b2, losses, accuracies = train_network(act_func, act_deriv)
    results[name] = {'W1': W1, 'b1': b1, 'W2': W2, 'b2': b2, 'losses': losses, 'accuracies': accuracies}
    print(f"Фінальна втрата для {name}: {losses[-1]:.5f}")

def predict(X, W1, b1, W2, b2, activation_func):
    Z1 = np.dot(X, W1) + b1
    A1 = activation_func(Z1)
    Z2 = np.dot(A1, W2) + b2
    A2 = sigmoid(Z2)
    return (A2 > 0.5).astype(int)

def plot_decision_boundary(X, y, W1, b1, W2, b2, activation_func):
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100), np.linspace(y_min, y_max, 100))
    Z = predict(np.c_[xx.ravel(), yy.ravel()], W1, b1, W2, b2, activation_func)
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, alpha=0.3)
    plt.scatter(X[:, 0], X[:, 1], c=y.flatten(), edgecolors='k', cmap=plt.cm.Spectral)
    plt.title(f"Межа прийняття рішення для {activation_func.__name__}")
    plt.show()

# Візуалізація для кожної функції активації
for name, res in results.items():
    print(f"\n--- Візуалізація межі прийняття рішення для {name} ---")
    plot_decision_boundary(X, y, res['W1'], res['b1'], res['W2'], res['b2'], activation_functions[name][0])

# Візуалізація графіків втрат для кожної активаційної функції
for name, res in results.items():
    plt.figure(figsize=(6, 4))
    plt.plot(res['losses'], label=f"{name}")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.title(f"Зміна втрат під час навчання ({name})")
    plt.legend()
    plt.grid()
    plt.show()

# ---- fragment 2 ----
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def derSigmoid(x):
    return x * (1 - x)

def tanh(x):
    return np.tanh(x)

def derTanh(x):
    return 1 - np.tanh(x) ** 2

def relu(x):
    return np.maximum(0, x)

def derRelu(x):
    return np.where(x > 0, 1, 0)

# ---- fragment 3 ----
def my_func(x):
    return np.sin(x)

def derMy_func(x):
    return np.cos(x)

# ---- fragment 4 ----
def calculate_accuracy(predictions, Y):
    preds = (predictions > 0.5).astype(int)
    return np.mean(preds == Y)

# ---- fragment 5 ----
    input_dim = 2 - кількість входів
    hidden_dim = 4 - кількість нейронів у прихованому шарі   Для проблеми XOR мінімальна необхідна кількість нейронів у прихованому шарі – 2 ( чим їх більше тим точніше обрахунки, але я обрав просто в 2 рази більшу кулькість і  для 4 в мене там достатня точність обрахунків )
    output_dim = 1 - кількість виходів

# ---- fragment 6 ----
    W1 = np.random.randn(input_dim, hidden_dim) ( це ваги між вхідним та прихованим шаром )
    b1 = np.zeros((1, hidden_dim)) Зміщення для прихованого шару
    W2 = np.random.randn(hidden_dim, output_dim) Ваги між прихованим і вихідним шарами
    b2 = np.zeros((1, output_dim)) Зміщення для вихідного шару

# ---- fragment 7 ----
 Z1 = np.dot(X, W1) + b1 ( лініцне перетворення входів )
 A1 = activation_func(Z1) ( функція активації залежно від вхідних даних )
 Z2 = np.dot(A1, W2) + b2  (вагове перетворення виходу з прихованого шару)
 A2 = sigmoid(Z2) ( остаточний результат (Sigmoid для отримання ймовірностей між 0 і 1).)

# ---- fragment 8 ----
dA2 = (A2 - y) * derSigmoid(A2) тут виконуєтся Обчислення градієнта для вихідного шару, Помилка (A2 – y) показує, наскільки передбачене значення A2 відрізняється від справжнього. Множимо її на derSigmoid(A2), бо похідна Sigmoid контролює, як змінювати ваги.

 dW2 = np.dot(A1.T, dA2) (  обчислюємо градієнт ваг для W2. )
db2 = np.sum(dA2, axis=0, keepdims=True) (  градієнт для зміщення b2 )

dA1 = np.dot(dA2, W2.T) * activation_derivative(A1) ( Обчислення градієнта для прихованого шару )  Помилка розповсюджується назад через ваги W2 і  Множимо на похідну функції анктивації, бо це визначає, наскільки сильно прихований шар вплинув на помилку.

dW1 = np.dot(X.T, dA1) ( обчислюємо градієнт ваг для W1 )
db1 = np.sum(dA1, axis=0, keepdims=True)  (  градієнт для зміщення b1. )

# ---- fragment 9 ----
      W2 -= lr * dW2
       b2 -= lr * db2
       W1 -= lr * dW1
       b1 -= lr * db1

# ---- fragment 10 ----
if epoch % 1000 == 0:
            predictions = (A2 > 0.5).astype(int)
            acc = calculate_accuracy(predictions, y)
            accuracies.append(acc)
            print(f"Epoch {epoch}, Loss: {loss:.4f}, Accuracy: {acc:.4f}")

# ---- fragment 11 ----
def predict(X, W1, b1, W2, b2, activation_func):
    Z1 = np.dot(X, W1) + b1
    A1 = activation_func(Z1)
    Z2 = np.dot(A1, W2) + b2
    A2 = sigmoid(Z2)
    return (A2 > 0.5).astype(int)

# ---- fragment 12 ----
    Z = predict(np.c_[xx.ravel(), yy.ravel()], W1, b1, W2, b2, activation_func)
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, alpha=0.3)
    plt.scatter(X[:, 0], X[:, 1], c=y.flatten(), edgecolors='k', cmap=plt.cm.Spectral)

# ---- fragment 13 ----
    plt.show()

for name, res in results.items():
    plot_decision_boundary(X, y, res['W1'], res['b1'], res['W2'], res['b2'], activation_functions[name][0])

for name, res in results.items():
    plt.figure(figsize=(6, 4))
    plt.plot(res['losses'], label=f"{name}")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")

# ---- fragment 14 ----
    plt.legend()
    plt.grid()
    plt.show()
