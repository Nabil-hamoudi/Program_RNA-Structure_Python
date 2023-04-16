# parameters : table 2 & 3

# dictionnary --> key = parameter, value = score
harpin_loop_energy = {
        3 : 7.4,
        4 : 5.9,
        5 : 4.4,
        6 : 4.3,
        7 : 4.1,
        8 : 4.1,
        9 : 4.2,
        10 : 4.3,
        11 : 4.6,
        12 : 4.9,
        13 : 5.25,
        14 : 5.6,
        15 : 5.85,
        16 : 6.1,
        17 : 6.4,
        18 : 6.7,
        19 : 6.9,
        20 : 7.1,
        21 : 7.3,
        22 : 7.5,
        23 : 7.7,
        24 : 7.9,
        25 : 8.1,
        26 : 8.26,
        27 : 8.42,
        28 : 8.58,
        29 : 8.74,
        30 : 8.9
 }

bulge_energy = {
        2 : 5.2,
        3 : 6.0,
        4 : 6.7,
        5 : 7.4,
        6 : 8.2,
        7 : 9.1,
        8 : 10.0,
        9 : 10.5,
        10 : 11.0,
        11 : 11.4,
        12 : 11.8,
        13 : 12.15,
        14 : 12.5,
        15 : 12.75,
        16 : 13.0,
        17 : 13.3,
        18 : 13.6,
        19 : 13.8,
        20 : 14.0,
        21 : 14.2,
        22 : 14.4,
        23 : 14.6,
        24 : 14.8,
        25 : 15.0,
        26 : 15.16,
        27 : 15.32,
        28 : 15.48,
        29 : 15.64,
        30 : 15.8
 }

internal_loop_energy = {
        2 : 0.8,
        3 : 1.3,
        4 : 1.7,
        5 : 2.1,
        6 : 2.5,
        7 : 2.6,
        8 : 2.8,
        9 : 3.1,
        10: 3.6,
        11 : 4.0,
        12 : 4.4,
        13 : 4.75,
        14 : 5.1,
        15 : 5.35,
        16 : 5.6,
        17 : 5.9,
        18 : 6.2,
        19 : 6.4,
        20 : 6.6,
        21 : 6.8,
        22 : 7.0,
        23 : 7.2,
        24 : 7.4,
        25 : 7.6,
        26 : 7.76,
        27 : 7.92,
        28 : 8.08,
        29 : 8.24,
        30 : 8.4
}


def EIS1(i, j):
    """scoring function for an irreducible surface of order 1"""
    # compute number of nucleotides between j and i
    delta_j_i = j - i - 1

    if delta_j_i > 30:
        return coaxial_stacking(i, j, i+1, j-1) + 8.9
    elif delta_j_i > 2:
        return coaxial_stacking(i, j, i+1, j-1) + harpin_loop_energy[delta_j_i]
    else:
        return float("inf")


def EIS2(i, j, k, l):
    """scoring function for an irreducible surface of order 2"""

    #######
    # k-l #
    # i-j #
    # 5 3 #
    #######

    # compute number of nucleotides between k and i / j and l
    delta_k_i = k - i - 1
    delta_j_l = j - l - 1


    # stem
    if (delta_k_i == 0) and (delta_j_l == 0):
        return coaxial_stacking(i, j, k, l)


    # bulge
    if (delta_k_i == 1) or (delta_j_l == 1):
        # bulge size = 1
        return coaxial_stacking(i, j, k, l) + 3.3

    if (delta_k_i > 0) and (delta_j_l == 0):
        # the bulge is between k  and i and its size is delta_k_i
        if delta_k_i > 30: return 16
        else: return bulge_energy[delta_k_i]

    if (delta_k_i == 0) and (delta_j_l > 0):
        # the bulge is between j and l and its size is delta_j_l
        if delta_j_l > 30: return 16
        else: return bulge_energy[delta_j_l]


    # internal loop
    if (delta_k_i > 0) and (delta_k_i > 0):
        if delta_k_i + delta_j_l > 30: return 8.5
        else: return internal_loop_energy[delta_k_i + delta_j_l]


