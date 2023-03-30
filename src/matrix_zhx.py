from create_matrices import create_matrices


def matrix_zhx(i, j, k, l):
    """pipoupipoupipoupipoupipoupipou"""
    if (i > k) or (k > l) or (l > j):
        print(f"Error : invalid index.\n i = {i}, k = {k}, l = {l}, j= {j} ")
        exit(1)

    if zhx[j][l][k][i] is not None:
        return zhx[j][l][k][i]

