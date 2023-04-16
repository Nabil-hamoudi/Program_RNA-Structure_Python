from parameters import *
from matrix_whx import matrix_whx

# matrix vhx

def matrix_vhx(i, j, k, l):
    """Return the value of the gap matrix vhx at the given indices"""

    #check indices
    if (i > k) or (k > l) or (l > j):
        print(f"Error : invalid index. \n i = {i}, k = {k}, l = {l}, j = {j}")
        exit(1)

    if vhx[j][l][k][i] is not None:
        return vhx[j][l][k][i]


    # initialization of the optimal score
    best_score = float('inf')


    # search for a better score
    if score := parameters["EIS2_wave"](i, j, k, l) < best_score: best_score = score
    if score := (2 * parameters["P_wave"] + parameters["M_wave"] + matrix_whx(i+1, j-1, k-1, l+1)) < best_score: best_score =
    score


    for s in range(l, j+1):
        for r in range(i, k+1):
            if score := parameters["EIS2_wave"](i, j, r s) + matrix_vhx(r, s, k, l) < best_score: best_score =
            score
            if score := parameters["EIS2_wave"](r, s k, l) + matrix_vhx(i, j, r, s) < best_score: best_score =
            score


    # store the best score in the matrix and return it 
    vhx[j][l][k][i] = best_score
    return best_score
