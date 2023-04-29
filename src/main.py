from output import *
from traceback_RNA import *
from sequence_handling import *
from create_matrices import *
from matrices import matrix_wx
from program_parser import parser_function
import os

# Default constant for file display
GRAPH_EXTENSION = ".jpeg"


def get_sequences(args):
    """
    Input: Arguments entered by the user
    Output: 
    Manage the program with the arguments
    """
    if args.input is not None:
        return {"Unknown sequence": args.input}
    else:
        return reading_fasta_file(args.file_input)


def get_output(sequence, sequence_name, verbose_traceback, graphe_directory=None):
    """
    Output str of the save if need it and 
    save graph(s) if graph argument present
    """
    matches, best_score = run_algorithm(sequence, verbose_traceback)
    output = display_results(sequence_name, sequence, matches, best_score)
    if graphe_directory is not None:
        draw_graph(os.path.join(graphe_directory, sequence_name + GRAPH_EXTENSION), sequence, matches)
    return output


def run_algorithm(sequence, verbose=False):
    """
    Start the dynamic programming algorithm
    """
    # initialize matrices
    matrix = create_matrices(len(sequence))
    fill_matrices(matrix)

    # start the algorithm
    matrix_wx.matrix_wx(0, len(sequence)-1, matrix, sequence)

    # traceback
    matches = [None] * len(sequence)
    traceback(matrix, "wx", (0, len(sequence) - 1), matches, verbose)

    best_score = matrix["wx"][len(sequence) - 1][0][0]

    return (matches, best_score)


def main():
    args = parser_function()
    
    dict_seq = get_sequences(args)

    output = ""
    for sequence_name in dict_seq:
        sequence = check_rna_seq(dict_seq[sequence_name])
        output += get_output(sequence, sequence_name, args.traceback, args.graph)

    # write into file if asked
    if args.save is not None:
        args.save.write(output)


if __name__ == "__main__":
    main()
