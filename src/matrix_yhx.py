from parameters import * 
from matrix_vhx import matrix_vhx
from matrix_wxi import matrix_wxi
from matrix_whx import matrix_whx


def matrix_yhx(i, j, k, l):
    """return the value of the gap matrix yhx at the given indices"""
    if (i > k) or (k > l) or (l > j):
        print(f"Error : invalid index.\n i = {i}, k = {k}, l = {l}, j= {j} ")
        exit(1)

    if yhx[j][l][k][i] is not None:
        return yhx[j][l][k][i]

    # initialization of the optimal score
    best_score = float('inf')

    # paired
    if score := (parameters["P_wave"] + matrix_vhx(i, j, k, l)) < best_score: best_score = score

    # single-stranded
    if score := (parameters["Q_wave"] + matrix_yhx(i + 1, j, k, l)) < best_score: best_score = score
    if score := (parameters["Q_wave"] + matrix_yhx(i, j - 1, k, l)) < best_score: best_score = score

    # nested bifurcations
    for r in range(i, k+1):
        if score := (matrix_wxi(i, r) + matrix_yhx(r+1, j, k, l)) < best_score: best_score = score

    for s in range(l, j+1):
        if score := (matrix_yhx(i, s, k, l) + matrix_wxi(s+1, j)) < best_score: best_score = score

    for r in range(i, k+1):
        for s in range(l, j+1):
            if score := (matrix_yhx(i, j, r, s) + EIS2(r, s, k, l)) < best_score: best_score = score

    if score := (parameters["P_wave"] + parameters["M_wave"] + matrix_whx(i, j, k - 1, l + 1)) < best_score: best_score = score

    # store the best score in the matrix and return it 
    yhx[j][l][k][i] = best_score
    return best_score
