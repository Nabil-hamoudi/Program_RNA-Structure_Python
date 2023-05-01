def seq_same_name(sequences, sequence, sequence_name, counter_same_name):
    """
    If in the fasta file, 2 different RNA sequences have the same name
    change the name of one of the sequences
    Input:
        sequences: dictionnary containing the sequences and their name as key
        sequence: string containing the sequence to add
        sequence_name: string containing the name of the sequence to add
        counter_same_name: integer
    Output:
        string containing the name of the sequence to add
        integer of the number of sequences that have the same name
    """
    # if sequence_name already in dictionary with a different RNA string
    if (sequence_name in sequences.keys()) and \
       (sequences[sequence_name] != sequence):
        sequence_name = sequence_name + " (" + str(counter_same_name) + ")"
        counter_same_name += 1

    return sequence_name, counter_same_name


def reading_fasta_file(fasta_file_path):
    """
    Reading file containing RNA (or DNA) sequence
    Input:
        fasta_file_path: path to the fasta file to read
    Output:
        dictionnary containing the sequences and their name as key
    """
    # variable initialization
    sequences = {}
    counter_unknown_seq = 1
    counter_same_name = 1
    sequence_name = ""
    sequence = ""

    with fasta_file_path as fasta_file:
        for line in fasta_file:  # iterate through each line of the file
            line = line.strip()  # removing both the leading and the trailing characters of the line
            if line.startswith(">"):  # if sequence header
                if sequence_name != "":
                    sequence_name, counter_same_name = seq_same_name(sequences,
                                                                     sequence,
                                                                     sequence_name,
                                                                     counter_same_name)
                    sequences[sequence_name.strip()] = sequence  # add previous sequence to dictionary
                    sequence = ""
                sequence_name = line[1:]
                if sequence_name == "":  # if sequence without informations/header
                    sequence_name = "Unknown sequence " + str(counter_unknown_seq)
                    counter_unknown_seq += 1
            elif sequence_name == "": # if the file doesn't start with an header
                raise IOError("The given file isn't a fasta file")
            else:  # if it is a sequence line
                sequence += line

        sequence_name, counter_same_name = seq_same_name(sequences, sequence,
                                                         sequence_name, counter_same_name)
        sequences[sequence_name.strip()] = sequence  # add previous sequence to dictionary

    return sequences


def check_rna_seq(sequence, sequence_name):
    """
    Check if the sequence isn't empty.
    Check if it's an RNA sequence.
    If it's a DNA sequence, transform it into an RNA sequence.
    Otherwise return an error.
    input:
        sequence: string containing a DNA or RNA sequence
        sequence_name: string containing the name of the sequence
    output:
        string containing an RNA sequence
        return empty string if there is an error
    """
    
    # check if sequence is empty
    if sequence == "":
        print(f"WARNING : The sequence {sequence_name} is empty\n")
        return ""
  
    sequence = sequence.upper()
    list_nucleotides = ["A", "T", "G", "C", "U"]
    for i in range(len(sequence)):
        # replacing T by U
        if sequence[i] == "T":
            sequence = sequence[:i] + "U" + sequence[i+1:]
        elif sequence[i] not in list_nucleotides:
            print(f"WARNING : The sequence {sequence_name} is not an RNA or DNA sequence\n") 
            return ""
        

    return sequence
