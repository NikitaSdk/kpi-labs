import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR, CosineAnnealingLR, ExponentialLR
from torch.utils.data import DataLoader, Subset
import torchvision
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------
# 1. Підготовка даних (Dataset)
# ---------------------------
transform = transforms.Compose([transforms.ToTensor()])

# Завантаження MNIST (тренувальний та тестовий набори)
train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)

# Вибір підмножини: 10000 зразків для тренування та 2000 для тестування
train_indices = np.random.choice(len(train_dataset), 10000, replace=False)
test_indices = np.random.choice(len(test_dataset), 2000, replace=False)
train_subset = Subset(train_dataset, train_indices)
test_subset = Subset(test_dataset, test_indices)

# Створення DataLoader-ів
train_loader = DataLoader(train_subset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_subset, batch_size=64, shuffle=False)

# ---------------------------
# 2. Визначення нейронної мережі
# ---------------------------
class NeuralNet(nn.Module):
    def __init__(self):
        super(NeuralNet, self).__init__()
        # Перший шар: Linear -> BatchNorm -> ReLU -> Dropout
        self.fc1 = nn.Linear(28*28, 256)
        self.bn1 = nn.BatchNorm1d(256)
        self.dropout1 = nn.Dropout(0.5)
        # Другий шар: Linear -> BatchNorm -> ReLU -> Dropout
        self.fc2 = nn.Linear(256, 128)
        self.bn2 = nn.BatchNorm1d(128)
        self.dropout2 = nn.Dropout(0.5)
        # Вихідний шар: класифікація на 10 класів
        self.fc3 = nn.Linear(128, 10)
        
    def forward(self, x):
        x = x.view(-1, 28*28)  # Перетворення зображення в вектор
        x = self.fc1(x)
        x = self.bn1(x)
        x = torch.relu(x)
        x = self.dropout1(x)
        x = self.fc2(x)
        x = self.bn2(x)
        x = torch.relu(x)
        x = self.dropout2(x)
        x = self.fc3(x)
        return x

# ---------------------------
# 3. Функція навчання моделі
# ---------------------------
def train_model(model, train_loader, test_loader, optimizer, scheduler, epochs=10, l1_lambda=0.0):
    criterion = nn.CrossEntropyLoss()
    
    train_losses = []
    test_losses = []
    train_acc = []
    test_acc = []
    
    for epoch in range(epochs):
        model.train()  # Режим тренування
        running_loss = 0.0
        correct = 0
        total = 0
        
        for data, target in train_loader:
            optimizer.zero_grad()
            outputs = model(data)
            loss = criterion(outputs, target)
            
            # L1 регулярізація (якщо l1_lambda > 0)
            if l1_lambda > 0:
                l1_norm = sum(p.abs().sum() for p in model.parameters())
                loss = loss + l1_lambda * l1_norm
            
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * data.size(0)
            _, predicted = torch.max(outputs.data, 1)
            total += target.size(0)
            correct += (predicted == target).sum().item()
        
        scheduler.step()  # Оновлення learning rate за допомогою scheduler
        
        epoch_loss = running_loss / len(train_loader.dataset)
        epoch_acc = correct / total
        train_losses.append(epoch_loss)
        train_acc.append(epoch_acc)
        
        # Оцінка моделі на тестових даних
        model.eval()
        test_loss = 0.0
        correct_test = 0
        total_test = 0
        
        with torch.no_grad():
            for data, target in test_loader:
                outputs = model(data)
                loss = criterion(outputs, target)
                test_loss += loss.item() * data.size(0)
                _, predicted = torch.max(outputs.data, 1)
                total_test += target.size(0)
                correct_test += (predicted == target).sum().item()
                
        epoch_test_loss = test_loss / len(test_loader.dataset)
        epoch_test_acc = correct_test / total_test
        test_losses.append(epoch_test_loss)
        test_acc.append(epoch_test_acc)
        
        print(f"Epoch {epoch+1}/{epochs}: Train loss: {epoch_loss:.4f}, Train acc: {epoch_acc:.4f} | Test loss: {epoch_test_loss:.4f}, Test acc: {epoch_test_acc:.4f}")
    
    return {
        "train_losses": train_losses,
        "test_losses": test_losses,
        "train_acc": train_acc,
        "test_acc": test_acc
    }

# ---------------------------
# 4. Конфігурації експериментів
# ---------------------------
# Створюємо 9 конфігурацій: 3 оптимізатори x 3 scheduler’и

