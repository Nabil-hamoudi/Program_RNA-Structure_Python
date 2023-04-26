from create_matrices import *
from matrices import matrix_wx

def run_matrix(sequence):
    """"""
    matrix = create_matrices(len(sequence))
    fill_matrices(matrix)

    matrix_wx.matrix_wx(0, len(sequence)-1, matrix, sequence)

    return matrix


def display_results(name_sequence, sequence, matches, best_score):
    """output the results of the given sequence"""
    
    output = f"## Results for {name_sequence} ##\n" + f"length of the sequence : {len(sequence)} nucleotides" \
            + "\nenergy : " + str(round(best_score, 2)) + " kcal/mol\n"
                                                                                      
    for nucleotide in sequence: output += nucleotide + "  "
    output += "\n"
    for position in range(len(sequence)): output += str(position) + " "*(3-len(str(position)))
    output += "\n"
    for index in matches: output += str(index) + " "*(3-len(str(index)))
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


