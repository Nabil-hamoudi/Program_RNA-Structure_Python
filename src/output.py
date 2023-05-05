import os
import sys
import subprocess
from traceback_RNA import matches2dbn


def display_results(sequence_name, sequence, matches, best_score):
    """
    Output the results of the given sequence
    Input:
        sequence_name: string containing the name of the sequence
        sequence: string containing the sequence
        matches: list where the ith nucleotide is:
                  - not paired if matches[i] is None
                  - paired to matches[i]th nucleotide if matches[i] is an integer
                 for 0 <= i < sequence length
        best_score: integer of the energy in kcal/mol for the best folding found
    Output:
        string containing the displayed result
    """
    plural = 's' if len(sequence) > 1 else '' # attention to details
    output = f"## Results for {sequence_name} ##\n" + f"length of the sequence : {len(sequence)} nucleotide{plural}" \
            + "\nenergy : " + str(round(best_score, 2)) + " kcal/mol\n"

    # display the nucleotides of the sequence
    for nucleotide in sequence: output += nucleotide + "  "
    output += '\n'
    
    # display the index of the nucleotide
    for position in range(len(sequence)): output += str(position) + " "*(3-len(str(position)))
    output += '\n'
    
    # display the index of the paired nucleotide
    for index in matches:
        if index is None: index = '_'
        output += str(index) + " "*(3-len(str(index)))
    output += "\nStructure(s) in DBN format:\n"

    # translates the list matches to DBN format
    output += matches2dbn(matches) + '\n'
    print(output)
    return output + '\n'


def print_matrix(matrix, matrix_name):
    """
    Used for debugging, print a matrix
    Input:
        matrix: dictionnary of matrices
        matrix_name: string of the name of the matrix to print
    No output
    """
    print("\n##", matrix_name, "##")
    if matrix_name in ["vx", "wx", "wxi"]: # 2D matrices
        for line in matrix[matrix_name]: print([round(x[0], 2) for x in line])
    elif matrix_name in ["vhx", "whx", "yhx", "zhx"]: # 4D matrices
        pass
        #for line in matrix[matrix_name]: print([round(x[0], 2) for x in line])


def draw_graph(file, sequence, matches):
    """
    Create an image to represent the secondary structure of the given sequence, using the software VARNA
    Input:
        file: Path of the file to create
        sequence: string containing the sequence
        matches: list where the ith nucleotide is:
                  - not paired if matches[i] is None
                  - paired to matches[i]th nucleotide if matches[i] is an integer
                 for 0 <= i < sequence length
    No output
    """
    dbn = matches2dbn(matches) # translates the list matches to DBN format
    # compute VARNA path
    path_to_varna = os.path.join(os.path.dirname(__file__), '..', 'structures_tools', "VARNAv3-93.jar")

    # format the command and its arguments
    main_command = f"java -cp \"{path_to_varna}\" fr.orsay.lri.varna.applications.VARNAcmd"
    sequence_argument = f" -sequenceDBN {sequence}"
    structure_argument = f" -structureDBN \"{dbn}\""
    output_argument = f" -o \"{str(file)}\" -resolution 3"

    # execute the command
    return_code = subprocess.call(main_command + sequence_argument + structure_argument + output_argument, shell=True)

    if return_code != 0: print(f"VARNA finished with the return code {return_code}")

