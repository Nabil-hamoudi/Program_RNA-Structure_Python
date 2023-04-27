from parameters import *
from matrices import matrix_vx, matrix_yhx, matrix_whx


def matrix_wx(i, j, matrix, sequence):
    """
    Calculate the box (i,j) of the wx matrix and return its value.
    Entry: i and j: int as i <= j
    Exit: best score value
    """

    # Function input check
    if (i > j):
        return float('inf')

    # Box already calculated ? 
    if matrix["wx"][j][i] is not None:
        return matrix["wx"][j][i][0]
    matrix["wx"][j][i] = (float('inf'), [])

    # initialisation of the optimal score
    best_score = float('inf')

    # creation of the list for traceback
    matrices_used = []

    # #############################
    # Beginning Recursions

    # Paired (9)
    if (score := (parameters["P"] + matrix_vx.matrix_vx(i,j, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("vx", i, j)]

    # Dangles
    if (score := (dangle_L(i, i+1, j-1, sequence) + dangle_R(j, i+1, j-1, sequence) + parameters["P"]
                 + matrix_vx.matrix_vx(i+1, j-1, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("vx", i+1, j-1)]


    if (score := (dangle_L(i, i+1, j, sequence) + parameters["P"]
                  + matrix_vx.matrix_vx(i+1, j, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("vx", i+1, j)]


    if (score := (dangle_R(j, i, j-1, sequence) + parameters["P"]
                  + matrix_vx.matrix_vx(i, j-1, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("vx", i, j-1)]


    # Single stranded (9)
    if (score := (parameters["Q"] + matrix_wx(i+1, j, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("wx", i+1, j)]

    if (score := (parameters["Q"] + matrix_wx(i, j-1, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("wx", i, j-1)]

    # Nested Bifurcation (9 & 10)
    for k in range(i, j+1):
        if (score := (matrix_wx(i, k, matrix, sequence) + matrix_wx(k+1, j, matrix, sequence))) < best_score:
            best_score = score
            matrices_used = [("wx", i, k), ("wx", k+1, j)]

        if (score := (coaxial_stacking(k, i, k+1, j, sequence) + matrix_vx.matrix_vx(i, k, matrix, sequence) 
                      + matrix_vx.matrix_vx(k+1, j, matrix, sequence))) < best_score:
            best_score = score
            matrices_used = [("vx", i, k), ("vx", k+1, j)]


    # Non nested bifurcation (pseudoknot) (9)
    for r in range(i, j+1):
        for l in range(i, r+1):
            for k in range(i, l+1):

                if (score := (parameters["Gw"] + matrix_whx.matrix_whx(i,r, k,l, matrix, sequence) +
                             matrix_whx.matrix_whx(k+1, j, l-1, r+1, matrix, sequence))) < best_score:
                    best_score = score
                    matrices_used = [("whx", i, r, k, l), ("whx", k+1, j, l-1, r+1)]

                if (score := (2 * parameters["P_wave"] + parameters["Gw"] 
                             + coaxial_stacking_wave(l-1, r+1, l, k, sequence) 
                             + matrix_yhx.matrix_yhx(i, r, k, l, matrix, sequence)
                             + matrix_yhx.matrix_yhx(k+1, j, l-1, r+1, matrix, sequence))) < best_score:
                    best_score = score
                    matrices_used = [("yhx", i, r, k, l), ("yhx", k+1, j, l-1, r+1)]

    # End Recursions
    # #############################

    # Addition of the best value in the matrix
    matrix["wx"][j][i] = (best_score, matrices_used)

    return best_score
