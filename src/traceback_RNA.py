def traceback(matrix, current_matrix_name, indices, matches, verbose=False):
    """
    Recursive function to traceback the matrices to get the optimal path and deduce the optimal structures
    Fill the list matches
    Input:
        matrix: dictionnary of the matrices
        current_matrix_name: string of the name of the matrix to trace
        indices: list of 2 or 4 indices depending of the matrix
        matches: list where the ith nucleotide is:
                  - not paired if matches[i] is None
                  - paired to matches[i]th nucleotide if matches[i] is an integer
                 for 0 <= i < sequence length
        verbose_traceback: boolean, True  - the traceback should be printed
                                    False - the traceback should not be printed
    No output
    """
  
    # recover the best score and the matrices used to obtain it
    if len(indices) == 2: # matrices vx, wx and wxi
        best_score  = matrix[current_matrix_name][indices[1]][indices[0]][0]
        matrices_used = matrix[current_matrix_name][indices[1]][indices[0]][1]
    elif len(indices) == 4: # matrices vhx, whx, yhx and zhx
        best_score = matrix[current_matrix_name][indices[1]][indices[3]][indices[2]][indices[0]][0]
        matrices_used = matrix[current_matrix_name][indices[1]][indices[3]][indices[2]][indices[0]][1]
    else: raise IndexError("Invalid number of indices.")
        
    if verbose:    
        print("------------------------------------------------------------------------")
        print(f"Current matrix : {current_matrix_name}\nindices : {indices}")
        print("best score :", round(best_score, 2))


    # for each tuple in list matrices_used
    if verbose:
        for matrix_used in matrices_used:
            print(f"trace {matrix_used[0]} {matrix_used[1:]}")

    for matrix_used in matrices_used:
        matrix_name = matrix_used[0]
        
        if "EIS" in matrix_name:
            continue
    
        if matrix_name == "vx":
            matches[matrix_used[1]] = matrix_used[2]
            matches[matrix_used[2]] = matrix_used[1]
            continue

        if matrix_name == "yhx" or matrix_name == "vhx":
            matches[matrix_used[3]] = matrix_used[4]
            matches[matrix_used[4]] = matrix_used[3]


        if matrix_name == "zhx" or matrix_name == "vhx":
            matches[matrix_used[1]] = matrix_used[2]
            matches[matrix_used[2]] = matrix_used[1]


        traceback(matrix, matrix_name, matrix_used[1:], matches, verbose)



def matches2dbn(matches):
    """
    translate the 'matches' list into dot-bracket notation (DBN)
    Input:
        matches: list where the ith nucleotide is:
                  - not paired if matches[i] is None
                  - paired to matches[i]th nucleotide if matches[i] is an integer
                 for 0 <= i < sequence length
    Output:
        string of a sequence structure in DBN format
    """
    # copy the list matches
    dbn = list(matches)
    
    for position in range(len(dbn)):
        if dbn[position] is None: # unpaired
            dbn[position] = '.'
        
        elif isinstance(dbn[position], str): # already changed
            continue

        else: # paired
            # for more and more complex pseudoknot
            # we need to add more and more kinds of brackets
            if ')' in dbn[position:dbn[position]]:
                if ']' in dbn[position:dbn[position]]:
                    if '}' in dbn[position:dbn[position]]:
                        if '>' in dbn[position:dbn[position]]:
                            raise ValueError("Unsupported DBN format for this pseudoknot")
                        else: 
                            dbn[dbn[position]] = '>'
                            dbn[position] = '<'
                    else: 
                        dbn[dbn[position]] = '}'
                        dbn[position] = '{'
                else: 
                    dbn[dbn[position]] = ']'
                    dbn[position] = '['
            else: 
                dbn[dbn[position]] = ')'
                dbn[position] = '('
            
    return ''.join(dbn)
