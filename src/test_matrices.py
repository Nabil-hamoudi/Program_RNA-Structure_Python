import sys
from create_matrices import *
import matrix_vx
import matrix_wx
import matrix_wxi

# sequence1 = "UCCGAAGUGCAACGGGAAAAUGCACU"
# sequence2 = "CAGUCAUGCUAGCAUG"
# sequence4 = "GGCACCUCCUCGCGGUGCC"
# sequence3 = "AAACAUGAGGAUUACCCAUGU"
# sequence = "GGCGCAGUGGGCUAGCGCCACUCAAAAGGCCCAU"  # pseudoknot


#sys.setrecursionlimit(19000)


def run_matrix(sequence):
    """create_matrix"""
    matrix = create_matrices(len(sequence))
    fill_matrices(matrix)

    matrix_wx.matrix_wx(0, len(sequence)-1, matrix, sequence)

    print("## WX ##")
    for line in matrix["wx"]: print([round(x[0], 2) for x in line])
    print("## VX ##")
    for line in matrix["vx"]: print([round(x[0], 2) for x in line])

    return matrix


def traceback(matrix, current_matrix_name, indices, matches):
    """traceback the matrices to get the optimal path and deduce the optimal structures"""
    
    print("------------------------------------------------------------------------")
    print(f"Current matrix : {current_matrix_name}")
    print(f"indices : {indices}")

    if len(indices) == 2:
        best_score  = matrix[current_matrix_name][indices[1]][indices[0]][0]
        matrices_used = matrix[current_matrix_name][indices[1]][indices[0]][1]
    elif len(indices) == 4:
        best_score = matrix[current_matrix_name][indices[1]][indices[3]][indices[2]][indices[0]][0]
        matrices_used = matrix[current_matrix_name][indices[1]][indices[3]][indices[2]][indices[0]][1]
    else:
        print(f"Index error")

    print("best score :", round(best_score, 2))


    # for each tuple in list matrices_used
    for matrix_used in matrices_used:
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


        traceback(matrix, matrix_name, matrix_used[1:], matches)


def display(sequence, matches, best_score):
    """"""
    output = f"\nResults :\n"
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



# print("\n## WX ##")
# for line in matrix["wx"]: print(line)
# print("\n## WXi ##")
# for line in matrix["wxi"]: print(line)
# print("\n## Whx ##")
# for line in matrix["whx"]: print(line)
# print("\n## vhx ##")
# for line in matrix["vhx"]: print(line)
# print("\n## yhx ##")
# for line in matrix["yhx"]: print(line)
# print("\n## zhx ##")
# for line in matrix["zhx"]: print(line)

#matches = ["_"] * len(sequence)
#traceback(matrix, "wx", (0, len(sequence) - 1), matches)
#display(sequence, matches, matrix["wx"][len(sequence) - 1][0][0])

# avec i = 0 et j = len(sequence) - 1
