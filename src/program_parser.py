import os
import sys
import pathlib
import argparse


# Default constants
DIRECTORY_NAME_GRAPH = "results"
DEFAULT_SAVE_FILENAME = "result"
DEFAULT_SAVE_EXTENSION = ".txt"
FILE_TYPE_SAVE = [("Text file", "*.txt"), ("Log file", "*.log")]
FILE_TYPE_READ = [("Fasta file", "*.fasta *.fa *.fna *.ffn *.frn"), ("Text file", "*.txt"), ("Other format", "*")]


# Parser
def parser_function():
    """
    Initialization of the arguments parser and
    modification of the arguments for the program
    No input
    Output:
        Argument of the user
    """
    parser = argparse.ArgumentParser(description='RNA secondary structure prediction using dynamic programmation from a given sequence of RNA.')

    # -i and -f flags cannot be set at the same time
    input_group = parser.add_mutually_exclusive_group(required=False)
    input_group.add_argument('-i', '--input',
                             help='input an RNA sequence',
                             dest="sequence",
                             type=str,
                             nargs='?')
    input_group.add_argument('-f', '--file_input',
                             dest="Fasta_file",
                             help='input a Fasta file of one or more RNA sequence(s)',
                             type=argparse.FileType('r'),
                             nargs='?')

    # remaining flags
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
                        type=lambda argument: check_directory(parser, argument, '-g/--graph'),
                        required=False,
                        nargs='?')

    # analyze the given arguments
    args = parser.parse_args(sys.argv[1::])

    parser_input(args, parser)
    parser_graph(args, parser)
    parser_save(args, parser)

    return args


def create_folder(folder):
    """
    Create a folder if it not already exist
    Input:
        folder: string of the path of the folder to create
    Output:
        string of the path of the folder
    """
    if not pathlib.Path(folder).exists():
        os.mkdir(folder)
    return folder


def check_directory(parser, directory, flag):
    """
    Check if the given path is a directory
    Input:
        parser: container for argument specifications
        directory: string of a path
        flag: string of the name of a flag 
    No output
    """
    directory = os.path.abspath(pathlib.Path(directory))
    parent_directory = pathlib.Path(os.path.abspath(os.path.join(directory, "..")))
    if parent_directory.exists() and parent_directory.is_dir():
        # creation of the folder if an argument is given
        return create_folder(directory)
    else:
        parser.error(f'invalid directory for flag {flag}.')


def parser_input(args, parser):
    """
    Analyze the input for the flags -i and -f
    Input: 
        args: class object of arguments entered by the user
        parser: container for argument specifications
    No output
    """
    # -i and -f flags cannot be set at the same time
    if ('-i' in sys.argv[1::] or '--input' in sys.argv[1::]) and ('-f' in sys.argv[1::] or '--file_input' in sys.argv[1::]):
        parser.error("argument -f/--file_input: not allowed with argument -i/--input")

    # if no input is given
    if args.Fasta_file is None and args.sequence is None:
        # the -i flag must be followed by an RNA sequence
        if '-i' in sys.argv[1::] or '--input' in sys.argv[1::]:
            parser.error('argument for -i flag is required.')
        # open the graphical interface
        try: from tkinter import filedialog
        except ImportError:
            parser.error('No input is given for -i nor -f flag and the tkinter module is not installed.')
        args.Fasta_file = filedialog.askopenfile(mode='r', title="Choose a fasta file", filetypes=FILE_TYPE_READ)
        # raise an error if no file is chosen
        if args.Fasta_file is None:
            parser.error('No parameter given for -i nor -f flag.')


def parser_graph(args, parser):
    """
    Analyze the input for the flag -g
    Input: 
        args: class object of arguments entered by the user
        parser: container for argument specifications
    No output
    """
    # if the -g flag is set but no argument is given
    if args.directory_path is None and ('-g' in sys.argv[1::] or '--graph' in sys.argv[1::]):
        # open the graphical interface
        try: from tkinter import filedialog
        except ImportError:
            parser.error('No input is given for -g/--graph flag and the tkinter module is not installed.')
        argument = filedialog.askdirectory(mustexist=True, title="Choose a directory where to save the graph(s)")
        # creation of the folder at the given path
        if argument is not None:
            args.directory_path = pathlib.Path(argument)
            args.directory_path = os.path.join(args.directory_path, DIRECTORY_NAME_GRAPH)
            create_folder(args.directory_path)
        # creation of the folder at the current directory
        else:
            args.directory_path = os.path.abspath(DIRECTORY_NAME_GRAPH)
            create_folder(args.directory_path)



def parser_save(args, parser):
    """
    Analyze the input for the flag -s
    Input: 
        args: class object of arguments entered by the user
        parser: container for argument specifications
    No output
    """
    # if the -s flag is set but no argument is given
    if args.file_path is None and ('-s' in sys.argv[1::] or '--save' in sys.argv[1::]):
        # open the graphical interface
        try: from tkinter import filedialog
        except ImportError:
            parser.error('No input is given for -s/--save and the tkinter module is not installed.')
        args.file_path = filedialog.asksaveasfile(mode='w', title="Choose a directory and the file name where to save the results",
                                             initialdir=args.directory_path,
                                             initialfile=DEFAULT_SAVE_FILENAME,
                                             defaultextension=DEFAULT_SAVE_EXTENSION,
                                             filetypes=FILE_TYPE_SAVE)
    
        if args.file_path is None:
            if args.directory_path is not None: # save the file in the graphs directory
                args.file_path = os.path.join(args.directory_path, DEFAULT_SAVE_FILENAME) + DEFAULT_SAVE_EXTENSION
            else: # save the file in the current directory and give the default name
                args.file_path = os.path.abspath(DEFAULT_SAVE_FILENAME + DEFAULT_SAVE_EXTENSION)
            try: # try to open or create the file
                args.file_path = open(args.file_path, 'x')
            except FileExistsError:
                parser.error(f"File with the same name already exists : {args.file_path}")
