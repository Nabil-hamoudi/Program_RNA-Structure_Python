from parameters import *
from matrix_vhx import matrix_vhx
from matrix_zhx import matrix_zhx
from matrix_yhx import matrix_yhx
from matrix_whi import matrix_whi

# matrix whx

def matrix_whx(i, j, k, l):
    """return the value of the gap matrix whx at the given indices"""
    # check indices
    if (i > k) or (k > l) or (l > j):
        print(f"Error : invalid index.\n i = {i}, k = {k}, l = {l}, j= {j} ")
        exit(1)

    if whx[j][l][k][i] is not None:
        return whx[j][l][k][i]
    
    # initialization of the optimal score
    best_score = float('inf')

    
    # search for a better score
    
    # paired
    if score := (2 * parameters["P_wave"] + matrix_vhx(i, j, k, l)) < best_score: best_score = score
    if score := (parameters["P_wave"] + matrix_zhx(i, j, k, l)) < best_score: best_score = score
    if score := (parameters["P_wave"] + matrix_yhx(i, j, k, l)) < best_score: best_score = score

    # single-stranded
    if score := (parameters["Q_wave"] + matrix_whx(i+1, j, k, l)) < best_score: best_score = score
    if score := (parameters["Q_wave"] + matrix_whx(i, j-1, k, l)) < best_score: best_score = score
    if score := (parameters["Q_wave"] + matrix_whx(i, j, k-1, l)) < best_score: best_score = score
    if score := (parameters["Q_wave"] + matrix_whx(i, j, k, l+1)) < best_score: best_score = score

    # nested bifurcations
    if score := (matrix_wxi(i, k) + matrix_wxi(l, j)) < best_score: best_score = score

    for r in range(i, k+1):
        if score := (matrix_whi(i, r) + matrix_whx(r+1, j, k, l)) < best_score: best_score = score
        if score := (matrix_whi(r+1, k) + matrix_whx(i, j, r, l)) < best_score: best_score = score
        
    for s in range(l, j+1):
        if score := (matrix_whi(s+1, j) + matrix_whx(i, s, k, l)) < best_score: best_score = score
        if score := (matrix_whi(l, s) + matrix_whx(i, j, k, s+1)) < best_score: best_score = score
    
    for s in range(l, j+1):
        for r in range(i, k+1):
            if score := (matrix_yhx(i, j, r, s) + matrix_zhx(r, s,  k, l)) < best_score: best_score = score
            if score := (parameters["M_wave"] + matrix_whx(i, j, r, s) + matrix_whx(r+1, s-1, k, l)) < best_score: best_score = score

    # non-nested bifurcations
            if score := (parameters["Gwh"] + matrix_whx(i, s, r, l) + matrix_whx(r+1, j, k, s+1)) < best_score: best_score = score

    for s_prime in range(l, j+1):
        for s in range(l, s_prime+1):
            for r_prime in range(i, k+1):
                for r in range(i, r_prime+1):
                    if score := (parameters["Gwh"] + matrix_whx(i, s_prime, k, s) \
                            + matrix_whx(l, j, s-1, s_prime+1)) < best_score: best_score = score
                    if score := (parameters["Gwh"] + matrix_whx(r, j, r_prime, l) \
                            + matrix_whx(i, k, r-1, r_prime+1)) < best_score: best_score = score

    # store the best score in the matrix and return it 
    whx[j][l][k][i] = best_score
    return best_score
