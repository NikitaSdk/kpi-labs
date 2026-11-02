from Bio.Align import substitution_matrices
import numpy as np
import matplotlib.pyplot as plt

blosum50 = substitution_matrices.load("BLOSUM62")


T = int(input("Введіть значення T: "))

x = "VADTPVT"
y = "VAGPVAV"
d = 8

n, m = len(x), len(y)
F = np.zeros((n + 1, m + 2), dtype=int)
Trace = [[0 for _ in range(m + 2)] for _ in range(n + 1)]

for j in range(1, m + 1):
    i0 = 0
    max_score = F[0][j - 1]
    for i in range(0, n + 1):
        current_score = F[i][j - 1] - T
        if current_score > max_score:
            max_score = current_score
            i0 = i
    F[0][j] = max_score
    t = (i0, j - 1)
    Trace[0][j] = t

    for i in range(1, n + 1):
        top = F[0][j]
        insert = F[i - 1][j - 1] + blosum50[x[i - 1], y[j - 1]]
        insert_x = F[i - 1][j] - d
        insert_y = F[i][j - 1] - d
        max_score = max(top, insert, insert_x, insert_y)
        if max_score == top:
            Trace[i][j] = [0, j]
        elif max_score == insert:
            Trace[i][j] = [i - 1, j - 1]
        elif max_score == insert_x:
            Trace[i][j] = [i - 1, j]
        elif max_score == insert_y:
            Trace[i][j] = [i, j - 1]
        F[i][j] = max_score

i0 = 0
j = m + 1
max_score = F[0][j - 1]
for i in range(0, n + 1):
    current_score = F[i][j - 1] - T
    if current_score > max_score:
        max_score = current_score
        i0 = i

F[0][m + 1] = max_score
Trace[0][m + 1] = (i0, m)

start_pos = (0, m + 1)
aligned_x = ""
aligned_y = ""
i, j = start_pos
path = []

while Trace[i][j] != 0:
    path.append(F[i][j])
    if Trace[i][j] == [i - 1, j - 1]:
        aligned_x = x[i - 1] + aligned_x
        aligned_y = y[j - 1] + aligned_y
        i, j = Trace[i][j]
    elif Trace[i][j] == [i - 1, j]:
        i, j = Trace[i][j]
        if i > 0:
            aligned_x = x[i - 1] + aligned_x
            aligned_y = '-' + aligned_y
    elif Trace[i][j] == [i, j - 1]:
        i, j = Trace[i][j]
        if j > 0:
            aligned_x = '-' + aligned_x
            aligned_y = y[j - 1] + aligned_y
    else:
        i, j = Trace[i][j]
        aligned_x = '*' + aligned_x
        if j < len(y):
            aligned_y = y[j] + aligned_y
        else:
            aligned_y = '*' + aligned_y

path.append(F[i][j])
path.pop(0)
path.reverse()

print("\nМодифіковане локальне вирівнювання:")
print(aligned_x)
print(aligned_y)
print("Оцінка:", F[0][m + 1])
print("Шлях:", "->".join(map(str, path[::-1])))

n, m = len(x), len(y)
fig, ax = plt.subplots()
cax = ax.matshow(F[:, :m + 1], cmap="coolwarm")
ax.set_xticks(range(m + 1))
ax.set_yticks(range(n + 1))
ax.set_xticklabels([''] + list(y))
ax.set_yticklabels([''] + list(x))

for i in range(n + 1):
    for j in range(m + 1):
        ax.text(j, i, F[i, j], va='center', ha='center', color='white')

i, j = start_pos
while Trace[i][j] != 0:
    if j < m + 1:
        ax.text(j, i, F[i][j], va='center', ha='center', color='green')
    i, j = Trace[i][j]
if j < m + 1:
    ax.text(j, i, F[i][j], va='center', ha='center', color='green')

plt.show()
