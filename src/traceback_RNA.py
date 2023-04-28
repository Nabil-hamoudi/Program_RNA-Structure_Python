def traceback(matrix, current_matrix_name, indices, matches, verbose=False):
    """
    traceback the matrices to get the optimal path and deduce the optimal structures
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
    for matrix_used in matrices_used:
        if verbose: print(f"trace {matrix_used[0]} {matrix_used[1:]}")

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
    translate the 'matches' list into dot-bracket notation (dbn)
    """
    # dot-bracket notation
    dbn = list(matches)
    
    for position in range(len(dbn)):
        if dbn[position] is None : 
            dbn[position] = '.'
        
        elif isinstance(dbn[position], str): continue

        else:
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