experiment_configs = [
    # Конфігурації для StepLR
    {
       "name": "SGD + StepLR",
       "optimizer": "SGD",
       "lr": 0.01,
       "scheduler": "StepLR",
       "scheduler_params": {"step_size": 5, "gamma": 0.1},
       "weight_decay": 1e-4,
       "l1_lambda": 0.0,
    },
    {
       "name": "Adam + StepLR",
       "optimizer": "Adam",
       "lr": 0.001,
       "scheduler": "StepLR",
       "scheduler_params": {"step_size": 5, "gamma": 0.1},
       "weight_decay": 1e-4,
       "l1_lambda": 1e-5,
    },
    {
       "name": "RMSprop + StepLR",
       "optimizer": "RMSprop",
       "lr": 0.001,
       "scheduler": "StepLR",
       "scheduler_params": {"step_size": 5, "gamma": 0.1},
       "weight_decay": 1e-4,
       "l1_lambda": 0.0,
    },
    # Конфігурації для CosineAnnealingLR
    {
       "name": "SGD + CosineAnnealingLR",
       "optimizer": "SGD",
       "lr": 0.01,
       "scheduler": "CosineAnnealingLR",
       "scheduler_params": {"T_max": 10},
       "weight_decay": 1e-4,
       "l1_lambda": 0.0,
    },
    {
       "name": "Adam + CosineAnnealingLR",
       "optimizer": "Adam",
       "lr": 0.001,
       "scheduler": "CosineAnnealingLR",
       "scheduler_params": {"T_max": 10},
       "weight_decay": 1e-4,
       "l1_lambda": 1e-5,
    },
    {
       "name": "RMSprop + CosineAnnealingLR",
       "optimizer": "RMSprop",
       "lr": 0.001,
       "scheduler": "CosineAnnealingLR",
       "scheduler_params": {"T_max": 10},
       "weight_decay": 1e-4,
       "l1_lambda": 0.0,
    },
    # Конфігурації для ExponentialLR
    {
       "name": "SGD + ExponentialLR",
       "optimizer": "SGD",
       "lr": 0.01,
       "scheduler": "ExponentialLR",
       "scheduler_params": {"gamma": 0.9},
       "weight_decay": 1e-4,
       "l1_lambda": 0.0,
    },
    {
       "name": "Adam + ExponentialLR",
       "optimizer": "Adam",
       "lr": 0.001,
       "scheduler": "ExponentialLR",
       "scheduler_params": {"gamma": 0.9},
       "weight_decay": 1e-4,
       "l1_lambda": 1e-5,
    },
    {
       "name": "RMSprop + ExponentialLR",
       "optimizer": "RMSprop",
       "lr": 0.001,
       "scheduler": "ExponentialLR",
       "scheduler_params": {"gamma": 0.9},
       "weight_decay": 1e-4,
       "l1_lambda": 0.0,
    },
]

# ---------------------------
# 5. Виконання експериментів
# ---------------------------
results = {}
epochs = 10  # Кількість епох для тренування

for config in experiment_configs:
    print("\nЗапуск експерименту:", config["name"])
    model = NeuralNet()
    
    # Визначення оптимізатора згідно конфігурації
    if config["optimizer"] == "SGD":
        optimizer = optim.SGD(model.parameters(), lr=config["lr"], weight_decay=config["weight_decay"])
    elif config["optimizer"] == "Adam":
        optimizer = optim.Adam(model.parameters(), lr=config["lr"], weight_decay=config["weight_decay"])
    elif config["optimizer"] == "RMSprop":
        optimizer = optim.RMSprop(model.parameters(), lr=config["lr"], weight_decay=config["weight_decay"])
    
    # Налаштування scheduler'а
    if config["scheduler"] == "StepLR":
        scheduler = StepLR(optimizer, **config["scheduler_params"])
    elif config["scheduler"] == "CosineAnnealingLR":
        scheduler = CosineAnnealingLR(optimizer, **config["scheduler_params"])
    elif config["scheduler"] == "ExponentialLR":
        scheduler = ExponentialLR(optimizer, **config["scheduler_params"])
    
    result = train_model(model, train_loader, test_loader, optimizer, scheduler, epochs=epochs, l1_lambda=config["l1_lambda"])
    results[config["name"]] = result

# ---------------------------
# 6. Групування та візуалізація результатів
# ---------------------------
# Групуємо результати за scheduler'ом
grouped_results = {
    "StepLR": [],
    "CosineAnnealingLR": [],
    "ExponentialLR": []
}

for config_name, result in results.items():
    for scheduler_name in grouped_results.keys():
        if scheduler_name in config_name:
            grouped_results[scheduler_name].append((config_name, result))

# Побудова графіків для кожного scheduler'а
for scheduler_name, configs in grouped_results.items():
    # 1. Графік порівняння тестової точності
    plt.figure(figsize=(12, 6))
    for config_name, result in configs:
        epochs_range = range(1, len(result["test_acc"]) + 1)
        # Отримуємо назву оптимізатора (частина до знака " + ")
        label = config_name.split(" + ")[0]
        plt.plot(epochs_range, result["test_acc"], label=label)
    plt.title(f"Порівняння тестової точності для {scheduler_name}")
    plt.xlabel("Епохи")
    plt.ylabel("Точність")
    plt.legend()
    plt.grid(True)
    plt.show()

    # 2. Графік порівняння тренувальних втрат
    plt.figure(figsize=(12, 6))
    for config_name, result in configs:
        epochs_range = range(1, len(result["train_losses"]) + 1)
        label = config_name.split(" + ")[0]
        plt.plot(epochs_range, result["train_losses"], label=label)
    plt.title(f"Порівняння тренувальних втрат для {scheduler_name}")
    plt.xlabel("Епохи")
    plt.ylabel("Втрати")
    plt.legend()
    plt.grid(True)
    plt.show()
