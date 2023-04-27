from parameters import *
from matrices import matrix_wxi, matrix_whx, matrix_zhx, matrix_yhx



def matrix_vx(i, j, matrix, sequence):
    """
    Calculate the box (i,j) of the wx matrix and return its value.
    Entry: i and j: int as i <= j
    Exit: best score value
    """

    # Function input check
    if (i > j):
        return float('inf')

    # Box already calculated ? 
    if matrix["vx"][j][i] is not None:
        return matrix["vx"][j][i][0]
    matrix["vx"][j][i] = (float('inf'), [])

    # #############################
    # Beginning Recursions

    #initialization of the best_score
    best_score = float('inf')

    # creation of the list for traceback
    matrices_used = []

    # IS(1)
    if (score := (parameters["EIS1"](i,j, sequence))) < best_score :
        best_score = score
        matrices_used = [("EIS1", i, j)]

    # IS(2)
    for l in range(i,j):
        for k in range(i+1, l+1):
            if (score := (parameters["EIS2"](i, j, k, l, sequence) 
                          + matrix_vx(k, l, matrix, sequence))) < best_score:
                best_score = score
                matrices_used = [("EIS2", i, j, k, l), ("vx", k, l)]

    # Nested Multiloop
    for k in range(i, j+1):

        if (score := (parameters["Pi"] + parameters["M"] + matrix_wxi.matrix_wxi(i+1, k, matrix, sequence)
                     + matrix_wxi.matrix_wxi(k+1, j-1, matrix, sequence))) < best_score:
            best_score = score
            matrices_used = [("wxi", i+1, k), ("wxi", k+1, j-1)]

        if (score := (2 * parameters["Pi"] + coaxial_stacking(i, j, i+1, k, sequence)
                     + parameters["M"] + matrix_vx(i+1, k, matrix, sequence) 
                     + matrix_wxi.matrix_wxi(k+1, j-1, matrix, sequence))) < best_score:
            best_score = score
            matrices_used = [("vx", i+1, j), ("wxi", k+1, j-1)]

        if (score := (2 * parameters["Pi"] + coaxial_stacking(j-1, k+1, j, i, sequence)
                     + parameters["M"] + matrix_vx(k+1, j-1, matrix, sequence) 
                     + matrix_wxi.matrix_wxi(i+1, k, matrix, sequence))) < best_score:
            best_score = score
            matrices_used = [("vx", k+1, j-1), ("wxi", i+1, k)]

    for j_prime in range(i, j+1):
        for k in range(i, j_prime+1):
            for i_prime in range(i, k+1):

                if (score := (3 * parameters["Pi"] + coaxial_stacking(k, i_prime, k+1, j_prime, sequence)
                             + parameters["M"] + matrix_vx(i_prime, k, matrix, sequence) 
                             + matrix_vx(k+1, j_prime, matrix, sequence))) < best_score:
                    best_score = score
                    matrices_used = [("vx", i_prime, k), ("vx", k+1, j_prime)]


    # Non nested multiloop
    for r in range(i, j+1):
        for l in range(i, r+1):
            for k in range(i, l+1):

                if (score := (parameters["Pi_wave"] + parameters["M_wave"] + parameters["Gwi"]
                             + matrix_whx.matrix_whx(i+1, r, k, l, matrix, sequence) 
                             + matrix_whx.matrix_whx(k+1, j-1, l-1, r+1, matrix, sequence))) < best_score:
                    best_score = score
                    matrices_used = [("whx", i+1, r, k, l), ("whx", k+1, j-1, l-1, r+1)]

                if (score := (2 * parameters["Pi_wave"] + parameters["M_wave"] + parameters["Gwi"]
                             + coaxial_stacking_wave(i, j, i+1, r, sequence) 
                             + matrix_zhx.matrix_zhx(i+1, r, k, l, matrix, sequence)
                             + matrix_whx.matrix_whx(k+1, j-1, l-1, r+1, matrix, sequence))) < best_score:
                    best_score = score
                    matrices_used = [("zhx", i+1, r, k, l), ("whx", k+1, j-1, l-1, r+1)]

                if (score := (2 * parameters["Pi_wave"] + parameters["M_wave"] + parameters["Gwi"]
                             + coaxial_stacking_wave(j-1, k+1, j, i, sequence) 
                             + matrix_whx.matrix_whx(i+1, r, k, l, matrix, sequence)
                             + matrix_zhx.matrix_zhx(k+1, j-1, l-1, r+1, matrix, sequence))) < best_score:
                    best_score = score
                    matrices_used = [("whx", i+1, r, l, l), ("zhx", k+1, j-1, l-1, r+1)]

                if (score := (3 * parameters["Pi_wave"] + parameters["M_wave"] + parameters["Gwi"]
                             + coaxial_stacking_wave(l-1, r+1, l, k, sequence) 
                             + matrix_yhx.matrix_yhx(i+1, r, k, l, matrix, sequence)
                             + matrix_yhx.matrix_yhx(k+1, j-1, l-1, r+1, matrix, sequence))) < best_score:
                    best_score = score
                    matrices_used = [("yhx", i+1, r, k, l), ("yhx", k+1, j-1, l-1, r+1)]

    # End Recursions
    # #############################

    # Addition of the best value and matrices used in the matrix
    matrix["vx"][j][i] = (best_score, matrices_used)

    return best_score
