from parameters import *
from matrix_wxi import matrix_wxi
from matrix_whx import matrix_whx
from matrix_vx import matrix_vx
from matrix_zhx import matrix_zhx
from matrix_yhx import matrix_yhx


def matrix_vx(i, j):
    """
    Calculate the box (i,j) of the wx matrix and return its value.
    Entry: i and j: int as i <= j
    Exit: best score value
    """
    if (i > j):
        raise IndexError("Invalid index, i must be smaller or equal to j.")

    if vx[j][i] is not None:
        return vx[j][i]


    # #############################
    # Beginning Recursions

    # IS(1)
    if score := (parameters["EIS1"](i,j)) < best_score: best_score = score

    # IS(2)
    for l in range(i,j+1):
        for k in range(i, l+1):
            if score := (parameters["EIS2"](i, j, k, l) + matrix_vx(k, l)) < best_score: best_score = score

    # Nested Multiloop
    for k in range(i, j+1):
        if score := (parameters["Pi"] + parameters["M"] + matrix_wxi(i+1, k)
                     + matrix_wxi(k+1, j-1)) < best_score: best_score = score

        if score := (2 * parameters["Pi"] + coaxial_stacking(i, j, i+1, k)
                     + parameters["M"] + matrix_vx(i+1, k) + matrix_wxi(k+1, j-1)
                     ) < best_score: best_score = score

        if score := (2 * parameters["Pi"] + coaxial_stacking(j-1, k+1, j, i)
                     + parameters["M"] + matrix_vx(k+1, j-1) + matrix_wxi(i+1, k)
                     ) < best_score: best_score = score

    for j_prime in range(i, j+1):
        for k in range(i, j_prime+1):
            for i_prime in range(i, k+1):
                if score := (3 * parameters["Pi"] + coaxial_stacking(k, i_prime, k+1, j_prime)
                             + parameters["M"] + matrix_vx(i_prime, k) + matrix_vx(k+1, j_prime)
                             ) < best_score: best_score = score


    # Non nested multiloop
    for r in range(i, j+1):
        for l in range(i, r+1):
            for k in range(i, l+1):
                if score := (parameters["Pi_wave"] + parameters["M_wave"] + parameters["Gwi"]
                             + matrix_whx(i+1, r, k, l) + matrix_whx(k+1, j-1, l-1, r+1)
                             ) < best_score: best_score = score
         
                if score := (2 * parameters["Pi_wave"] + parameters["M_wave"] + parameters["Gwi"]
                             + coaxial_stacking_wave(i, j, i+1, r) + matrix_zhx(i+1, r, k, l)
                             + matrix_whx(k+1, j-1, l-1, r+1)) < best_score: best_score = score

                if score := (2 * parameters["Pi_wave"] + parameters["M_wave"] + parameters["Gwi"]
                             + coaxial_stacking_wave(j-1, k+1, j, i) + matrix_whx(i+1, r, k, l)
                             + matrix_zhx(k+1, j-1, l-1, r+1)) < best_score: best_score = score

                if score := (3 * parameters["Pi_wave"] + parameters["M_wave"] + parameters["Gwi"]
                             + coaxial_stacking_wave(l-1, r+1, l, k) + matrix_yhx(i+1, r, k, l)
                             + matrix_yhx(k+1, j-1, l-1, r+1)) < best_score: best_score = score

    # End Recursions
    # #############################

    # Addition of the best value in the matrix
    vx[j][i] = best_score

    return best_score