def EIS2_wave(i, j, k, l):
    """scoring function for an irreducible surface of order 2 in pseudoknot"""
    return EIS2(i, j, k, l) * 0.83


def coaxial_stacking(i, j, k, l):
    """compute and return the coaxial stacking score"""

    global sequence
    i = sequence[i]
    j = sequence[j]
    k = sequence[k]
    l = sequence[l]

    #######
    # --> #
    # i k #
    # | | #
    # j l #
    # <-- #
    #######

    #table 2 from 'Improved free-energy parameters for predictions of RNA duplex stability'
    if i == 'A' and j == 'U' and k == 'A' and l == 'U': return -0.9
    if i == 'A' and j == 'U' and k == 'U' and l == 'A': return -0.9
    if i == 'U' and j == 'A' and k == 'A' and l == 'U': return -1.1
    if i == 'C' and j == 'G' and k == 'A' and l == 'U': return -1.8
    if i == 'C' and j == 'G' and k == 'U' and l == 'A': return -1.7
    if i == 'G' and j == 'C' and k == 'A' and l == 'U': return -2.3
    if i == 'G' and j == 'C' and k == 'U' and l == 'A': return -2.1
    if i == 'C' and j == 'G' and k == 'G' and l == 'C': return -2.0
    if i == 'G' and j == 'C' and k == 'C' and l == 'G': return -3.4
    if i == 'G' and j == 'C' and k == 'G' and l == 'C': return -2.9

    # initiation 3.4 ?

    # mismatches G-U
    if i == 'A' and j == 'U' and k == 'G' and l == 'U': return -0.5
    if i == 'C' and j == 'G' and k == 'G' and l == 'U': return -1.5
    if i == 'G' and j == 'C' and k == 'G' and l == 'U': return -1.3
    if i == 'U' and j == 'A' and k == 'G' and l == 'U': return -0.7
    if i == 'G' and j == 'U' and k == 'G' and l == 'U': return -0.5
    if i == 'U' and j == 'G' and k == 'G' and l == 'U': return -0.6

    if i == 'A' and j == 'U' and k == 'U' and l == 'G': return -0.7
    if i == 'C' and j == 'G' and k == 'U' and l == 'G': return -1.5
    if i == 'G' and j == 'C' and k == 'U' and l == 'G': return -1.9
    if i == 'U' and j == 'A' and k == 'U' and l == 'G': return -0.5
    if i == 'G' and j == 'U' and k == 'U' and l == 'G': return -0.5
    if i == 'U' and j == 'G' and k == 'U' and l == 'G': return -0.5

    return -0.4



def coaxial_stacking_wave(i, j, k, l):
    """compute and return the coaxial stacking score in pseudoknots """
    return coaxial_stacking(i, j, k, l) * 0.83


def dangle_R(i, j, k):
    """return the free-energy for unpaired 3' terminal nucleotides"""
    # page 9/16 --> R^j i, j-1 where j = i, i = j, j-1 = k

    global sequence
    i = sequence[i]
    j = sequence[j]
    k = sequence[k]

    #############
    # --> # --> #
    # k i #   k #
    # |   #   | #
    # j   # i j #
    # <-- # <-- #
    #############

    if (k != i-1) or (j != i-1): raise IndexError("k != i-1 or j != i-1")
    # table 3 from 'Improved free-energy parameters for predictions of RNA duplex stability'
    if i == 'A' and k == 'A' and j == 'U': return -0.8
    if i == 'C' and k == 'A' and j == 'U': return -0.5
    if i == 'G' and k == 'A' and j == 'U': return -0.8
    if i == 'U' and k == 'A' and j == 'U': return -0.6

    if i == 'A' and k == 'C' and j == 'G': return -1.7
    if i == 'C' and k == 'C' and j == 'G': return -0.8
    if i == 'G' and k == 'C' and j == 'G': return -1.7
    if i == 'U' and k == 'C' and j == 'G': return -1.2

    if i == 'A' and k == 'G' and j == 'C': return -1.1
    if i == 'C' and k == 'G' and j == 'C': return -0.4
    if i == 'G' and k == 'G' and j == 'C': return -1.3
    if i == 'U' and k == 'G' and j == 'C': return -0.6

    if i == 'A' and k == 'U' and j == 'A': return -0.7
    if i == 'C' and k == 'U' and j == 'A': return -0.1
    if i == 'G' and k == 'U' and j == 'A': return -0.7
    if i == 'U' and k == 'U' and j == 'A': return -0.1


