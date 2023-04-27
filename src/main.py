import sys
import argparse
from display import *
from traceback_RNA import traceback


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


def reading_fasta_file(file):
    """
    Reading file containing RNA (or DNA) sequence
    Input: file in fasta format
    Output: dictionary with RNA (or DNA) sequence(s) & sequence(s) name
            Under the form {name_seq1: seq1, name_seq2: seq2}
    """
    sequences = {}
    counter_unknow_seq = 1
    counter_same_name = 1

    with file as f:
        sequence_name = ""
        sequence = ""
        for line in f:  # iterate through each line of the file
            line = line.strip()  # removing both the leading and the trailing characters of the line
            if line.startswith(">"):  # if sequence header
                if sequence_name != "":
                    # If 2 different RNA sequences have the same name
                    if sequence_name in sequences.keys() and sequences[sequence_name] != sequence:
                        sequence_name = sequence_name + str(counter_same_name)
                        counter_same_name += 1

                    sequences[sequence_name] = sequence  # add previous sequence to dictionary
                    sequence = ""
                sequence_name = line[1:]
                if sequence_name == "":  # if sequence without informations/header
                    sequence_name = "Unknow sequence " + str(counter_unknow_seq)
                    counter_unknow_seq += 1
            else:  # if it is a sequence line
                sequence += line

        # If 2 different RNA sequences have the same name
        if sequence_name in sequences.keys() and sequences[sequence_name] != sequence:
            sequence_name = sequence_name + str(counter_same_name)
            counter_same_name += 1
        sequences[sequence_name] = sequence # add previous sequence to dictionary
    print(sequences)
    return sequences


def check_rna_seq(sequence):
    """
    Check if it's an RNA sequence.
    If it's a DNA sequence, transform it into an RNA sequence.
    Otherwise return an error.
    input: RNA or DNA sequence
    output: RNA sequence
    """
    sequence = sequence.upper()
    list_nucleotides = ["A", "T", "G", "C", "U"]
    for i in range(len(sequence)):
        # replacing T by U
        if sequence[i] == "T":
            sequence = sequence[:i] + "U" + sequence[i+1:]
        elif sequence[i] not in list_nucleotides:
            raise ValueError("The sequence entered is not an RNA or DNA sequence")

    return sequence


def run_programs(sequence, verbose=False):
    """
    get sequence from arguments
    """
    sequence = check_rna_seq(sequence)
    matches = ["_"] * len(sequence)
    matrix = run_matrix(sequence)
    traceback(matrix, "wx", (0, len(sequence) - 1), matches, verbose)
    return (matches, matrix)


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


def save_into_file(args, output):
    """
    output with or without argument after the flag
    """
    if args.save is not None:
        args.save.write(output)
    else:
        from tkinter import filedialog
        if '--save' in sys.argv[1::] or '-s' in sys.argv[1::]:
            file = filedialog.asksaveasfile(mode='x', title="save file")
            file.write(output)


args = parser()
output = program_parse(args)
save_into_file(args, output)
