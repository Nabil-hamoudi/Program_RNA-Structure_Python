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


def sequence_processing(sequence, sequence_name, verbose_traceback, graph_directory=None):
    """
    Process a single sequence
    Input:
        sequence: string containing the sequence
        sequence_name: string containing the name of the sequence
        verbose_traceback: boolean, True  - the traceback should be printed
                                      False - the traceback should not be printed
        graph_directory: string containing the path to the directory
                         where the graph should be created
    Output:
        output: string containing the displayed result
    """
    # check if the sequence is valid
    sequence = check_rna_seq(sequence, sequence_name)
    if sequence == "": # invalid sequence
        return "" # skip the sequence

    # get results for the dynamic programming algorithm
    matches, best_score = run_algorithm(sequence, verbose_traceback)
    
    # keep the output (display) for further use
    output = display_results(sequence_name, sequence, matches, best_score)
    
    if graph_directory is not None: # create the graph if asked
        graph_file = os.path.join(graphe_directory, sequence_name + GRAPH_EXTENSION)
        draw_graph(graph_file, sequence, matches)
    
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
        output += sequence_processing(dict_seq[sequence_name], sequence_name, args.traceback, args.graph)

    # write into file if asked
    if args.save is not None:
        args.save.write(output)


if __name__ == "__main__":
    main()
