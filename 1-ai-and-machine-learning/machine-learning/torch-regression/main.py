import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np

# 1. Генерація тренувальних даних
x_train = torch.linspace(-1, 1, 101).view(-1, 1)
y_train = x_train ** 2

# 2. Визначення моделі (аналог FANN create_standard(3, 1, 10, 1))
model = nn.Sequential(
    nn.Linear(1, 10),
    nn.Tanh(),               # SIGMOID_SYMMETRIC ≈ tanh
    nn.Linear(10, 1)         # LINEAR
)

# 3. Функція втрат і оптимізатор
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# 4. Навчання: 5000 епох
mse_list = []
for epoch in range(1, 5001):
    optimizer.zero_grad()
    output = model(x_train)
    loss = criterion(output, y_train)
    loss.backward()
    optimizer.step()

    mse_list.append(loss.item())

    if epoch % 100 == 0 or epoch == 1 or epoch == 5000:
        print(f"Epoch {epoch}, MSE = {loss.item():.6f}")

# 5. Тестування (аналог run)
print("\nTesting:")
with torch.no_grad():
    for i in range(11):
        x = i / 5.0 - 1.0  # те саме, що static_cast<float>(i) / 5.0f - 1.0f
        x_tensor = torch.tensor([[x]], dtype=torch.float32)
        y_pred = model(x_tensor).item()
        print(f"x = {x:.1f}, predict = {y_pred:.6f}, actual = {x*x:.6f}")

# 6. Побудова графіку втрат
plt.plot(mse_list)
plt.xlabel("Epoch")
plt.ylabel("MSE")
plt.title("Loss over Epochs")
plt.grid(True)
plt.show()