def dangle_L(i, k, j):
    """return the free-energy for unpaired 5' terminal nucleotides """
   # page 9/16 --> L^i i+1, j where i = i, i+1 = k, j = j

    global sequence
    i = sequence[i]
    j = sequence[j]
    k = sequence[k]

    #############
    # --> # --> #
    # i k # k   #
    #   | # |   #
    #   j # j i #
    # <-- # <-- #
    #############

    if (k != i+1) or (j != i+1): raise IndexError("k != i+1 or j != i+1")
    # table 3 from 'Improved free-energy parameters for predictions of RNA duplex stability'
    if i == 'A' and k == 'A' and j == 'U': return -0.3
    if i == 'C' and k == 'A' and j == 'U': return -0.3
    if i == 'G' and k == 'A' and j == 'U': return -0.3
    if i == 'U' and k == 'A' and j == 'U': return -0.2

    if i == 'A' and k == 'C' and j == 'G': return -0.5
    if i == 'C' and k == 'C' and j == 'G': return -0.2
    if i == 'G' and k == 'C' and j == 'G': return -0.2
    if i == 'U' and k == 'C' and j == 'G': return -0.1

    if i == 'A' and k == 'G' and j == 'C': return -0.2
    if i == 'C' and k == 'G' and j == 'C': return -0.2
    if i == 'G' and k == 'G' and j == 'C': return -0.0
    if i == 'U' and k == 'G' and j == 'C': return -0.0

    if i == 'A' and k == 'U' and j == 'A': return -0.3
    if i == 'C' and k == 'U' and j == 'A': return -0.3
    if i == 'G' and k == 'U' and j == 'A': return -0.3
    if i == 'U' and k == 'U' and j == 'A': return -0.2


def dangle_Ri(i, j, k):
    """return the scoring parameter for 3' base dangling off a multiloop pair"""
    return dangle_R(i, j, k) + 0.4


def dangle_Li(i, j, k):
    """return the scoring parameter for 5' base dangling off a multiloop pair"""
    return dangle_L(i, k, j) + 0.4


def dangle_R_wave(i, j, k):
    """return the scoring paramater for 3' base dangling off a pseudoknot pair"""
    return dangle_R(i, j, k) * 0.83 + 0.2


def dangle_L_wave(i, j, k):
    """return the scoring paramater for 5' base dangling off a pseudoknot pair"""
    return dangle_L(i, k, j) * 0.83 + 0.2


# dictionnary --> key = parameter, value = score
parameters = {
        "EIS1" : EIS1,
        "EIS2" : EIS2,
        "C" : coaxial_stacking,
        "P" : 0,
        "Q" : 0,
        "R" : dangle_R,
        "L" : dangle_L,
        "Pi" : 0.1,
        "Qi" : 0.4,
        "Ri" : dangle_Ri,
        "Li" : dangle_Li,
        "M" : 4.6,
        "g" : 0.83,
        "EIS2_wave" : EIS2_wave,
        "C_wave" : coaxial_stacking_wave,
        "P_wave" : 0.1,
        "Pi_wave" : 0.1*0.83,
        "Q_wave" : 0.2,
        "R_wave" : dangle_R_wave,
        "L_wave" : dangle_L_wave,
        "M_wave" : 8.43,
        "Gw" : 7.0,
        "Gwi" : 13.0,
        "Gwh" : 6.0
}
