# A Dynamic Programming Algorithm for RNA Structure Prediction Including Pseudoknots

*CIESLA Julie, GODET Chloé, GROSJACQUES Marwane, HAMOUDI Nabil*


## Presentation
RNA secondary structure prediction using dynamic programmation from a given sequence of RNA.

## Installation
- Python version used : 3.10.10
- tkinter version 8.6 or newer 
(you can install it with `pip install tk`). If pip is not installed, you can follow this link : https://pip.pypa.io/en/stable/installation
- JAVA for VARNA : http://varna.lri.fr/index.php?lang=en&page=home&css=varna

## Content
The folder RNA_Program contains : 
* rapport.pdf
* references
    * 1985_Sankoff.pdf
    * A Dynamic Programming Algorithm for RNA Structure.pdf
    * complete set of recursion.pdf
    * HIV-1-RT-ligand RNA pseudoknots.pdf
    * Improvedfree-energyparametersforpredictionsofRNAduplexstability.pdf
* results
    * pseudoknot_example.jpeg
* seq
* src
    * matrices
        * matrix_vhx.py
        * matrix_vx.py
        * matrix_whx.py
        * matrix_wx.py
        * matrix_wxi.py
        * matrix_yhx.py
        * matrix_zhx.py
    * create_matrices.py
    * main.py
    * output.py
    * parameters.py
    * program_parser.py
    * sequence_handling.py
    * traceback_RNA.py
* structures tools
    * VARNAv3-93.jar
    * find_structures
        * find_structures.l
        * find_structures.y
        * Makefile
        * README.md
        * test
- algo.py
- README.md

## Utilisation
