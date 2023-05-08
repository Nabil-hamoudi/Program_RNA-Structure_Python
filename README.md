# Program Prediction of Secondary Structure RNA

## Dependancy

### Required
 - Python 3.XX

### Optional
 - Tkinter (version 8.6 or newer)
 - Java (version ?)

## Presentation of the project

RNA secondary structure prediction using dynamic programmation from a given sequence of RNA.

## Content and Code structuration

<!--## [```seq```](https://github.com/Nabil-hamoudi/Program_RNA-Structure_Python/tree/main/seq "online git of seq folder") -->

## ```seq```
 - Reference RNA sequence
    #### ```seq_PKNOT``` contain RNA sequence but in there configuration there is pseudoknot

<!--    #### [```seq_PKNOT```](https://github.com/Nabil-hamoudi/Program_RNA-Structure_Python/tree/main/seq/seq_PKNOT "online git of seq_PKNOT folder") contain RNA sequence but in there configuration there is pseudoknot -->

<!--## [```src```](https://github.com/Nabil-hamoudi/Program_RNA-Structure_Python/tree/main/seq "online git of seq folder") -->

## ```src```
 - ## Code folder
    ### ```main.py```
     - main file contain base code to start the code and handle the input/output file
         #### ```get_sequences(args)```
          - ##### take argument from parser format (see args)
    ### ```parameters.py```
     - file containing all the parameters use by the program
    ### ```create_matrices.py```
     - contain the initaialisation function for matrices
    ### ```output.py```
     - contain function to display the result and make graph
    ### ```program_parser.py```
     - contain all the function to make the flags and parser code to launch the program (see how to use part for the explaination of flags)
         #### ```args```
          - ##### structure containing all data enter by the user it's create by argparse and modify by the ```parser_function``` by adding default option or modify certain entry like the directory
    ### ```sequence_handling.py```
     - handle the input sequence, contain a function to verify if a sequence is RNA or verify input file is a fasta and get the sequence inside
    ### ```traceback_RNA.py```
     - 
    ## Folder '```matrices```'
     - ### ```matrix_wx.py```
     - ### ```matrix_vx.py```
     - ### ```matrix_wxi.py```
     - ### ```matrix_vhx.py```
     - ### ```matrix_yhx.py```
     - ### ```matrix_zhx.py```
     - ### ```matrix_whx.py```

# How to use

