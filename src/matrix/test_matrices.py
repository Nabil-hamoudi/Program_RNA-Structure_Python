import sys
from create_matrices import *
import matrix_vx
import matrix_wx
import matrix_wxi

sequence2 = "CAGUCAUGCUAGCAUG"
sequence = "AGCAAAAAGCAA"

#sys.setrecursionlimit(19000)
matrix = create_matrices(len(sequence))
fill_matrices(matrix)

matrix_wx.matrix_wx(0, len(sequence)-1, matrix, sequence)

print("## WX ##")
for line in matrix["wx"]: print([round(x[0], 2) for x in line])


def traceback(matrix, current_matrix_name, indices):
    """traceback"""
    
    print("------------------------------------------------------------------------")
    print(f"Current matrix : {current_matrix_name}")
    print(f"indices : {indices}")

    if len(indices) == 2:
        best_score  = matrix[current_matrix_name][indices[1]][indices[0]][0]
        matrices_used = matrix[current_matrix_name][indices[1]][indices[0]][1]
    elif len(indices) == 4:
        best_score = matrix[current_matrix_name][indices[3]][indices[2]][indices[1]][indices[0]][0]
        matrices_used = matrix[current_matrix_name][indices[3]][indices[2]][indices[1]][indices[0]][1]
    else:
        print(f"Index error")

    print(f"best score : {best_score}")


    # for each tuple in list matrices_used
    for matrix_used in matrices_used:
        print(f"trace {matrix_used[0]} {matrix_used[1:]}")

    for matrix_used in matrices_used:
        matrix_name = matrix_used[0]
        
        if "EIS" in matrix_name:
            continue


        traceback(matrix, matrix_name, matrix_used[1:])

        

def display(sequence):
    for nucleotide in sequence:
        print(nucleotide, "  ", sep="", end="")
    print()
    for position in range(len(sequence)):
        print(position, " "*(2-(position//10)), sep="", end="")
    print()







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

traceback(matrix, "wx", (0, len(sequence) - 1))
display(sequence)
# avec i = 0 et j = len(sequence) - 1

