import sys

def display_results(name_sequence, sequence, matches, best_score):
    """output the results of the given sequence"""
    
    output = f"## Results for {name_sequence} ##\n" + f"length of the sequence : {len(sequence)} nucleotides" \
            + "\nenergy : " + str(round(best_score, 2)) + " kcal/mol\n"
                                                                                      
    for nucleotide in sequence: output += nucleotide + "  "
    output += "\n"
    for position in range(len(sequence)): output += str(position) + " "*(3-len(str(position)))
    output += "\n"
    for index in matches:
        if index is None: index = '_'
        output += str(index) + " "*(3-len(str(index)))
    output += "\n"
  
    print(output)
    return output


def print_matrix(matrix, matrix_name):
    """print the given matrix"""
    
    if matrix_name in ["vx", "wx", "wxi"]:
        print("\n##", matrix_name, "##")
        for line in matrix[matrix_name]: print([round(x[0], 2) for x in line])
    elif matrix_name in ["vhx", "whx", "yhx", "zhx"]:
        print("\n##", matrix_name, "##")
        #for line in matrix[matrix_name]: print([round(x[0], 2) for x in line])



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
