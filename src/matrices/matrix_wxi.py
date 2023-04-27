from parameters import *
from matrices import matrix_vx, matrix_whx, matrix_yhx


def matrix_wxi(i, j, matrix, sequence):
    """
    Calculate the box (i,j) of the wxi matrix and return its value.
    Entry: i and j: int as i <= j
    Exit: best score value
    """

    # Function input check
    if (i > j):
        return float('inf')

    # Box already calculated ?
    if matrix["wxi"][j][i] is not None:
        return matrix["wxi"][j][i][0]
    matrix["wxi"][j][i] = (float('inf'), [])

     # initialization of the optimal score
    best_score = float('inf')

    # creation of the list for traceback
    matrices_used = []

    # #############################
    # Beginning Recursions

    # Paired
    if (score := (parameters["Pi"] + matrix_vx.matrix_vx(i,j, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("vx", i, j)]


    # Dangles
    if (score := (dangle_Li(i, i+1, j-1, sequence) + dangle_Ri(j, i+1, j-1, sequence) + parameters["Pi"]
                 + matrix_vx.matrix_vx(i+1, j-1, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("vx", i+1, j-1)]

    if (score := (dangle_Li(i, i+1, j, sequence) + parameters["Pi"] 
                  + matrix_vx.matrix_vx(i+1, j, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("vx", i+1, j)]

    if (score := (dangle_Ri(j, i, j-1, sequence) + parameters["Pi"] 
                  + matrix_vx.matrix_vx(i, j-1, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("vx", i, j-1)]


    # Single stranded
    if (score := (parameters["Qi"] + matrix_wxi(i+1,j, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("wxi", i+1, j)]

    if (score := (parameters["Qi"] + matrix_wxi(i, j-1, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("wxi", i, j-1)]


    # Nested Bifurcation
    for k in range(i, j+1):
        if (score := (matrix_wxi(i,k, matrix, sequence) + matrix_wxi(k+1, j, matrix, sequence))) < best_score:
            best_score = score
            matrices_used = [("wxi", i, k), ("wxi", k+1, j)]

        if (score := (coaxial_stacking(k, i, k+1, j, sequence) + matrix_vx.matrix_vx(i, k, matrix, sequence) 
                      + matrix_vx.matrix_vx(k+1, j, matrix, sequence))) < best_score:
            best_score = score
            matrices_used = [("vx", i, k), ("vx", k+1, j)]


    # Non nested bifurcation
    for r in range(i, j+1):
        for l in range(i, r+1):
            for k in range(i, l+1):

                if (score := (parameters["Gwi"] + matrix_whx.matrix_whx(i,r, k,l, matrix, sequence) + 
                             matrix_whx.matrix_whx(k+1, j, l-1, r+1, matrix, sequence))) < best_score:
                    best_score = score
                    matrices_used = [("whx", i, r, k, l), ("whx", k+1, j, l-1, r+1)]

                if (score := (2 * parameters["Pi_wave"] + parameters["Gwi"] 
                             + coaxial_stacking_wave(l-1, r+1, l, k, sequence) 
                              + matrix_yhx.matrix_yhx(i, r, k, l, matrix, sequence)
                             + matrix_yhx.matrix_yhx(k+1, j, l-1, r+1, matrix, sequence))) < best_score:
                    best_score = score
                    matrices_used = [("yhx", i, r, k, l), ("yhx", k+1, j, l-1, r+1)]

    # End Recursions
    # #############################

    # Addition of the best value and matrices used in the matrix
    matrix["wxi"][j][i] = (best_score, matrices_used)
    return best_score
