# creation matrices

def create_matrices(n):
    """creation of the six triangular matrices """
    # global vx, wx, vhx, whx, yhx, zhx
    vx = [[None for i in range(j+1)] for j in range(n)]
    wx = [[None for i in range(j+1)] for j in range(n)]
    wxi = [[None for i in range(j+1)] for j in range(n)]
    vhx = [[[[None for i in range(k+1)] for k in range(l+1)] for l in range(j+1)] for j in range(n)]
    whx = [[[[None for i in range(k+1)] for k in range(l+1)] for l in range(j+1)] for j in range(n)]
    yhx = [[[[None for i in range(k+1)] for k in range(l+1)] for l in range(j+1)] for j in range(n)]
    zhx = [[[[None for i in range(k+1)] for k in range(l+1)] for l in range(j+1)] for j in range(n)]

    return {"vx" : vx, "wx" : wx, "wxi" : wxi, "vhx" : vhx, "whx" : whx, "yhx" : yhx, "zhx" : zhx}


def fill_matrices():
    """fill the matrices with the initialization conditions"""
    n = len(vx)

    # initialization for vx and wx
    for i in range(n):
        vx[i][i] = float('inf')
        wx[i][i] = 0

    #initialization for vhx, whx, yhx, zhx
    for j in range(n):
        for k in range(j+1):
            for i in range(k+1):

                #vhx
                vhx[j][k][k][i] = float('inf')
                
                #yhx
                yhx[j][k][k][i] = float('inf')
                
                # whx
                whx[j][k][k][i] = wx[j][i]
                whx[j][j][i][i] = float('inf')
                #k+1 must be lower than j
                if k+1 <= j:
                    whx[j][k+1][k][i] = wx[j][i]
                
                #zhx
                zhx[j][k][k][i] = vx[j][i]
                #k+1 must be lower than j 
                if k+1 <= j:
                    zhx[j][k+1][k][i] = vx[j][i]
                

                
#for l in vx: print(l)
#for l in wx: print(l)
