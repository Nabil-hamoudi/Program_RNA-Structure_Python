import os
import sys
import pathlib
import argparse
from tkinter import filedialog


# Default constant for file display
DIRECTORY_NAME_GRAPH = "result"
DEFAULT_SAVE_FILENAME = "result"
DEFAULT_EXTENSION_SAVE = ".txt"
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
    parser_graph(args, parser)

    if args.graph is not None:
        parser_save(args, parser, os.path.abspath(os.path.join(args.graph, "..")))
    else:
        parser_save(args, parser)

    return args


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


def parser_input(args, parser):
    """
    parse if there is the flag file, input or no flag and the argument
    """
    # because Argparse is fucking dumb
    if ('-i' in sys.argv[1::] or '--input' in sys.argv[1::]) and ('-f' in sys.argv[1::] or '--file_input' in sys.argv[1::]):
        parser.error("argument -f/--file_input: not allowed with argument -i/--input")

    if args.file_input is None:
        if args.input is None:
            if '-i' in sys.argv[1::] or '--input' in sys.argv[1::]:
                parser.error('argument for -i flag is required.')
            args.file_input = filedialog.askopenfile(mode='r', title="Choose a fasta file", filetypes=FILE_TYPE_READ)
            if args.file_input is None:
                parser.error('no input given for -i/--input or -f/--file_input flag.')


def parser_graph(args, parser):
    """
    parse the graph and add the result directory
    """
    if args.graph is not None:
        args.graph = os.path.join(args.graph, DIRECTORY_NAME_GRAPH)
        os.mkdir(args.graph)
    elif '-g' in sys.argv[1::] or '--graph' in sys.argv[1::]:
        argument = filedialog.askdirectory(mustexist=True, title="Enter a directory to save the graph(s)")
        if argument is not None:
            args.graph = pathlib.Path(argument)
            args.graph = os.path.join(args.graph, DIRECTORY_NAME_GRAPH)
            os.mkdir(args.graph)
        else:
            parser.error('no save directory given for -g/--graph flag.')


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
