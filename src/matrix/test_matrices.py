import sys
from create_matrices import *
import matrix_vx
import matrix_wx
import matrix_wxi

# sequence1 = "UCCGAAGUGCAACGGGAAAAUGCACU"
# sequence2 = "CAGUCAUGCUAGCAUG"
# sequence4 = "GGCACCUCCUCGCGGUGCC"
# sequence3 = "AAACAUGAGGAUUACCCAUGU"
# sequence = "GGCGCAGUGGGCUAGCGCCACUCAAAAGGCCCAU"  # pseudoknot
filename = 'pdb_test.fasta'


def reading_fasta_file(filename):
    """
    Reading file containing arn (or dna) sequence
    Input: file .txt or .fasta
    Output: RNA (or DNA) sequence & sequence name
    """
    with open(filename, "r") as f:
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


sequence, sequence_name = reading_fasta_file(filename)

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


sequence = check_rna_seq(sequence)

#sys.setrecursionlimit(19000)
matrix = create_matrices(len(sequence))
fill_matrices(matrix)

matrix_wx.matrix_wx(0, len(sequence)-1, matrix, sequence)

print("## WX ##")
for line in matrix["wx"]: print([round(x[0], 2) for x in line])
print("## VX ##")
for line in matrix["vx"]: print([round(x[0], 2) for x in line])


def traceback(matrix, current_matrix_name, indices, matches):
    """traceback"""
    
    print("------------------------------------------------------------------------")
    print(f"Current matrix : {current_matrix_name}")
    print(f"indices : {indices}")

    if len(indices) == 2:
        best_score  = matrix[current_matrix_name][indices[1]][indices[0]][0]
        matrices_used = matrix[current_matrix_name][indices[1]][indices[0]][1]
    elif len(indices) == 4:
        best_score = matrix[current_matrix_name][indices[1]][indices[3]][indices[2]][indices[0]][0]
        matrices_used = matrix[current_matrix_name][indices[1]][indices[3]][indices[2]][indices[0]][1]
    else:
        print(f"Index error")

    print("best score :", round(best_score, 2))


    # for each tuple in list matrices_used
    for matrix_used in matrices_used:
        print(f"trace {matrix_used[0]} {matrix_used[1:]}")

    for matrix_used in matrices_used:
        matrix_name = matrix_used[0]
        
        if "EIS" in matrix_name:
            continue
    
        if matrix_name == "vx":
            matches[matrix_used[1]] = matrix_used[2]
            matches[matrix_used[2]] = matrix_used[1]


        elif matrix_name == "vhx":
            matches[matrix_used[1]] = matrix_used[2]
            matches[matrix_used[2]] = matrix_used[1]

            matches[matrix_used[3]] = matrix_used[4]
            matches[matrix_used[4]] = matrix_used[3]



        elif matrix_name == "yhx":
            matches[matrix_used[3]] = matrix_used[4]
            matches[matrix_used[4]] = matrix_used[3]


        elif matrix_name == "zhx":
            matches[matrix_used[1]] = matrix_used[2]
            matches[matrix_used[2]] = matrix_used[1]


        traceback(matrix, matrix_name, matrix_used[1:], matches)


def display(sequence, matches, best_score):
    print()
    print(f"Results : ")
    print("energy (in kcal/mol) :", round(best_score, 2))
    print()
    for nucleotide in sequence:
        print(nucleotide, "  ", sep="", end="")
    print()
    for position in range(len(sequence)):
        print(position, " "*(3-len(str(position))), sep="", end="")
    print()
    for index in matches:
        print(index, " "*(3-len(str(index))), sep="", end="")
        
    print()


# print("\n## WX ##")
# for line in matrix["wx"]: print(line)
# print("\n## WXi ##")
# for line in matrix["wxi"]: print(line)
# print("\n## Whx ##")
# for line in matrix["whx"]: print(line)
# print("\n## vhx ##")
# for line in matrix["vhx"]: print(line)
# print("\n## yhx ##")
# for line in matrix["yhx"]: print(line)
# print("\n## zhx ##")
# for line in matrix["zhx"]: print(line)
matches = ["_"] * len(sequence)
traceback(matrix, "wx", (0, len(sequence) - 1), matches)
display(sequence, matches, matrix["wx"][len(sequence) - 1][0][0])
# avec i = 0 et j = len(sequence) - 1
