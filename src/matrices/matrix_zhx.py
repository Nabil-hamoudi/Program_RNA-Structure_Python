from parameters import *
from matrices import matrix_vhx, matrix_wxi, matrix_whx, matrix_vx


def matrix_zhx(i, j, k, l, matrix, sequence):
    """
    return the value of the gap matrix zhx at the given indices
    """
    
    if (i > k) or (k > l) or (l > j):
        return float('inf')

    if matrix["zhx"][j][l][k][i] is not None:
        return matrix["zhx"][j][l][k][i][0]
    matrix["zhx"][j][l][k][i] = (float('inf'), [])

    if (k+1) == l:
        matrix["zhx"][j][l][k][i] = (matrix_vx.matrix_vx(i, j, matrix, sequence), [("vx", i, j)])
        return matrix_vx.matrix_vx(i, j, matrix, sequence)

    # initialization of the optimal score
    best_score = float('inf')

    # creation of the list for traceback
    matrices_used = []


    # paired
    if (score := (parameters["P_wave"] + matrix_vhx.matrix_vhx(i, j, k, l, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("vhx", i, j, k, l)]

    # dangles
    if (score := (parameters["L_wave"](l, k-1, l+1, sequence) + parameters["R_wave"](k, k-1, l+1, sequence) 
                  + parameters["P_wave"] + matrix_vhx.matrix_vhx(i, j, k-1, l+1, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("vhx", i, j, k-1, l+1)]

    if (score := (parameters["R_wave"](k, k-1, l, sequence) + parameters["P_wave"] 
                  + matrix_vhx.matrix_vhx(i, j, k-1, l, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("vhx", i, j, k-1, l)]

    if (score := (parameters["L_wave"](l, k, l+1, sequence) + parameters["P_wave"] 
                  + matrix_vhx.matrix_vhx(i, j, k, l+1, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("vhx", i, j, k, l+1)]


    # single-stranded
    if (score := (parameters["Q_wave"] + matrix_zhx(i, j, k-1, l, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("zhx", i, j, k-1, l)]

    if (score := (parameters["Q_wave"] + matrix_zhx(i, j, k, l+1, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("zhx", i, j, k, l+1)]


    # nested bifurcations
    for r in range(i, k+1):

        if (score := (matrix_zhx(i, j, r, l, matrix, sequence) + matrix_wxi.matrix_wxi(r+1, k, matrix, sequence))) < best_score:
            best_score = score
            matrices_used = [("zhx", i, j, r, l), ("wxi", r+1, k)]

        if (score := ((2 * parameters["P_wave"]) + parameters["C_wave"](r, l, r+1, k, sequence) 
                      + matrix_vhx.matrix_vhx(i, j, r, l, matrix, sequence) 
                      + matrix_vx.matrix_vx(r+1, k, matrix, sequence))) < best_score:
            best_score = score
            matrices_used = [("vhx", i, j, r, l), ("vx", r+1, k)]


    for s in range(l, j+1):

        if (score := (matrix_zhx(i, j, k, s, matrix, sequence) + matrix_wxi.matrix_wxi(l, s-1, matrix, sequence))) < best_score:
            best_score = score
            matrices_used = [("zhx", i, j, k, s), ("wxi", l, s-1)]

        if (score := ((2 * parameters["P_wave"]) + parameters["C_wave"](s-1, l, s, k, sequence) 
                      + matrix_vhx.matrix_vhx(i, j, k, s, matrix, sequence) 
                      + matrix_vx.matrix_vx(l, s-1, matrix, sequence))) < best_score:
            best_score = score
            matrices_used = [("vhx", i, j, k, s), ("vx", l, s-1)]


    for r in range(i, k+1):
        for s in range(l, j+1):

            if (score := (parameters["EIS2"](i, j, r, s, sequence) + matrix_zhx(r, s, k, l, matrix, sequence))) < best_score:
                best_score = score
                matrices_used = [("EIS2", i, j, r, s), ("zhx", r, s, k, l)] 

    if (score := (parameters["P_wave"] + parameters["M_wave"] 
                  + matrix_whx.matrix_whx(i+1, j-1, k, l, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("whx", i+1, j-1, k, l)]


    # store the best score in the matrix and return it
    matrix["zhx"][j][l][k][i] = (best_score, matrices_used)
    return best_score
