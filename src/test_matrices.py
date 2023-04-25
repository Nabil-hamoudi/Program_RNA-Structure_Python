from create_matrices import *
from matrices import matrix_wx

# sequence1 = "UCCGAAGUGCAACGGGAAAAUGCACU"
# sequence2 = "CAGUCAUGCUAGCAUG"
# sequence4 = "GGCACCUCCUCGCGGUGCC"
# sequence3 = "AAACAUGAGGAUUACCCAUGU"
# sequence = "GGCGCAGUGGGCUAGCGCCACUCAAAAGGCCCAU"  # pseudoknot


def run_matrix(sequence):
    """"""
    matrix = create_matrices(len(sequence))
    fill_matrices(matrix)

    matrix_wx.matrix_wx(0, len(sequence)-1, matrix, sequence)

    return matrix


def traceback(matrix, current_matrix_name, indices, matches, verbose=False):
    """traceback the matrices to get the optimal path and deduce the optimal structures"""
  
    if len(indices) == 2: # matrices vx, wx and wxi
        best_score  = matrix[current_matrix_name][indices[1]][indices[0]][0]
        matrices_used = matrix[current_matrix_name][indices[1]][indices[0]][1]
    elif len(indices) == 4: # matrices vhx, whx, yhx and zhx
        best_score = matrix[current_matrix_name][indices[1]][indices[3]][indices[2]][indices[0]][0]
        matrices_used = matrix[current_matrix_name][indices[1]][indices[3]][indices[2]][indices[0]][1]
    else:
        raise IndexError("Invalid number of indices.")
        
    if verbose:    
        print("------------------------------------------------------------------------")
        print(f"Current matrix : {current_matrix_name}")
        print(f"indices : {indices}")
        print("best score :", round(best_score, 2))


    # for each tuple in list matrices_used
    for matrix_used in matrices_used:
        if verbose:
            print(f"trace {matrix_used[0]} {matrix_used[1:]}")

    for matrix_used in matrices_used:
        matrix_name = matrix_used[0]
        
        if "EIS" in matrix_name:
            continue
    
        if matrix_name == "vx":
            matches[matrix_used[1]] = matrix_used[2]
            matches[matrix_used[2]] = matrix_used[1]


        elif matrix_name == "vhx":
            matches[matrix_used[1]] = matrix_used[2]
            matches[matrix_used[2]] = matrix_used[1]

            matches[matrix_used[3]] = matrix_used[4]
            matches[matrix_used[4]] = matrix_used[3]


        elif matrix_name == "yhx":
            matches[matrix_used[3]] = matrix_used[4]
            matches[matrix_used[4]] = matrix_used[3]


        elif matrix_name == "zhx":
            matches[matrix_used[1]] = matrix_used[2]
            matches[matrix_used[2]] = matrix_used[1]


        traceback(matrix, matrix_name, matrix_used[1:], matches, verbose)


def display(sequence, matches, best_score):
    """output the results of the given sequence"""
    output = f"Results :\n"
    output += "energy : " +  str(round(best_score, 2)) + " kcal/mol\n"
    for nucleotide in sequence:
        output += nucleotide + "  "
    output += "\n"
    for position in range(len(sequence)):
        output += str(position) + " "*(3-len(str(position)))
    output += "\n"
    for index in matches:
        output += str(index) + " "*(3-len(str(index)))
    output += "\n"
  
    print(output)
    return output


def print_matrix(matrix, matrix_name):
    """print the given matrix"""
    
    if matrix_name in ["vx", "wx", "wxi"]:
        print("\n##", matrix_name, "##")
        for line in matrix[matrix_name]: print([round(x[0], 2) for x in line])
    elif matrix_name in ["vhx", "whx", "yhx", "zhx"]:
        print("\n##", matrix_name, "##")
        #for line in matrix[matrix_name]: print([round(x[0], 2) for x in line])

