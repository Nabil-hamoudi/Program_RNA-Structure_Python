import sys
import argparse
from output import *
from traceback_RNA import *
from sequence_handling import *
from create_matrices import *
from matrices import matrix_wx
from tkinter import filedialog
import pathlib
import os


DIRECTORY_NAME_GRAPH = "result"
DEFAULT_SAVE_FILENAME = "result"
DEFAULT_EXTENSION_SAVE = "txt"
FILE_TYPE = [("Fasta file", "*.fasta *.fa *.fna *.ffn *.frn"), ("Texte file", "*.txt"), ("other format", "*")]


# Parser
def parser():
    """
    Initialisation of the parser
    output argument of the user
    """
    parser = argparse.ArgumentParser()

    input_group = parser.add_mutually_exclusive_group(required=False)
    input_group.add_argument('-i', '--input', help='input an RNA sequence', type=str, nargs='?')
    input_group.add_argument('-f', '--file_input', help='input a Fasta file of an RNA sequence', type=argparse.FileType('r'), nargs='?')
    parser.add_argument('-s', '--save', help='save the output into a file', type=argparse.FileType('x'), required=False, nargs='?')
    parser.add_argument('-t', '--traceback', help='display the traceback', action='store_true', default=False, required=False)
    parser.add_argument('-g', '--graph', help='create a graph and save it into a directory', type=path_input, required=False, nargs='?')

    args = parser.parse_args(sys.argv[1::])

    # parse if there is the flag file, input or no flag and the argument
    if args.file_input is None:
        if args.input is None:
            if '-i' in sys.argv[1::] or '--input' in sys.argv[1::]:
                args.input = ""
            args.file_input = filedialog.askopenfile(mode='r', title="RNA sequence file", filetypes=FILE_TYPE)
            if args.file_input is None:
                args.input = ""

    # parse the graph and add the result directory
    save_directory = None
    if args.graph is not None:
        save_directory = args.graph
        args.graph = os.path.join(args.graph, DIRECTORY_NAME_GRAPH)
        os.mkdir(args.graph)
    elif args.graph is None and ('-g' in sys.argv[1::] or '--graph' in sys.argv[1::]):
        argument = filedialog.askdirectory(mustexist=True, title="Enter a valid directory")
        if argument is not None:
            args.graph = pathlib.Path(argument)
            save_directory = args.graph
            args.graph = os.path.join(args.graph, DIRECTORY_NAME_GRAPH)
            os.mkdir(args.graph)

    # parse the save if there is an argument or not
    if args.save is None and ('--save' in sys.argv[1::] or '-s' in sys.argv[1::]):
        args.save = filedialog.asksaveasfile(mode='x', title="save file",
                                             initialdir=save_directory,
                                             initialfile=DEFAULT_SAVE_FILENAME,
                                             defaultextension=DEFAULT_EXTENSION_SAVE)

    return args


def path_input(argument):
    """
    docstring
    """
    argument = pathlib.Path(argument)
    if argument.exists() and argument.is_dir():
        return argument
    else:
        raise "Not a directory"


def get_output(sequence, sequence_name, verbose_traceback, graphe_directory=None):
    """
    docstring
    """
    matches, matrix = run_programs(sequence, verbose_traceback)
    output = display_results(sequence_name, sequence, matches, matrix["wx"][len(sequence) - 1][0][0]) + '\n'
    if graphe_directory is not None:
        draw_graph(os.path.join(graphe_directory, sequence_name + ".jpeg"), sequence, matches)
    return output


def program_parse(args):
    """
    parse with flag: ['-i', '--input'] or ['-f', '--file_input'] or no flag
    """
    if args.input is not None:
        sequence = check_rna_seq(args.input)
        sequence_name = "Unknow sequence"
        output = get_output(sequence, sequence_name, args.traceback, args.graph)
    else:
        dict_seq = reading_fasta_file(args.file_input)
        output = ""
        for sequence_name in dict_seq:
            sequence = check_rna_seq(dict_seq[sequence_name])
            output += get_output(sequence, sequence_name, args.traceback, args.graph)
    return output


def run_programs(sequence, verbose=False):
    """
    get sequence from arguments
    """
    # check the sequence
    sequence = check_rna_seq(sequence)

    # initialize matrices
    matrix = create_matrices(len(sequence))
    fill_matrices(matrix)

    # start the algorithm
    matrix_wx.matrix_wx(0, len(sequence)-1, matrix, sequence)

    # traceback
    matches = ["_"] * len(sequence)
    traceback(matrix, "wx", (0, len(sequence) - 1), matches, verbose)

    return (matches, matrix)


if __name__ == "__main__":
    args = parser()
    output = program_parse(args)

    # write into file if we save
    if args.save is not None:
        args.save.write(output)

