def reading_fasta_file(file):
    """
    Reading file containing RNA (or DNA) sequence
    Input: file in fasta format
    Output: dictionary with RNA (or DNA) sequence(s) & sequence(s) name
            Under the form {name_seq1: seq1, name_seq2: seq2}
    """
    sequences = {}
    counter_unknown_seq = 1
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
                    sequence_name = "Unknown sequence " + str(counter_unknown_seq)
                    counter_unknown_seq += 1
            else:  # if it is a sequence line
                sequence += line

        # If 2 different RNA sequences have the same name
        if sequence_name in sequences.keys() and sequences[sequence_name] != sequence:
            sequence_name = sequence_name + str(counter_same_name)
            counter_same_name += 1
        sequences[sequence_name] = sequence # add previous sequence to dictionary
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
