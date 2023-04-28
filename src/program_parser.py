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
    Initialization of the parser and
    modification of the arguments for the program
    Output: Argument of the user
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
                        type=lambda argument: path_input(parser, argument, '-g/--graph'),
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


def path_input(parser, argument, flag):
    """
    Input: Parser_class to get error and argument user input
    Define path of the directory
    enter by the user and return it if
    it exists and is a directory
    """
    argument = pathlib.Path(argument)
    if argument.exists() and argument.is_dir():
        return argument
    else:
        parser.error(f'invalid directory for flag {flag}.')


def parser_input(args, parser):
    """
    Input: Argument structure with the user input, Parser_class to get error 
    parse the input for -i/--input and -f/--file_input if there is an argument or not, if not a window to choose the
    file will display
    """
    if ('-i' in sys.argv[1::] or '--input' in sys.argv[1::]) and ('-f' in sys.argv[1::] or '--file_input' in sys.argv[1::]):
        parser.error("argument -f/--file_input: not allowed with argument -i/--input")

    if args.file_input is None:
        if args.input is None:
            if '-i' in sys.argv[1::] or '--input' in sys.argv[1::]:
                parser.error('argument for -i flag is required.')
            args.file_input = filedialog.askopenfile(mode='r', title="Choose a file", filetypes=FILE_TYPE_READ)
            if args.file_input is None:
                parser.error('no parameters given for -i/--input or -f/--file_input.')


def parser_graph(args, parser):
    """
    Input: Argument structure with the user input, Parser_class to get error 
    parse the save directory input by the user and add the result directory to it
    """
    if args.graph is not None:
        args.graph = os.path.join(args.graph, DIRECTORY_NAME_GRAPH)
        os.mkdir(args.graph)
    elif '-g' in sys.argv[1::] or '--graph' in sys.argv[1::]:
        argument = filedialog.askdirectory(mustexist=True, title="Enter a directory where save the graph(s)")
        if argument is not None:
            args.graph = pathlib.Path(argument)
            args.graph = os.path.join(args.graph, DIRECTORY_NAME_GRAPH)
            os.mkdir(args.graph)
        else:
            parser.error('no save directory given for -g/--graph flag.')


def parser_save(args, parser, save_directory=None):
    """
    Input: Argument structure with the user input, Parser_class to get error and
    default directory where to display the save window
    parse the save if there is an argument or not, if not a window for choose the
    file will display
    """
    if args.save is None and ('--save' in sys.argv[1::] or '-s' in sys.argv[1::]):
        args.save = filedialog.asksaveasfile(mode='x', title="Save file",
                                             initialdir=save_directory,
                                             initialfile=DEFAULT_SAVE_FILENAME,
                                             defaultextension=DEFAULT_EXTENSION_SAVE,
                                             filetypes=FILE_TYPE_SAVE)
        if args.save is None:
            parser.error('no save file given for -s/--save flag.')
