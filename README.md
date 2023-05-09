# A Dynamic Programming Algorithm for RNA Structure Prediction Including Pseudoknots

*CIESLA Julie, GODET Chloé, GROSJACQUES Marwane, HAMOUDI Nabil*

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)
## 🎓 Presentation
This is a graduation project. 

The goal was to implement an RNA secondary structure prediction algorithm using dynamic programmation.
Our work is based on [A Dynamic Programming Algorithm for RNA Structure Prediction Including Pseudoknots](https://github.com/Nabil-hamoudi/Program_RNA-Structure_Python/blob/main/references/A%20Dynamic%20Programming%20Algorithm%20for%20RNA%20Structure.pdf) by Elena Rivas and Sean R. Eddy. 

This program is coded in Python and has a time complexity of O(n⁶).
It is capable of predicting the following structures :
* hairpin loop
* stem
* bulge
* internal loop
* multiloop
* pseudoknot (only the three most common topologies)


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)
## :construction: Installation
- Python version used : 3.10.10
- tkinter version 8.6 or newer 
(you can install it with `pip install tk`). If pip is not installed, you can follow this link : https://pip.pypa.io/en/stable/installation
- JAVA for VARNA : http://varna.lri.fr/index.php?lang=en&page=home&css=varna



![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)
## :computer: How to use the program
The following command lines must be run in a terminal by executing the file [`algo.py`](https://github.com/Nabil-hamoudi/Program_RNA-Structure_Python/blob/main/algo.py).

```
algo.py [-h] [-i [SEQUENCE] | -f [FASTA_FILE]] [-s [FILE_PATH]] [-t] [-g [DIRECTORY_PATH]]
```

> Note: The program can take several minutes or even several hours to run.

> Note: All flags can be used together except -i and -f.


### Enter an RNA sequence

Use the flag **-i** or **--input** follow by your sequence.
In order to launch the program you can can directly enter an RNA or DNA sequence (which will be automatically converted into an RNA sequence). The sequence must be composed of the following characters: A, C, G, U, T, a, c, g, u, t.

```sh 
python3 algo.py -i sequence
``` 

Examples : 
```sh
python3 algo.py −i AAAUCCAAAGCGAUUUCG
python3 algo.py −i aaauccaaagcauuucg
python3 algo.py −i AAauCCAaAGcGAUUuCG
python3 algo.py −i AAATCCAAAGCATTTCG
python3 algo.py −−input AAATCCAAAGCATTTCG
```


### Load a file in fasta format

Instead of entering a sequence by hand you can choose to use a fasta file (containing one or more RNA or DNA sequence(s)).
To do this, use the flag: **-f** or **--file_input**.

Two options are available:

→ Enter the path leading to the fasta file

```sh
python3 algo.py -f path/file
```
where *path* is the path leading to the fasta *file*.

Examples :

```sh
python3 algo.py −f C:\path\to\file.fasta
python3 algo.py --file_input relative/path/to/file.fasta

```
→ Do not write anything after the flag, in this case the file explorer will open and you can directly select the file to open.
Examples : 
```sh
python3 algo.py -f
python3 algo.py --file_input
```
> Note: If no flag is entered, the file explorer opens by default.


### Save the results

If you want to save the results, use the flag **-s** or **--save**. 

Then 2 options are available:

→ Enter the path to choose where to save the file.
```sh
python3 algo.py -f -s path/file.txt
```
where *path* is the path leading to the *file* which is the name of the file with its extension.

Examples : 
```sh
python3 algo.py −f C:\path\to\file.fa -s C:\path\to\result.txt
python3 algo.py -f -s relative/path/to/result.txt
```
→ Do not enter anything, in this case a window will open to invite you to select the location of the backup and the name of the file. 
Examples : 
```sh
python3 algo.py -f -s
python3 algo.py −f C:\path\to\file.fa -s
```


### Generate and save a graph

Pour générer et enregistrer un graphe représentant la structure secondaire de l'ARN vous pouvez utiliser le flag -g ou --graph. 

Then 2 options are available:

→ Enter the path to choose where to save the file.

```sh
python3 algo.py -f -g path/directory
```
where *path* is the path leading to the *directory* which will contains the graphs

Examples : 
```sh
python3 algo.py -f -g C:\path\to\directory
python3 algo.py -g path/to/directory
```

→ Do not enter anything, in this case a window will open to invite you to select the location of the backup and the name of the file. 
Examples : 
```sh
python3 algo.py -f -g
python3 algo.py −i AGCUC -g
```
> Note: to use this feature you must have [java](https://www.java.com/fr/) installed on your machine.
> Note: the default name of the graph directory is results


### Display traceback

It is possible to display the traceback using the flag **-t** or **--traceback**. This feature is especially useful for developers, as it makes it easier to debug the program. Indeed, it makes it possible to display for each recursion, the current matrix, the indices studied, the best score and the matrices of the next recursion.

Examples : 
```sh
python3 algo.py -f -t
python3 algo.py −i AGCUC -t
python3 algo.py −i AGCUC --traceback
```

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)
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
