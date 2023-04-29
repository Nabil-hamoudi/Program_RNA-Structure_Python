import sys
import subprocess
from traceback_RNA import matches2dbn


def display_results(sequence_name, sequence, matches, best_score):
    """
    output the results of the given sequence
    """

    output = f"## Results for {sequence_name} ##\n" + f"length of the sequence : {len(sequence)} nucleotides" \
            + "\nenergy : " + str(round(best_score, 2)) + " kcal/mol\n"

    for nucleotide in sequence: output += nucleotide + "  "
    output += "\n"
    for position in range(len(sequence)): output += str(position) + " "*(3-len(str(position)))
    output += "\n"
    for index in matches:
        if index is None: index = '_'
        output += str(index) + " "*(3-len(str(index)))
    output += "\n"

    print(output)
    return output + '\n'


def print_matrix(matrix, matrix_name):
    """
    print the given matrix
    """

    if matrix_name in ["vx", "wx", "wxi"]:
        print("\n##", matrix_name, "##")
        for line in matrix[matrix_name]: print([round(x[0], 2) for x in line])
    elif matrix_name in ["vhx", "whx", "yhx", "zhx"]:
        print("\n##", matrix_name, "##")
        #for line in matrix[matrix_name]: print([round(x[0], 2) for x in line])


def draw_graph(file, sequence, matches):
    """
    create an image to represent the secondary structure of the given sequence, using the software VARNA
    """

    dbn = matches2dbn(matches)
    print(dbn)
    main_command = "java -cp structures_tools/VARNAv3-93.jar fr.orsay.lri.varna.applications.VARNAcmd"
    sequence_argument = f" -sequenceDBN {sequence}"
    structure_argument = f" -structureDBN \"{dbn}\""
    output_argument = f" -o \"{str(file)}\""

    return_code = subprocess.call(main_command + sequence_argument + structure_argument + output_argument, shell=True)

    if return_code != 0:
        print(f"VARNA finished with the return code {return_code}")

