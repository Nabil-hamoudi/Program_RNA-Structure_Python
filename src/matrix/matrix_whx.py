from parameters import *
import matrix_vhx
import matrix_zhx
import matrix_yhx
import matrix_wxi
import matrix_vx
import matrix_wx

# matrix whx

def matrix_whx(i, j, k, l, matrix, sequence):
    """return the value of the gap matrix whx at the given indices"""
    # check indices
    if (i > k) or (k > l) or (l > j):
        #print(f"Error : invalid index.\n i = {i}, k = {k}, l = {l}, j= {j} ")
        # exit(1)
        return float('inf')

    if matrix["whx"][j][l][k][i] is not None:
        return matrix["whx"][j][l][k][i]


    if (k+1) == l:
        matrix["whx"][j][l][k][i] = matrix_wx.matrix_wx(i, j, matrix, sequence)
        return matrix_wx.matrix_wx(i, j, matrix, sequence)


    # initialization of the optimal score
    best_score = float('inf')

    
    # search for a better score
    
    # paired
    if score := (2 * parameters["P_wave"] + matrix_vhx.matrix_vhx(i, j, k, l, matrix, sequence)) < best_score: best_score = score
    if score := (parameters["P_wave"] + matrix_zhx.matrix_zhx(i, j, k, l, matrix, sequence)) < best_score: best_score = score
    if score := (parameters["P_wave"] + matrix_yhx.matrix_yhx(i, j, k, l, matrix, sequence)) < best_score: best_score = score

    # single-stranded
    if score := (parameters["Q_wave"] + matrix_whx(i+1, j, k, l, matrix, sequence)) < best_score: best_score = score
    if score := (parameters["Q_wave"] + matrix_whx(i, j-1, k, l, matrix, sequence)) < best_score: best_score = score
    if score := (parameters["Q_wave"] + matrix_whx(i, j, k-1, l, matrix, sequence)) < best_score: best_score = score
    if score := (parameters["Q_wave"] + matrix_whx(i, j, k, l+1, matrix, sequence)) < best_score: best_score = score


    # dangles 
    if score := parameters["L_wave"](i, i+1, j) + parameters["R_wave"](k, k-1, l) \
            + (2 * parameters["P_wave"]) + matrix_vhx.matrix_vhx(i+1, j, k-1, l, matrix, sequence) < best_score:
                best_score = score

    if score := parameters["L_wave"](l-1, k, l) + parameters["R_wave"](j, i, j-1) \
            + (2 * parameters["P_wave"]) + matrix_vhx.matrix_vhx(i, j-1, k, l+1, matrix, sequence) < best_score:
                best_score = score
    
    if score := (parameters["L_wave"](i, i+1, j) + parameters["L_wave"](l, k, l+1)) \
            + (2 * parameters["P_wave"]) + matrix_vhx.matrix_vhx(i+1, j, k, l+1, matrix, sequence) < best_score:
                best_score = score
    
    if score := (parameters["R_wave"](k, k-1, l) + parameters["R_wave"](j, i, j-1)) \
            + (2 * parameters["P_wave"]) + matrix_vhx.matrix_vhx(i, j-1, k-1, l, matrix, sequence) < best_score:
                best_score = score
    
    if score := parameters["L_wave"](i, i+1, j-1) + (parameters["R_wave"](k, k-1, l) \
            + parameters["R_wave"](j, i+1, j-1)) + (2 * parameters["P_wave"]) \
            + matrix_vhx.matrix_vhx(i+1, j-1, k-1, l, matrix, sequence) < best_score: best_score = score
    
    if score := (parameters["L_wave"](i, i+1, j) + parameters["L_wave"](l, k-1, l+1)) \
            + parameters["R_wave"](k, k-1, l+1) + (2 * parameters["P_wave"]) \
            + matrix_vhx.matrix_vhx(i+1, j, k-1, l+1, matrix, sequence) < best_score: best_score = score
    
    if score := (parameters["L_wave"](i, i+1, j-1) + parameters["L_wave"](l, k, l+1)) \
            + parameters["R_wave"](j, i+1, j-1) + (2 * parameters["P_wave"]) \
            + matrix_vhx.matrix_vhx(i+1, j-1, k, l+1, matrix, sequence) < best_score: best_score = score
    
    if score := parameters["L_wave"](l, k-1, l+1) + (parameters["R_wave"](k, k-1, l+1) \
            + parameters["R_wave"](j, i, j-1)) + (2 * parameters["P_wave"]) \
            + matrix_vhx.matrix_vhx(i, j-1, k-1, l+1, matrix, sequence) < best_score: best_score = score
    
    if score := (parameters["L_wave"](i, i+1, j-1) + parameters["L_wave"](l, k-1, l+1)) \
            + (parameters["R_wave"](k, k-1, l+1) + parameters["R_wave"](j, i+1, j-1)) \
            + (2 * parameters["P_wave"]) + matrix_vhx.matrix_vhx(i+1, j-1, k-1, l+1, matrix, sequence) < best_score:
                best_score = score

    if score := parameters["L_wave"](i, i+1, j-1) + parameters["R_wave"](j, i+1, j-1) \
            + parameters["P_wave"] + matrix_zhx.matrix_zhx(i+1, j-1, k, l, matrix, sequence) < best_score:
                best_score = score
    
    if score := parameters["L_wave"](i, i+1, j) + parameters["P_wave"] \
            + matrix_zhx.matrix_zhx(i+1, j, k, l, matrix, sequence) < best_score: best_score = score

    if score := parameters["R_wave"](j, i, j-1) + parameters["P_wave"] \
            + matrix_zhx.matrix_zhx(i, j-1, k, l, matrix, sequence) < best_score: best_score = score
    
    if score := parameters["L_wave"](l, k-1, l+1) + parameters["R_wave"](k, k-1, l+1) \
            + parameters["P_wave"] + matrix_yhx.matrix_yhx(i, j, k-1, l+1, matrix, sequence) < best_score:
                best_score = score
    
    if score := parameters["R_wave"](k, k-1, l) + parameters["P_wave"] \
            + matrix_yhx.matrix_yhx(i, j, k-1, l+1, matrix, sequence) < best_score: best_score = score
    
    if score := parameters["L_wave"](l, k, l+1) + parameters["P_wave"] \
            + matrix_yhx.matrix_yhx(i, j, k, l+1, matrix, sequence) < best_score: best_score = score




    # nested bifurcations
    if score := (matrix_wxi.matrix_wxi(i, k, matrix, sequence) + matrix_wxi.matrix_wxi(l, j, matrix, sequence)) < best_score: best_score = score


    for r in range(i, k+1):
        if score := (matrix_wxi.matrix_wxi(i, r, matrix, sequence) + matrix_whx(r+1, j, k, l, matrix, sequence)) < best_score: best_score = score
        
        if score := 2 * parameters["P_wave"] + coaxial_stacking(r, i, r+1, j) \
                + matrix_vx.matrix_vx(i, r, matrix, sequence) + matrix_zhx.matrix_zhx(r+1, j, k, l, matrix, sequence) < best_score: best_score = score

        if score := (matrix_wxi.matrix_wxi(r+1, k, matrix, sequence) + matrix_whx(i, j, r, l, matrix, sequence)) < best_score: best_score = score


    for s in range(l, j+1):
        if score := 2 * parameters["P_wave"] + coaxial_stacking(r, l, r+1, k) \
                + matrix_yhx.matrix_yhx(i, j, r, l, matrix, sequence) + matrix_vx.matrix_vx(r+1, k, matrix, sequence) < best_score: best_score = score

        if score := (matrix_wxi.matrix_wxi(s+1, j, matrix, sequence) + matrix_whx(i, s, k, l, matrix, sequence)) < best_score: best_score = score

        if score := 2 * parameters["P_wave"] + coaxial_stacking(s, i, s+1, j) \
                + matrix_zhx.matrix_zhx(i, s, k, l, matrix, sequence) + matrix_vx.matrix_vx(s+1, j, matrix, sequence) < best_score: best_score = score

        if score := (matrix_wxi.matrix_wxi(l, s, matrix, sequence) + matrix_whx(i, j, k, s+1, matrix, sequence)) < best_score: best_score = score


    for s in range(l, j+1):
        for r in range(i, k+1):
            if score := 2 * parameters["P_wave"] + coaxial_stacking(s, l, s+1, k) \
                    + matrix_yhx.matrix_yhx(i, j, k, s+1, matrix, sequence) + matrix_vx.matrix_vx(l, s, matrix, sequence) < best_score: best_score = score

            if score (matrix_yhx.matrix_yhx(i, j, r, s, matrix, sequence) +  matrix_zhx.matrix_zhx(r, s,  k, l, matrix, sequence)) < best_score: best_score = score
            
            if score := (parameters["M_wave"] + matrix_whx(i, j, r, s, matrix, sequence) \
                    + matrix_whx(r+1, s-1, k, l, matrix, sequence)) < best_score: best_score = score


    # non-nested bifurcations
            if score := (parameters["Gwh"] + matrix_whx(i, s, r, l, matrix, sequence) \
                    + matrix_whx(r+1, j, k, s+1, matrix, sequence)) < best_score: best_score = score


    for s_prime in range(l, j+1):
        for s in range(l, s_prime+1):
            for r_prime in range(i, k+1):
                for r in range(i, r_prime+1):
                    if score := (parameters["Gwh"] + matrix_whx(i, s_prime, k, s, matrix, sequence) \
                            + matrix_whx(l, j, s-1, s_prime+1, matrix, sequence)) < best_score: best_score = score
                    
                    if score := 2 * parameters["P_wave"] + parameters["Gwh"] \
                            + coaxial_stacking_wave(s_prime, i, s_prime + 1, s-1) \
                            + matrix_zhx.matrix_zhx(i, s_prime, k, s, matrix, sequence) + matrix_yhx.matrix_yhx(l, j, s-1, s_prime + 1, matrix, sequence) \
                            < best_score: best_score = score

                    if score := 2 * parameters["P_wave"] + parameters["Gwh"] \
                            + coaxial_stacking_wave(s-1, s_prime + 1, s, k) \
                            + matrix_yhx.matrix_yhx(i, s_prime, k, s, matrix, sequence) + matrix_yhx.matrix_yhx(l, j, s-1, s_prime + 1, matrix, sequence) \
                            < best_score: best_score = score

                    if score := parameters["Gwh"] + matrix_whx(r, j, r_prime, l, matrix, sequence) \
                            +  matrix_whx(i, k, r-1, r_prime+1, matrix, sequence) < best_score: best_score = score

                    if score := 2 * parameters["P_wave"] + parameters["Gwh"] \
                            + coaxial_stacking_wave(r-1, r_prime+1, r, j) \
                            + matrix_zhx.matrix_zhx(r, j, r_prime, l, matrix, sequence) + matrix_yhx.matrix_yhx(i, k, r-1, r_prime + 1, matrix, sequence) \
                            < best_score: best_score = score

                    if score := 2 * parameters["P_wave"] + parameters["Gwh"] \
                            + coaxial_stacking_wave(r_prime, l, r_prime + 1, r-1) \
                            + matrix_yhx.matrix_yhx(r, j, r_prime, l, matrix, sequence) + matrix_yhx.matrix_yhx(i, k, r-1, r_prime + 1, matrix, sequence) \
                            < best_score: best_score = score



    # store the best score in the matrix and return it 
    matrix["whx"][j][l][k][i] = best_score
    return best_score

