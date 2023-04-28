import os
import sys
import pathlib
import argparse
from tkinter import filedialog
from output import *
from traceback_RNA import *
from sequence_handling import *
from create_matrices import *
from matrices import matrix_wx


# Default constant for file display
DIRECTORY_NAME_GRAPH = "result"
DEFAULT_SAVE_FILENAME = "result"
DEFAULT_EXTENSION_SAVE = ".txt"
GRAPH_EXTENSION = ".jpeg"
FILE_TYPE_SAVE = [("Text file", "*.txt"), ("Log file", "*.log")]
FILE_TYPE_READ = [("Fasta file", "*.fasta *.fa *.fna *.ffn *.frn"), ("Text file", "*.txt"), ("Other format", "*")]


# Parser
def parser_function():
    """
    Initialization of the parser
    return arguments of the user
    """
    parser = argparse.ArgumentParser()

    input_group = parser.add_mutually_exclusive_group(required=False)
    input_group.add_argument('-i', '--input',
                             help='input an RNA sequence',
                             type=str,
                             nargs='?')
    input_group.add_argument('-f', '--file_input',
                             help='input a Fasta file of one or more RNA sequence(s)',
                             type=argparse.FileType('r'),
                             nargs='?')

    parser.add_argument('-s', '--save',
                        help='save the output into a file',
                        type=argparse.FileType('x'),
                        required=False,
                        nargs='?')
    parser.add_argument('-t', '--traceback',
                        help='display the traceback',
                        action='store_true',
                        default=False,
                        required=False)
    parser.add_argument('-g', '--graph',
                        help='save a representation of the secondary structure of RNA into a directory',
                        type=lambda argument: path_input(parser, argument),
                        required=False,
                        nargs='?')

    args = parser.parse_args(sys.argv[1::])

    parser_input(args, parser)

    # parse the graph and add the result directory
    save_directory = None
    if args.graph is not None:
        save_directory = args.graph
        args.graph = os.path.join(args.graph, DIRECTORY_NAME_GRAPH)
        os.mkdir(args.graph)
    elif '-g' in sys.argv[1::] or '--graph' in sys.argv[1::]:
        argument = filedialog.askdirectory(mustexist=True, title="Enter a directory to save the graph(s)")
        if argument is not None:
            args.graph = pathlib.Path(argument)
            save_directory = args.graph
            args.graph = os.path.join(args.graph, DIRECTORY_NAME_GRAPH)
            os.mkdir(args.graph)
        else:
            parser.error('no save directory given for -g/--graph flage.')

    parser_save(args, parser, save_directory)

    return args


def parser_input(args, parser):
    """
    parse if there is the flag file, input or no flag and the argument
    """
    if args.file_input is None:
        if args.input is None:
            # A savoir si on garde ou non
            if '-i' in sys.argv[1::] or '--input' in sys.argv[1::]:
                parser.error('argument for -i flag is required.')
            ###########################
            args.file_input = filedialog.askopenfile(mode='r', title="Choose a fasta file", filetypes=FILE_TYPE_READ)
            if args.file_input is None:
                parser.error('no input given for -i/--input or -f/--file_input flag.')


def parser_save(args, parser, save_directory=None):
    """
    parse the save if there is an argument or not
    """
    if args.save is None and ('--save' in sys.argv[1::] or '-s' in sys.argv[1::]):
        args.save = filedialog.asksaveasfile(mode='x', title="save file",
                                             initialdir=save_directory,
                                             initialfile=DEFAULT_SAVE_FILENAME,
                                             defaultextension= DEFAULT_EXTENSION_SAVE,
                                             filetypes=FILE_TYPE_SAVE)
        if args.save is None:
            parser.error('no save file given for -s/--save flage.')


def path_input(parser, argument):
    """
    Define path and
    parse the graph and add the result directory
    """
    argument = pathlib.Path(argument)
    if argument.exists() and argument.is_dir():
        return argument
    else:
        parser.error('invalid directory for -g flag.')


def get_output(sequence, sequence_name, verbose_traceback, graphe_directory=None):
    """
    docstring
    """
    matches, best_score = run_programs(sequence, verbose_traceback)
    output = display_results(sequence_name, sequence, matches, best_score) + '\n'
    if graphe_directory is not None:
        draw_graph(os.path.join(graphe_directory, sequence_name + GRAPH_EXTENSION), sequence, matches)
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
    Start the dynamic programming algorithm
    """
    # initialize matrices
    matrix = create_matrices(len(sequence))
    fill_matrices(matrix)

    # start the algorithm
    matrix_wx.matrix_wx(0, len(sequence)-1, matrix, sequence)

    # traceback
    matches = ["_"] * len(sequence)
    traceback(matrix, "wx", (0, len(sequence) - 1), matches, verbose)

    best_score = matrix["wx"][len(sequence) - 1][0][0]

    return (matches, best_score)


if __name__ == "__main__":
    args = parser_function()
    output = program_parse(args)

    # write into file if we save
    if args.save is not None:
        args.save.write(output)
