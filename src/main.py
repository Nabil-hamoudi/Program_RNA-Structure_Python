import sys
import argparse
from tkinter import filedialog
#temporaire
from test_matrices import *


# Parser
parser = argparse.ArgumentParser()

input_group = parser.add_mutually_exclusive_group(required=False)
input_group.add_argument('-i', '--input', help='input an RNA sequence', type=str, nargs='?')
input_group.add_argument('-f', '--file_input', help='input a Fasta file of an RNA sequence', type=argparse.FileType('r'), nargs='?')
parser.add_argument('-s', '--file_output', help='save the output into a file', type=argparse.FileType('x'), required=False, nargs='?')
parser.add_argument('-t', '--traceback', help='display the traceback or not', action='store_true', required=False)

args = parser.parse_args(sys.argv[1::])


def reading_fasta_file(file):
    """
    Reading file containing arn (or dna) sequence
    Input: file .txt or .fasta
    Output: RNA (or DNA) sequence & sequence name
    """
    with file as f:
        sequence = ""
        name_seq = ""
        line = f.readline()
        while line != "":
            # if not a description line
            if line[0] != ">":
                sequence = sequence + line[: len(line)-1]
                line = f.readline()
            else:
                name_seq = line[1: len(line)-1]
                line = f.readline()

        if name_seq == "":
            name_seq = "No information on the sequence studied"

    sequence = sequence.upper()

    return sequence, name_seq


def check_rna_seq(sequence):
    """
    Check if it's an RNA sequence.
    If it's a DNA sequence, transform it into an RNA sequence.
    Otherwise return an error.
    input: rna or dna sequence
    output: rna sequence
    """
    list_nucleotides = ["A", "T", "G", "C", "U"]
    for i in range(len(sequence)):
        if sequence[i] == "T":
            sequence = sequence[:i] + "U" + sequence[i+1:]
        elif sequence[i] not in list_nucleotides:
            raise ValueError("The sequence entered is not an RNA or DNA sequence")

    return sequence


def run_programs(sequence):
    """
    get sequence from arguments
    """
    sequence = check_rna_seq(sequence)
    matches = ["_"] * len(sequence)
    matrix = run_matrix(sequence)
    traceback(matrix, "wx", (0, len(sequence) - 1), matches)
    return (matches, matrix)

# parse with flag: ['-i', '--input'] or --file_input or no flag
if args.input is not None:
    sequence = check_rna_seq(args.input)
    sequence_name = None
    matches, matrix = run_programs(sequence)
elif args.file_input is not None:
    sequence, sequence_name = reading_fasta_file(args.file_input)
    print(sequence)
    sequence = check_rna_seq(sequence)
    matches, matrix = run_programs(sequence)
else:
    file = filedialog.askopenfile(mode='r')
    sequence, sequence_name = reading_fasta_file(file)
    sequence = check_rna_seq(sequence)
    matches, matrix = run_programs(sequence)

# make the display
output = display(sequence, matches, matrix["wx"][len(sequence) - 1][0][0])

# output with or without argument after the flag
if args.file_output is not None:
    args.file_output.write(output)
else:
    if '--file_output' in sys.argv[1::] or '-o' in sys.argv[1::]:
        file = filedialog.asksaveasfile(mode='x', title="output.log")
        file.write(output)
