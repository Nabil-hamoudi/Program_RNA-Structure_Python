def create_matrices(n):
    """
    Creation of the seven triangular matrices
    Input:
        n: integer, the size of the sequence to process
    Output:
        dictionnary of the matrices
    """
    # 2D triangular matrices
    vx = [[None for i in range(j+1)] for j in range(n)]
    wx = [[None for i in range(j+1)] for j in range(n)]
    wxi = [[None for i in range(j+1)] for j in range(n)]

    # 4D triangular matrices
    vhx = [[[[None for i in range(k+1)] for k in range(l+1)] for l in range(j+1)] for j in range(n)]
    whx = [[[[None for i in range(k+1)] for k in range(l+1)] for l in range(j+1)] for j in range(n)]
    yhx = [[[[None for i in range(k+1)] for k in range(l+1)] for l in range(j+1)] for j in range(n)]
    zhx = [[[[None for i in range(k+1)] for k in range(l+1)] for l in range(j+1)] for j in range(n)]

    return {"vx" : vx, "wx" : wx, "wxi" : wxi, "vhx" : vhx, "whx" : whx, "yhx" : yhx, "zhx" : zhx}


def fill_matrices(matrix):
    """
    Fill the matrices with the initialization conditions
    Input:
        matrix: dictionnary of the matrices
    No output
    """
    # retrieve the size of the sequence
    n = len(matrix["vx"])

    # initialization for vx and wx
    for i in range(n):
        matrix["vx"][i][i] = (float('inf'), [])
        matrix["wx"][i][i] = (0, [])
        matrix["wxi"][i][i] = (0, [])

    #initialization for vhx, whx, yhx, zhx
    for j in range(n):
        for k in range(j+1):
            for i in range(k+1):

                # vhx
                matrix["vhx"][j][k][k][i] = (float('inf'), [])
                
                # yhx
                matrix["yhx"][j][k][k][i] = (float('inf'), [])
                
                # whx
                matrix["whx"][j][k][k][i] = matrix["wx"][j][i]
                matrix["whx"][j][j][i][i] = (float('inf'), [])
                # k+1 must be lower than j
                if k+1 <= j:
                    matrix["whx"][j][k+1][k][i] = matrix["wx"][j][i]
                
                # zhx
                matrix["zhx"][j][k][k][i] = matrix["vx"][j][i]
                # k+1 must be lower than j 
                if k+1 <= j:
                    matrix["zhx"][j][k+1][k][i] = matrix["vx"][j][i]
                    
