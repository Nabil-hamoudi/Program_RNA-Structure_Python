# Mettre les import

def matrix_wx(i, j):
    """
    Calculate the box (i,j) of the wx matrix and return its value.
    Entry: i and j: int as i <= j
    Exit: best score value
    """

    # Function input check
    if (i > j):
        raise NameError("Invalid index, i must be smaller or equal to j.")

    # Box already calculated ? 
    if wx[j][i] is not None:
        return wx[j][i]

    best_score = float('inf')

    # Paired (9)
    if score := (P + matrix_vx(i,j)) < best_score: best_score = score

    # Single stranded (9)
    if score := (Q + matrix_wx(i+1,j)) < best_score: best_score = score
    if score := (Q + matrix_wx(i, j-1)) < best_score: best_score = score

    # Nested Bifurcation (9 & 10)
    for k in range(i, j+1):
        if score := (matrix_wx(i,k) + matrix_wx(k+1, j)) < best_score: best_score = score

    # Non nested bifurcation (9)
    for r in range(i, j+1):
        for l in range(i, r+1):
            for k in range(i, l+1):
                if score := (Gw + matrix_whx(i,r, k,l) + matrix_whx(k+1, j, l-1, r+1)) < best_score: best_score = score


    # Coaxial (11)
    if score := (matrix_vx(i, k) + matrix_vx(k+1, j) + C(k, i, k+1, j)) < best_score: best_score = score

    # Dangle (12)
    # Pas fait

    # Addition of the best value in the matrix
    wx[j][i] = best_score

    return best_score