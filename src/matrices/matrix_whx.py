from parameters import *
from matrices import matrix_vhx, matrix_zhx, matrix_yhx, matrix_wxi, matrix_vx, matrix_wx


# matrix whx

def matrix_whx(i, j, k, l, matrix, sequence):
    """
    return the value of the gap matrix whx at the given indices
    """
    # check indices
    if (i > k) or (k > l) or (l > j):
        return float('inf')

    if matrix["whx"][j][l][k][i] is not None:
        return matrix["whx"][j][l][k][i][0]
    matrix["whx"][j][l][k][i] = (float('inf'), [])

    if (k+1) == l:
        matrix["whx"][j][l][k][i] = (matrix_wx.matrix_wx(i, j, matrix, sequence), [("wx", i, j)])
        return matrix_wx.matrix_wx(i, j, matrix, sequence)


    # initialization of the optimal score
    best_score = float('inf')

    # initialization of the list for the traceback
    matrices_used = []

    ## search for a better score ##

    # paired
    if (score := (2 * parameters["P_wave"] + matrix_vhx.matrix_vhx(i, j, k, l, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("vhx", i, j, k, l)]
                          
    if (score := (parameters["P_wave"] + matrix_zhx.matrix_zhx(i, j, k, l, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("zhx", i, j, k, l)]
                       
    if (score := (parameters["P_wave"] + matrix_yhx.matrix_yhx(i, j, k, l, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("yhx", i, j, k, l)]


    # single-stranded
    if (score := (parameters["Q_wave"] + matrix_whx(i+1, j, k, l, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("whx", i+1, j, k, l)]

    if (score := (parameters["Q_wave"] + matrix_whx(i, j-1, k, l, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("whx", i, j-1, k, l)]

    if (score := (parameters["Q_wave"] + matrix_whx(i, j, k-1, l, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("whx", i, j, k-1, l)]

    if (score := (parameters["Q_wave"] + matrix_whx(i, j, k, l+1, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("whx", i, j, k, l+1)]


    # dangles
    if (score := parameters["L_wave"](i, i+1, j, sequence) + parameters["R_wave"](k, k-1, l, sequence) \
            + (2 * parameters["P_wave"]) + matrix_vhx.matrix_vhx(i+1, j, k-1, l, matrix, sequence)) < best_score:
        best_score = score
        matrices_used = [("vhx", i+1, j, k-1, l)]

    if (score := parameters["L_wave"](l-1, k, l, sequence) + parameters["R_wave"](j, i, j-1, sequence) \
            + (2 * parameters["P_wave"]) + matrix_vhx.matrix_vhx(i, j-1, k, l+1, matrix, sequence)) < best_score:
        best_score = score
        matrices_used = [("vhx", i, j-1, k, l+1)]

    if (score := (parameters["L_wave"](i, i+1, j, sequence) + parameters["L_wave"](l, k, l+1, sequence)) \
            + (2 * parameters["P_wave"]) + matrix_vhx.matrix_vhx(i+1, j, k, l+1, matrix, sequence)) < best_score:
        best_score = score
        matrices_used = [("vhx", i+1, j, k, l+1)]

    if (score := (parameters["R_wave"](k, k-1, l, sequence) + parameters["R_wave"](j, i, j-1, sequence)) \
            + (2 * parameters["P_wave"]) + matrix_vhx.matrix_vhx(i, j-1, k-1, l, matrix, sequence)) < best_score:
        best_score = score
        matrices_used = [("vhx", i, j-1, k-1, l)]

    if (score := parameters["L_wave"](i, i+1, j-1, sequence) + (parameters["R_wave"](k, k-1, l, sequence) \
            + parameters["R_wave"](j, i+1, j-1, sequence)) + (2 * parameters["P_wave"]) \
            + matrix_vhx.matrix_vhx(i+1, j-1, k-1, l, matrix, sequence)) < best_score:
        best_score = score
        matrices_used = [("vhx", i+1, j-1, k-1, l)]

    if (score := (parameters["L_wave"](i, i+1, j, sequence) + parameters["L_wave"](l, k-1, l+1, sequence)) \
            + parameters["R_wave"](k, k-1, l+1, sequence) + (2 * parameters["P_wave"]) \
            + matrix_vhx.matrix_vhx(i+1, j, k-1, l+1, matrix, sequence)) < best_score:
        best_score = score
        matrices_used = [("vhx", i+1, j, k-1, l+1)]

    if (score := (parameters["L_wave"](i, i+1, j-1, sequence) + parameters["L_wave"](l, k, l+1, sequence)) \
            + parameters["R_wave"](j, i+1, j-1, sequence) + (2 * parameters["P_wave"]) \
            + matrix_vhx.matrix_vhx(i+1, j-1, k, l+1, matrix, sequence)) < best_score:
        best_score = score
        matrices_used = [("vhx", i+1, j-1, k, l+1)]

    if (score := parameters["L_wave"](l, k-1, l+1, sequence) + (parameters["R_wave"](k, k-1, l+1, sequence) \
            + parameters["R_wave"](j, i, j-1, sequence)) + (2 * parameters["P_wave"]) \
            + matrix_vhx.matrix_vhx(i, j-1, k-1, l+1, matrix, sequence)) < best_score:
        best_score = score
        matrices_used = [("vhx", i, j-1, k-1, l+1)]

    if (score := (parameters["L_wave"](i, i+1, j-1, sequence) + parameters["L_wave"](l, k-1, l+1, sequence)) \
            + (parameters["R_wave"](k, k-1, l+1, sequence) + parameters["R_wave"](j, i+1, j-1, sequence)) \
            + (2 * parameters["P_wave"]) + matrix_vhx.matrix_vhx(i+1, j-1, k-1, l+1, matrix, sequence)) < best_score:
        best_score = score
        matrices_used = [("vhx", i+1, j-1, k-1, l+1)]

    if (score := parameters["L_wave"](i, i+1, j-1, sequence) + parameters["R_wave"](j, i+1, j-1, sequence) \
            + parameters["P_wave"] + matrix_zhx.matrix_zhx(i+1, j-1, k, l, matrix, sequence)) < best_score:
        best_score = score
        matrices_used = [("zhx", i+1, j-1, k, l)]
    
    if (score := parameters["L_wave"](i, i+1, j, sequence) + parameters["P_wave"] \
            + matrix_zhx.matrix_zhx(i+1, j, k, l, matrix, sequence)) < best_score:
        best_score = score
        matrices_used = [("zhx", i+1, j, k, l)]

    if (score := parameters["R_wave"](j, i, j-1, sequence) + parameters["P_wave"] \
            + matrix_zhx.matrix_zhx(i, j-1, k, l, matrix, sequence)) < best_score:
        best_score = score
        matrices_used = [("zhx", i, j-1, k, l)]
    
    if (score := parameters["L_wave"](l, k-1, l+1, sequence) + parameters["R_wave"](k, k-1, l+1, sequence) \
            + parameters["P_wave"] + matrix_yhx.matrix_yhx(i, j, k-1, l+1, matrix, sequence)) < best_score:
        best_score = score
        matrices_used = [("yhx", i, j, k-1, l+1)]
    
    if (score := parameters["R_wave"](k, k-1, l, sequence) + parameters["P_wave"] \
            + matrix_yhx.matrix_yhx(i, j, k-1, l+1, matrix, sequence)) < best_score:
        best_score = score
        matrices_used = [("yhx", i, j, k-1, l+1)]
    
    if (score := parameters["L_wave"](l, k, l+1, sequence) + parameters["P_wave"] \
            + matrix_yhx.matrix_yhx(i, j, k, l+1, matrix, sequence)) < best_score:
        best_score = score
        matrices_used = [("yhx", i, j, k, l+1)]


    # nested bifurcations
    if (score := (matrix_wxi.matrix_wxi(i, k, matrix, sequence) + matrix_wxi.matrix_wxi(l, j, matrix, sequence))) < best_score:
        best_score = score
        matrices_used = [("wxi", l, j), ("wxi", i, k)]


    for r in range(i, k+1):

        if (score := (matrix_wxi.matrix_wxi(i, r, matrix, sequence) + matrix_whx(r+1, j, k, l, matrix, sequence))) < best_score:
            best_score = score
            matrices_used = [("wxi", i, r), ("whx", r+1, j, k, l)]
        
        if (score := 2 * parameters["P_wave"] + coaxial_stacking(r, i, r+1, j, sequence) \
                + matrix_vx.matrix_vx(i, r, matrix, sequence) + matrix_zhx.matrix_zhx(r+1, j, k, l, matrix, sequence)) < best_score:
            best_score = score
            matrices_used = [("vx", i, r), ("zhx", r+1, j, k, l)]

        if (score := (matrix_wxi.matrix_wxi(r+1, k, matrix, sequence) + matrix_whx(i, j, r, l, matrix, sequence))) < best_score:
            best_score = score
            matrices_used = [("wxi", r+1, k), ("whx", i, j, r, l)]


    for s in range(l, j+1):

        if (score := 2 * parameters["P_wave"] + coaxial_stacking(r, l, r+1, k, sequence) \
                + matrix_yhx.matrix_yhx(i, j, r, l, matrix, sequence) + matrix_vx.matrix_vx(r+1, k, matrix, sequence)) < best_score:
            best_score = score
            matrices_used = [("vhx", i, j, r, l), ("vx", r+1, k)]

        if (score := (matrix_wxi.matrix_wxi(s+1, j, matrix, sequence) + matrix_whx(i, s, k, l, matrix, sequence))) < best_score:
            best_score = score
            matrices_used = [("wxi", s+1, j), ("whx", i, s, j, l)]

        if (score := 2 * parameters["P_wave"] + coaxial_stacking(s, i, s+1, j, sequence) \
                + matrix_zhx.matrix_zhx(i, s, k, l, matrix, sequence) + matrix_vx.matrix_vx(s+1, j, matrix, sequence)) < best_score:
            best_score = score
            matrices_used = [("zhx", i, s, k, l), ("vx", s+1, j)]

        if (score := (matrix_wxi.matrix_wxi(l, s, matrix, sequence) + matrix_whx(i, j, k, s+1, matrix, sequence))) < best_score:
            best_score = score
            matrices_used = [("wxi", l, s), ("whx", i, j, k, s+1)]


    for s in range(l, j+1):
        for r in range(i, k+1):

            if (score := 2 * parameters["P_wave"] + coaxial_stacking(s, l, s+1, k, sequence) \
                    + matrix_yhx.matrix_yhx(i, j, k, s+1, matrix, sequence) + matrix_vx.matrix_vx(l, s, matrix, sequence)) < best_score:
                best_score = score
                matrices_used = [("yhx", i, j, k, s+1), ("vx", l, s)]

            if (score := (matrix_yhx.matrix_yhx(i, j, r, s, matrix, sequence) +  matrix_zhx.matrix_zhx(r, s,  k, l, matrix, sequence))) < best_score:
                best_score = score
                matrices_used = [("yhx", i, j, r, s), ("zhx", r, s, k, l)]
            
            if (score := (parameters["M_wave"] + matrix_whx(i, j, r, s, matrix, sequence) \
                    + matrix_whx(r+1, s-1, k, l, matrix, sequence))) < best_score:
                best_score = score
                matrices_used = [("whx", i, j, r, s), ("whx", r+1, s-1, k, l)]


    # non-nested bifurcations
            if (score := (parameters["Gwh"] + matrix_whx(i, s, r, l, matrix, sequence) \
                    + matrix_whx(r+1, j, k, s+1, matrix, sequence))) < best_score:
                best_score = score
                matrices_used = [("whx", i, s, r, l), ("whx", r+1, j, k, s+1)]


    for s_prime in range(l, j+1):
        for s in range(l, s_prime+1):
            for r_prime in range(i, k+1):
                for r in range(i, r_prime+1):

                    if (score := (parameters["Gwh"] + matrix_whx(i, s_prime, k, s, matrix, sequence) \
                            + matrix_whx(l, j, s-1, s_prime+1, matrix, sequence))) < best_score:
                        best_score = score
                        matrices_used = [("whx", i, s_prime, k, s), ("whx", i, j, s-1, s_prime+1)]
                    
                    if (score := 2 * parameters["P_wave"] + parameters["Gwh"] \
                            + coaxial_stacking_wave(s_prime, i, s_prime + 1, s-1, sequence) \
                            + matrix_zhx.matrix_zhx(i, s_prime, k, s, matrix, sequence) \
                            + matrix_yhx.matrix_yhx(l, j, s-1, s_prime+1, matrix, sequence)) < best_score:
                        best_score = score
                        matrices_used = [("zhx", i, s_prime, k, s), ("yhx", l, j, s-1, s_prime+1)]

                    if (score := 2 * parameters["P_wave"] + parameters["Gwh"] \
                            + coaxial_stacking_wave(s-1, s_prime + 1, s, k, sequence) \
                            + matrix_yhx.matrix_yhx(i, s_prime, k, s, matrix, sequence) \
                            + matrix_yhx.matrix_yhx(l, j, s-1, s_prime+1, matrix, sequence)) < best_score:
                        best_score = score
                        matrices_used = [("yhx", i, s_prime, k, s), ("yhx", l, j, s-1, s_prime+1)]

                    if (score := parameters["Gwh"] + matrix_whx(r, j, r_prime, l, matrix, sequence) \
                            +  matrix_whx(i, k, r-1, r_prime+1, matrix, sequence)) < best_score:
                        best_score = score
                        matrices_used = [("whx", r, j, r_prime, l), ("whx", i, k, r-1, r_prime+1)]

                    if (score := 2 * parameters["P_wave"] + parameters["Gwh"] \
                            + coaxial_stacking_wave(r-1, r_prime+1, r, j, sequence) \
                            + matrix_zhx.matrix_zhx(r, j, r_prime, l, matrix, sequence) \
                            + matrix_yhx.matrix_yhx(i, k, r-1, r_prime+1, matrix, sequence)) < best_score:
                        best_score = score
                        matrices_used = [("zhx", r, j, r_prime, l), ("yhx", i, k, r-1, r_prime+1)]

                    if (score := 2 * parameters["P_wave"] + parameters["Gwh"] \
                            + coaxial_stacking_wave(r_prime, l, r_prime + 1, r-1, sequence) \
                            + matrix_yhx.matrix_yhx(r, j, r_prime, l, matrix, sequence) \
                            + matrix_yhx.matrix_yhx(i, k, r-1, r_prime+1, matrix, sequence)) < best_score:
                        best_score = score
                        matrices_used = [("yhx", r, j, r_prime, l), ("yhx", i, k, r-1, r_prime+1)]



    # store the best score in the matrix and return it 
    matrix["whx"][j][l][k][i] = (best_score, matrices_used)
    return best_score


