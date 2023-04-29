import os
import sys
import pathlib
import argparse


# Default constant for file display
DIRECTORY_NAME_GRAPH = "results"
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
    parser = argparse.ArgumentParser(description='RNA PROGRAM DESCRIPTION.')

    input_group = parser.add_mutually_exclusive_group(required=False)
    input_group.add_argument('-i', '--input',
                             help='input an RNA sequence',
                             dest="sequence",
                             type=str,
                             nargs='?')
    input_group.add_argument('-f', '--file_input',
                             dest="Fasta_File",
                             help='input a Fasta file of one or more RNA sequence(s)',
                             type=argparse.FileType('r'),
                             nargs='?')

    parser.add_argument('-s', '--save',
                        help='save the output into a file',
                        dest="file_path",
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
                        dest="directory_path",
                        type=lambda argument: path_input(parser, argument, '-g/--graph'),
                        required=False,
                        nargs='?')

    args = parser.parse_args(sys.argv[1::])

    parser_input(args, parser)
    parser_graph(args, parser)

    if args.directory_path is not None:
        parser_save(args, parser)
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

    if args.Fasta_File is None:
        if args.sequence is None:
            if '-i' in sys.argv[1::] or '--input' in sys.argv[1::]:
                parser.error('argument for -i flag is required.')
            from tkinter import filedialog
            args.Fasta_File = filedialog.askopenfile(mode='r', title="Choose a file", filetypes=FILE_TYPE_READ)
            if args.Fasta_File is None:
                parser.error('no parameters given for -i/--input or -f/--file_input.')


def parser_graph(args, parser):
    """
    Input: Argument structure with the user input, Parser_class to get error
    parse the save directory input by the user and add the result directory to it
    """
    if args.directory_path is not None:
        args.directory_path = os.path.join(args.directory_path, DIRECTORY_NAME_GRAPH)
        create_folder(args.directory_path)
    elif '-g' in sys.argv[1::] or '--graph' in sys.argv[1::]:
        from tkinter import filedialog
        argument = filedialog.askdirectory(mustexist=True, title="Enter a directory where save the graph(s)")
        if argument is not None:
            args.directory_path = pathlib.Path(argument)
            args.directory_path = os.path.join(args.directory_path, DIRECTORY_NAME_GRAPH)
            create_folder(args.directory_path)
        else:
            args.directory_path = os.path.abspath(DIRECTORY_NAME_GRAPH)
            create_folder(args.directory_path)


def create_folder(folder):
    """
    create a folder if it not already exist
    """
    if not pathlib.Path(folder).exists():
        os.mkdir(folder)


def parser_save(args, parser):
    """
    Input: Argument structure with the user input, Parser_class to get error and
    default directory where to display the save window
    parse the save if there is an argument or not, if not a window for choose the
    file will display
    """
    if args.file_path is None and ('--save' in sys.argv[1::] or '-s' in sys.argv[1::]):
        from tkinter import filedialog
        args.file_path = filedialog.asksaveasfile(mode='w', title="Save file",
                                             initialdir=args.directory_path,
                                             initialfile=DEFAULT_SAVE_FILENAME,
                                             defaultextension=DEFAULT_EXTENSION_SAVE,
                                             filetypes=FILE_TYPE_SAVE)
        if args.file_path is None:
            if args.directory_path is not None:
                args.file_path = os.path.join(args.directory_path, DEFAULT_SAVE_FILENAME) + DEFAULT_EXTENSION_SAVE
            else:
                args.file_path = os.path.abspath(DEFAULT_SAVE_FILENAME + DEFAULT_EXTENSION_SAVE)
            try:
                args.file_path = open(args.file_path, 'x')
            except FileExistsError:
                parser.error('default save already exist for -s/--save flag.')
