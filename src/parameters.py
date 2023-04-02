# parameters : table 2 & 3

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

def EIS1(i, j):
    """docstring"""
    pass

def EIS2(i, j, k, l):
    """docstring"""
    pass

def EIS2_wave(i, j, k, l):
    """docstring"""
    pass

def coaxial_stacking(i, j, k, l):
    """compute and return the coaxial stacking score"""
    
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

    #######
    # --> #
    # k i #
    # |   #
    # j   #
    # <-- #
    #######

    if k != i-1 : raise IndexError("k != i-1")
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
   #######
    # --> #
    # i k #
    #   | #
    #   j #
    # <-- #
    #######

    if k != i+1 : raise IndexError("k != i+1")
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


