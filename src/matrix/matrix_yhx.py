from parameters import *
import matrix_vhx
import matrix_wxi
import matrix_whx
import matrix_vx


def matrix_yhx(i, j, k, l, matrix, sequence):
    """return the value of the gap matrix yhx at the given indices"""
    if (i > k) or (k > l) or (l > j):
        # print(f"Error : invalid index.\n i = {i}, k = {k}, l = {l}, j= {j} ")
        # exit(1)
        return float('inf')
            
    if matrix["yhx"][j][l][k][i] is not None:
        return matrix["yhx"][j][l][k][i]
    matrix["yhx"][j][l][k][i] = float('inf')

    # initialization of the optimal score
    best_score = float('inf')

    # paired
    if (score := (parameters["P_wave"] + matrix_vhx.matrix_vhx(i, j, k, l, matrix, sequence))) < best_score: best_score = score

    # dangles
    if (score := (parameters["L_wave"](i, i+1, j-1, sequence) + parameters["R_wave"](j, i+1, j-1, sequence) + parameters["P_wave"] + matrix_vhx.matrix_vhx(i+1, j-1, k, l, matrix, sequence))) < best_score: best_score = score
    if (score := (parameters["L_wave"](i, i+1, j, sequence) + parameters["P_wave"] + matrix_vhx.matrix_vhx(i+1, j, k, l, matrix, sequence))) < best_score: best_score = score
    if (score := (parameters["R_wave"](j, i, j-1, sequence) + parameters["P_wave"] + matrix_vhx.matrix_vhx(i, j-1, k, l, matrix, sequence))) < best_score: best_score = score

    # single-stranded
    if (score := (parameters["Q_wave"] + matrix_yhx(i + 1, j, k, l, matrix, sequence))) < best_score: best_score = score
    if (score := (parameters["Q_wave"] + matrix_yhx(i, j - 1, k, l, matrix, sequence))) < best_score: best_score = score

    # nested bifurcations
    for r in range(i, k+1):
        if (score := (matrix_wxi.matrix_wxi(i, r, matrix, sequence) + matrix_yhx(r+1, j, k, l, matrix, sequence))) < best_score: best_score = score
        if (score := ((2 * parameters["P_wave"]) + parameters["C_wave"](r, i, r+1, j, sequence) + matrix_vx.matrix_vx(i, r, matrix, sequence) + matrix_vhx.matrix_vhx(r+1, j, k, l, matrix, sequence))) < best_score: best_score = score

    for s in range(l, j+1):
        if (score := (matrix_yhx(i, s, k, l, matrix, sequence) + matrix_wxi.matrix_wxi(s+1, j, matrix, sequence))) < best_score: best_score = score
        if (score := ((2 * parameters["P_wave"]) + parameters["C_wave"](s, i, s+1, j, sequence) + matrix_vhx.matrix_vhx(i, s, k, l, matrix, sequence) + matrix_vx.matrix_vx(s+1, j, matrix, sequence))) < best_score: best_score = score

    for r in range(i, k+1):
        for s in range(l, j+1):
            if (score := (matrix_yhx(i, j, r, s, matrix, sequence) + EIS2(r, s, k, l, sequence))) < best_score: best_score = score

    if (score := (parameters["P_wave"] + parameters["M_wave"] + matrix_whx.matrix_whx(i, j, k - 1, l + 1, matrix, sequence))) < best_score: best_score = score

    # store the best score in the matrix and return it
    matrix["yhx"][j][l][k][i] = best_score
    return best_score
