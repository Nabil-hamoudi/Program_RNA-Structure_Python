# import matrix_vhx
# import matrix_wxi
# import matrix_whx

# zhx(i, j : k, k + 1) = vx(i, j) Vk, i<=k<=j

def matrix_zhx(i, j, k, l):
    """docstring"""
    if (i > k) or (k > l) or (l > j):
        print(f"Error : invalid index.\n i = {i}, k = {k}, l = {l}, j= {j} ")
        exit(1)

    if zhx[j][l][k][i] is not None:
        return zhx[j][l][k][i]

    # initialization of the optimal score
    best_score = float('inf')

    # paired
    if score := (P_wave + matrix_vhx(i, j, k, l)) < best_score: best_score = score

    # single-stranded
    if score := (Q_wave + matrix_zhx(i, j, k-1, l)) < best_score: best_score = score
    if score := (Q_wave + matrix_zhx(i, j, k, l+1)) < best_score: best_score = score

    # nested bifurcations
    for r in range(i, k+1):
        if score := (matrix_zhx(i, j, r, l) + matrix_wxi(r+1, k)) < best_score: best_score = score

    for s in range(l, j+1):
        if score := (matrix_zhx(i, j, k, s) + matrix_wxi(l, s-1)) < best_score: best_score = score

    for r in range(i, k+1):
        for s in range(l, j+1):
            if score := (EIS2(i, j, r, s) + matrix_zhx(r, s, k, l)) < best_score: best_score = score

    if score := (P_wave + M_wave + matrix_whx(i + 1, j - 1, k, l)) < best_score: best_score = score

    # store the best score in the matrix and return it 
    zhx[j][l][k][i] = best_score
    return best_score
