from Bio.Align import substitution_matrices

blosum62 = substitution_matrices.load("BLOSUM62")

import numpy as np
import matplotlib.pyplot as plt


def local_alignment(x, y, d):
    m, n = len(x), len(y)
    F = np.zeros((m + 1, n + 1), dtype=int)
    Trace = np.zeros((m + 1, n + 1), dtype=int)

    # fill F
    for i in range(1, m + 1):
        for j in range(1, n + 1):

            match = F[i - 1][j - 1] + blosum62[x[i - 1], y[j - 1]]
            insert_x = F[i - 1][j] - d
            insert_y = F[i][j - 1] - d
            zero = 0

            max_score = max(zero, match, insert_x, insert_y)
            F[i][j] = max_score

            if (max_score == match):
                Trace[i][j] = 1
            elif (max_score == insert_x):
                Trace[i][j] = 2
            elif (max_score == insert_y):
                Trace[i][j] = 3
            else:
                Trace[i][j] = 0

    return F, Trace


def local_traceback(F, Trace, x, y):
    res_X = ""
    res_Y = ""

    i, j = np.unravel_index(np.argmax(F), F.shape)
    max_score = F[i][j]

    while (Trace[i][j] != 0 and i > 0 and j > 0):

        print((i, j))

        if (Trace[i][j] == 1):
            res_X = x[i - 1] + res_X
            res_Y = y[j - 1] + res_Y
            i -= 1
            j -= 1
        elif (Trace[i][j] == 2):
            res_X = x[i - 1] + res_X
            res_Y = '-' + res_Y
            i -= 1
        else:
            res_X = '-' + res_X
            res_Y = y[j - 1] + res_Y
            j -= 1

    return res_X, res_Y, max_score


x = "VELVM"
y = "TVELV"

F, T = local_alignment(x, y, 8)
show_alignment_matrix(F, x, y)
print(local_traceback(F, T, x, y))
