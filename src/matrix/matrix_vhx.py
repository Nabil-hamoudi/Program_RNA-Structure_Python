from parameters import *
import matrix_whx

# matrix vhx

def matrix_vhx(i, j, k, l, matrix, sequence):
    """Return the value of the gap matrix vhx at the given indices"""

    #check indices
    if (i > k) or (k > l) or (l > j):
        # print(f"Error : invalid index. \n i = {i}, k = {k}, l = {l}, j = {j}")
        # exit(1)
        return float('inf')

    if matrix["vhx"][j][l][k][i] is not None:
        return matrix["vhx"][j][l][k][i]
    matrix["vhx"][j][l][k][i] = float('inf')


    # initialization of the optimal score
    best_score = float('inf')


    # search for a better score
    if (score := parameters["EIS2_wave"](i, j, k, l, sequence)) < best_score: best_score = score
    if (score := (2 * parameters["P_wave"] + parameters["M_wave"] + matrix_whx.matrix_whx(i+1, j-1, k-1, l+1, matrix, sequence))) < best_score: best_score = score


    for s in range(l, j+1):
        for r in range(i, k+1):
            if (score := parameters["EIS2_wave"](i, j, r, s, sequence) + matrix_vhx(r, s, k, l, matrix, sequence)) < best_score: best_score = score
            if (score := parameters["EIS2_wave"](r, s, k, l, sequence) + matrix_vhx(i, j, r, s, matrix, sequence)) < best_score: best_score = score


    # store the best score in the matrix and return it 
    matrix["vhx"][j][l][k][i] = best_score
    return best_score