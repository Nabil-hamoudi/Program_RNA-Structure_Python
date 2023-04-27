import sys
import argparse
from output import *
from traceback_RNA import *
from sequence_handling import *
from create_matrices import *
from matrices import matrix_wx


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

    args = parser.parse_args(sys.argv[1::])

    return args


def program_parse(args):
    """
    parse with flag: ['-i', '--input'] or ['-f', '--file_input'] or no flag
    """
    if args.input is not None:
        sequence = check_rna_seq(args.input)
        sequence_name = "Unknow sequence"
        matches, matrix = run_programs(sequence, args.traceback)
        output = display_results(sequence_name, sequence, matches, matrix["wx"][len(sequence) - 1][0][0]) + '\n'
    elif args.file_input is not None:
        dict_seq = reading_fasta_file(args.file_input)
        output = ""
        for sequence_name in dict_seq:
            sequence = check_rna_seq(dict_seq[sequence_name])
            matches, matrix = run_programs(sequence, args.traceback)
            output += display_results(sequence_name, sequence, matches, matrix["wx"][len(sequence) - 1][0][0]) + '\n'
    else:
        from tkinter import filedialog
        if '-i' in sys.argv[1::] or '--input' in sys.argv[1::]:
            return ""
        dict_seq = reading_fasta_file(filedialog.askopenfile(mode='r'))
        output = ""
        for sequence_name in dict_seq:
            sequence = check_rna_seq(dict_seq[sequence_name])
            matches, matrix = run_programs(sequence, args.traceback)
            output += display_results(sequence_name, sequence, matches, matrix["wx"][len(sequence) - 1][0][0]) + '\n'
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
    save_into_file(args, output)
