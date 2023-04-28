from output import *
from traceback_RNA import *
from sequence_handling import *
from create_matrices import *
from matrices import matrix_wx
#parser
from program_parser import parser_function

# Default constant for file display
GRAPH_EXTENSION = ".jpeg"

def get_output(sequence, sequence_name, verbose_traceback, graphe_directory=None):
    """
    docstring
    """
    matches, best_score = run_programs(sequence, verbose_traceback)
    output = display_results(sequence_name, sequence, matches, best_score) + '\n'
    if graphe_directory is not None:
        draw_graph(os.path.join(graphe_directory, sequence_name + GRAPH_EXTENSION), sequence, matches)
    return output


def program_parse(args):
    """
    parse with flag: ['-i', '--input'] or ['-f', '--file_input'] or no flag
    """
    if args.input is not None:
        sequence = check_rna_seq(args.input)
        sequence_name = "Unknow sequence"
        output = get_output(sequence, sequence_name, args.traceback, args.graph)
    else:
        dict_seq = reading_fasta_file(args.file_input)
        output = ""
        for sequence_name in dict_seq:
            sequence = check_rna_seq(dict_seq[sequence_name])
            output += get_output(sequence, sequence_name, args.traceback, args.graph)
    return output


def run_programs(sequence, verbose=False):
    """
    Start the dynamic programming algorithm
    """
    # initialize matrices
    matrix = create_matrices(len(sequence))
    fill_matrices(matrix)

    # start the algorithm
    matrix_wx.matrix_wx(0, len(sequence)-1, matrix, sequence)

    # traceback
    matches = ["_"] * len(sequence)
    traceback(matrix, "wx", (0, len(sequence) - 1), matches, verbose)

    best_score = matrix["wx"][len(sequence) - 1][0][0]

    return (matches, best_score)


if __name__ == "__main__":
    args = parser_function()
    output = program_parse(args)

    # write into file if we save
    if args.save is not None:
        args.save.write(output)
