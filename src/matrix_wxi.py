from parameters import *
from matrix_vx import matrix_vx
from matrix_whx import matrix_whx
from matrix_yhx import matrix_yhx


def matrix_wxi(i, j):
    """
    Calculate the box (i,j) of the wxi matrix and return its value.
    Entry: i and j: int as i <= j
    Exit: best score value
    """

    # Function input check
    if (i > j):
        raise NameError("Invalid index, i must be smaller or equal to j.")

    # Box already calculated ?
    if wxi[j][i] is not None:
        return wxi[j][i]

    best_score = float('inf')

    # #############################
    # Beginning Recursions

    # Paired (9)
    if score := (parameters["Pi"] + matrix_vx(i,j)) < best_score: best_score = score

    # Dangles
    if score := (dangle_Li(i, i+1, j-1) + dangle_Ri(j, i+1, j-1) + parameters["Pi"]
                 + matrix_vx(i+1, j-1)) < best_score: best_score = score

    if score := (dangle_Li(i, i+1, j) + parameters["Pi"] + matrix_vx(i+1, j)
                 ) < best_score: best_score = score

    if score := (dangle_Ri(j, i, j-1) + parameters["Pi"] + matrix_vx(i, j-1)
                 ) < best_score: best_score = score

    # Single stranded (9)
    if score := (parameters["Qi"] + matrix_wxi(i+1,j)) < best_score: best_score = score
    if score := (parameters["Qi"] + matrix_wxi(i, j-1)) < best_score: best_score = score

    # Nested Bifurcation (9 & 10)
    for k in range(i, j+1):
        if score := (matrix_wxi(i,k) + matrix_wxi(k+1, j)) < best_score: best_score = score

        if score := (coaxial_stacking(k, i, k+1, j) + matrix_vx(i, k) + matrix_vx(k+1, j)
                     ) < best_score: best_score = score

    # Non nested bifurcation (9)
    for r in range(i, j+1):
        for l in range(i, r+1):
            for k in range(i, l+1):
                if score := (parameters["Gwi"] + matrix_whx(i,r, k,l) + 
                             matrix_whx(k+1, j, l-1, r+1)) < best_score: best_score = score

                if score := (2 * parameters["Pi_wave"] + parameters["Gwi"] 
                             + coaxial_stacking_wave(l-1, r+1, l, k) + matrix_yhx(i, r, k, l)
                             + matrix_yhx(k+1, j, l-1, r+1)) < best_score: best_score = score

    # End Recursions
    # #############################

    # Addition of the best value in the matrix
    wxi[j][i] = best_score

    return best_score
