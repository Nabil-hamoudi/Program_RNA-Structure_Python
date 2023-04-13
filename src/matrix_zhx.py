from parameters import *
from matrix_vhx import matrix_vhx
from matrix_wxi import matrix_wxi
from matrix_whx import matrix_whx
from matrix_vx import matrix_vx


def matrix_zhx(i, j, k, l):
    """return the value of the gap matrix zhx at the given indices"""
    if (i > k) or (k > l) or (l > j):
        print(f"Error : invalid index.\n i = {i}, k = {k}, l = {l}, j= {j} ")
        exit(1)

    if zhx[j][l][k][i] is not None:
        return zhx[j][l][k][i]

    if (k+1) == l:
        zhx[j][l][k][i] = matrix_vx(i, j)
        return matrix_vx(i, j)

    # initialization of the optimal score
    best_score = float('inf')

    # paired
    if score := (parameters["P_wave"] + matrix_vhx(i, j, k, l)) < best_score: best_score = score

    # dangles
    if score := (parameters["L_wave"](l, k-1, l+1) + parameters["R_wave"](k, k-1, l+1) + parameters["P_wave"] + matrix_vhx(i, j, k-1, l+1)) < best_score: best_score = score
    if score := (parameters["R_wave"](k, k-1, l) + parameters["P_wave"] + matrix_vhx(i, j, k-1, l)) < best_score: best_score = score
    if score := (parameters["L_wave"](l, k, l+1) + parameters["P_wave"] + matrix_vhx(i, j, k, l+1)) < best_score: best_score = score

    # single-stranded
    if score := (parameters["Q_wave"] + matrix_zhx(i, j, k-1, l)) < best_score: best_score = score
    if score := (parameters["Q_wave"] + matrix_zhx(i, j, k, l+1)) < best_score: best_score = score

    # nested bifurcations
    for r in range(i, k+1):
        if score := (matrix_zhx(i, j, r, l) + matrix_wxi(r+1, k)) < best_score: best_score = score
        if score := ((2 * parameters["P_wave"]) + parameters["C_wave"](r, l, r+1, k) + matrix_vhx(i, j, r, l) + matrix_vx(r+1, k)) < best_score: best_score = score

    for s in range(l, j+1):
        if score := (matrix_zhx(i, j, k, s) + matrix_wxi(l, s-1)) < best_score: best_score = score
        if score := ((2 * parameters["P_wave"]) + parameters["C_wave"](s-1, l, s, k) + matrix_vhx(i, j, k, s) + matrix_vx(l, s-1)) < best_score: best_score = score

    for r in range(i, k+1):
        for s in range(l, j+1):
            if score := (parameters["EIS2"](i, j, r, s) + matrix_zhx(r, s, k, l)) < best_score: best_score = score

    if score := (parameters["P_wave"] + parameters["M_wave"] + matrix_whx(i + 1, j - 1, k, l)) < best_score: best_score = score

    # store the best score in the matrix and return it
    zhx[j][l][k][i] = best_score
    return best_score
