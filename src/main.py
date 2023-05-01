#!/bin/python3

import os
from output import *
from traceback_RNA import *
from sequence_handling import *
from create_matrices import *
from matrices import matrix_wx
from program_parser import parser_function


GRAPH_EXTENSION = ".jpeg"


def get_sequences(args):
    """
    Get the sequences from the arguments
    Input:
        args: class of arguments entered by the user
    Output: 
        dictionnary containing the sequences and their name as key
    """
    if args.sequence is not None: # sequence input
        return {"Unknown sequence": args.sequence}
    else: # fasta file input
        return reading_fasta_file(args.Fasta_file)


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
        string containing the displayed result
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
        # replace all forbidden characters by an underscore
        for char in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
            sequence_name = sequence_name.replace(char, '_')
        graph_file = os.path.join(graph_directory, sequence_name + GRAPH_EXTENSION)
        draw_graph(graph_file, sequence, matches)
    
    return output


def run_algorithm(sequence, verbose=False):
    """
    Start the dynamic programming algorithm
    Input:
        sequence: string containing the sequence
        verbose: boolean, True  - the traceback should be printed
                          False - the traceback should not be printed
    Output:
        string containing the displayed result
    """
    # initialize the matrices
    matrix = create_matrices(len(sequence))
    fill_matrices(matrix)

    # start the algorithm to fill the matrices
    matrix_wx.matrix_wx(0, len(sequence)-1, matrix, sequence)

    # traceback the matrices to find the optimal path
    matches = [None] * len(sequence)
    traceback(matrix, "wx", (0, len(sequence) - 1), matches, verbose)

    # the best score is in the WX matrix where i = 0 and j = N (sequence length)
    best_score = matrix["wx"][len(sequence) - 1][0][0]

    return (matches, best_score)


def main():
    """
    Function to run the whole program
    No input
    No output
    """
    # read and manage the cli arguments
    args = parser_function()
    
    # retrieve the sequence(s) from the arguments
    dict_seq = get_sequences(args)

    # process each sequence in the dictionnary
    # and concatenate the result
    output = ""
    for sequence_name in dict_seq:
        output += sequence_processing(dict_seq[sequence_name], sequence_name, args.traceback, args.directory_path)

    # write the result into file if asked
    if args.file_path is not None:
        args.file_path.write(output)


if __name__ == "__main__":
    main()
