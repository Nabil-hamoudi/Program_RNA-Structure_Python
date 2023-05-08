# A Dynamic Programming Algorithm for RNA Structure Prediction Including Pseudoknots

*CIESLA Julie, GODET Chloé, GROSJACQUES Marwane, HAMOUDI Nabil*

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)
## Presentation
RNA secondary structure prediction using dynamic programmation from a given sequence of RNA.

## Installation
- Python version used : 3.10.10
- tkinter version 8.6 or newer 
(you can install it with `pip install tk`). If pip is not installed, you can follow this link : https://pip.pypa.io/en/stable/installation
- JAVA for VARNA : http://varna.lri.fr/index.php?lang=en&page=home&css=varna

## :open_file_folder: Content
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
* seq (*a lot of sequences for testing, they're not essentials*)
    * seq_PKNOT
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

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)
## How to use the program
The following command lines must be run in a terminal by executing the file algo.py.
> Note: The program can take several minutes or even several hours to run.

- Enter an RNA sequence

Use the flag -i or --input follow by your sequence.
In order to launch the program you can can directly enter an RNA or DNA sequence (which will be automatically converted into an RNA sequence). The sequence must be composed of the following characters: A, C, G, U, T, a, c, g, u, t.

```sh
python3 algo.py −i AAAUCCAAAGCGAUUUCG
python3 algo.py −i aaauccaaagcauuucg
python3 algo.py −i AAauCCAaAGcGAUUuCG
python3 algo.py −i AAATCCAAAGCATTTCG
python3 algo.py −−input AAATCCAAAGCATTTCG
```

- Load a file in fasta format

Instead of entering a sequence by hand you can choose to use a fasta file (containing one or more RNA or DNA sequence(s)).
To do this, use the flag: -f or --file_input. Two options are available:

→ Enter the path leading to the fasta file
```sh
python3 algo.py −f C:\xxx\xxxx\yyy.fa
python3 algo.py --file_input C:\xxx\xxxx\yyy.fa
```
→ Do not write anything after the flag, in this case the file explorer will open and you can directly select the file to open.
```sh
python3 algo.py -f
python3 algo.py --file_input
```
> Note: If no flag is entered, the file explorer opens by default.

- Save the results

If you want to save the results, use the flag -s or --save. Then 2 options are available:

→ Enter the path to choose where to save the file.
```sh
python3 algo.py −f C:\xxx\xxxx\yyy.fa -s C:\xxx\xxxxxx\xx\file_name.txt
python3 algo.py -f -s C:\xxx\xxxxxx\xx\file_name.txt
```
→ Do not enter anything, in this case a window will open to invite you to select the location of the backup and the name of the file. 
```sh
python3 algo.py -f -s
python3 algo.py −f C:\xxx\xxxx\yyy.fa -s
```

- Generate and save a graph

Pour générer et enregistrer un graphe représentant la structure secondaire de l'ARN vous pouvez utiliser le flag -g ou --graph. Then 2 options are available:

→  Enter the path to choose where to save the file.
```sh
python3 algo.py -f -g C:\xxx\xxxxxx\xx
```
→ Do not enter anything, in this case a window will open to invite you to select the location of the backup and the name of the file. 
```sh
python3 algo.py -f -g
python3 algo.py −i AGCUC -g
```
> Note: to use this feature you must have [java](https://www.java.com/fr/) installed on your machine.

- Afficher le traceback

It is possible to display the traceback using the flag -t or --traceback. This feature is especially useful for developers, as it makes it easier to debug the program. Indeed, it makes it possible to display for each recursion, the current matrix, the indices studied, the best score and the matrices of the next recursion.
```sh
python3 algo.py -f -t
python3 algo.py −i AGCUC -t
python3 algo.py −i AGCUC --traceback
