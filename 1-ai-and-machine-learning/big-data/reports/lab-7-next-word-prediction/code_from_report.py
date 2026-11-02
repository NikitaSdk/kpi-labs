# Code extracted from the lab report (report.pdf)

# ---- fragment 1 ----
import tiktoken

with open("THE EMPEROR’S NEW CLOTHES.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

tokenizer = tiktoken.get_encoding("gpt2")
enc_text = tokenizer.encode(raw_text)

print("Кількість токенів у тексті: ", len(enc_text))
enc_sample = enc_text[50:]

print("Перші 10 токенів обрізаного тексту: ", enc_sample[:10])

# ---- fragment 2 ----
context_size = 4
x = enc_sample[:context_size]
y = enc_sample[1:context_size+1]
print(f"x: {x}")
print(f"y: {y}")

print("У декодованому вигляді: ")
print("x: ", tokenizer.decode(x))
print("y: ", tokenizer.decode(y))

print("Метод ковзного вікна: ")
for i in range(1, context_size+1):
    context = enc_sample[:i]
    desired = enc_sample[i]
    print(tokenizer.decode(context), "-", tokenizer.decode([desired]))

# ---- fragment 3 ----
import torch
from torch.utils.data import Dataset, DataLoader

class GPTDatasetV1(Dataset):
    def __init__(self, txt, tokenizer, max_length, stride):
        self.input_ids = []
        self.target_ids = []

        token_ids = tokenizer.encode(txt)

        for i in range(0, len(token_ids) - max_length, stride):
            input_chunk = token_ids[i:i + max_length]
            target_chunk = token_ids[i + 1: i + max_length + 1]
            self.input_ids.append(torch.tensor(input_chunk))
            self.target_ids.append(torch.tensor(target_chunk))

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return self.input_ids[idx], self.target_ids[idx]

# ---- fragment 4 ----
def create_dataloader_v1(txt, batch_size=4, max_length=256,
                         stride=128, shuffle=True, drop_last=True, num_workers=0):
    tokenizer = tiktoken.get_encoding("gpt2")

    dataset = GPTDatasetV1(txt, tokenizer, max_length, stride)
    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        drop_last=drop_last,
        num_workers=num_workers
    )
    return dataloader

# ---- fragment 5 ----
print("Тест 1: batch_size=4, max_length=10, stride=5")
dataloader = create_dataloader_v1(text, batch_size=4, max_length=10, stride=5)
inputs, targets = next(iter(dataloader))
print("Inputs shape:", inputs.shape)
print("Targets shape:", targets.shape)
print("Inputs:", inputs)
print("Targets:", targets)

print("\nТест 2: batch_size=2, max_length=10, stride=2")
dataloader = create_dataloader_v1(text, batch_size=2, max_length=10, stride=2)
inputs, targets = next(iter(dataloader))
print("Inputs shape:", inputs.shape)
print("Targets shape:", targets.shape)
print("Inputs:", inputs)
print("Targets:", targets)

print("\nТест 3: batch_size=3, max_length=20, stride=10")
dataloader = create_dataloader_v1(text, batch_size=3, max_length=20, stride=10)
inputs, targets = next(iter(dataloader))
print("Inputs shape:", inputs.shape)
print("Targets shape:", targets.shape)
print("Inputs:", inputs)
print("Targets:", targets)

# ---- fragment 6 ----
def show_batch_as_text(inputs, targets, tokenizer, num_examples=3):
    print("\nТекстове представлення кількох тестів\n")

    for i in range(min(num_examples, len(inputs))):
        inp_text = tokenizer.decode(inputs[i].tolist())
        tgt_text = tokenizer.decode(targets[i].tolist())

        print(f"Тест {i+1}:")
        print("Вхід  ->", inp_text)
        print("Ціль  ->", tgt_text)

data_iter = iter(dataloader)
inputs, targets = next(data_iter)

show_batch_as_text(inputs, targets,tokenizer, num_examples=5)

# ---- fragment 7 ----
def test_dataloader_params(raw_text, params_list):
    tokenizer = tiktoken.get_encoding("gpt2")

    for i, params in enumerate(params_list, 1):
        max_length, stride = params

        dataloader = create_dataloader_v1(
            raw_text,
            batch_size=1,
            max_length=max_length,
            stride=stride,
            shuffle=False
        )

        data_iter = iter(dataloader)
        inputs, targets = next(data_iter)

        print(f"\nТест {i}: max_length={max_length}, stride={stride}")
        print("Вхідні токени:", inputs.tolist()[0])
        print("Цільові токени:", targets.tolist()[0])
        print("Вхід:", tokenizer.decode(inputs[0].tolist()))
        print("Ціль:", tokenizer.decode(targets[0].tolist()))

params_list = [
    (2, 2),
    (4, 1),
    (4, 2),
    (8, 2),
    (8, 8)
]

test_dataloader_params(text, params_list)
