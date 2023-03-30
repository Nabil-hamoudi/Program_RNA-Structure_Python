# Importer les matrices

def matrix_vx(i, j):
    """
    Calculate the box (i,j) of the wx matrix and return its value.
    Entry: i and j: int as i <= j
    Exit: best score value
    """
    if (i > j):
        raise NameError("Invalid index, i must be smaller or equal to j.")

    if vx[j][i] is not None:
        return wx[j][i]

    # IS(1)
    if score := (EIS1(i,j)) < best_score: best_score = score

    # IS(2)
    for l in range(i,j+1):
        for k in range(i, l+1):
            if score := (EIS2(i, j, k, l) + matrix_vx(k, l)) < best_score: best_score = score

    # Nested Multiloop
    for k in range(i, j+1):
        if score := (Pi + M + matrix_wxi(i+1, k) + matrix_wxi(k+1, j-1)) < best_score: best_score = score

    # Non nested multiloop
    for r in range(i, j+1):
        for l in range(i, r+1):
            for k in range(i, l+1):
                if score := (Pi_wave + M_wave + Gwi + matrix_whx(i+1, r, k, l) + matrix_whx(k+1, j-1, l-1, r+1)) < best_score: best_score = score

    # Addition of the best value in the matrix
    vx[j][i] = best_score
   
    return best_score
