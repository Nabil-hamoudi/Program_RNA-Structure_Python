%{
#include <stdio.h>
#include <stdlib.h>
extern FILE *yyin;

#if YYBISON
int yylex();
int yyerror();
#endif

// functions for each irreducible surface's order
void IS1(int size);
void IS2(int left_size, int right_size);
void IS3_and_more(int nb_structures);

// pseudoknot processing function
void pseudoknot(int nb_bra_o, int nb_bra_c);

// counters
int nb_hairpin = 0;
int nb_stem = 0;
int nb_bulge = 0;
int nb_internal_loop = 0;
int nb_multiloop = 0;
int nb_pseudoknot = 0;
%}

%token PAR_O PAR_C
%token BRA_O BRA_C
%token CUR_O CUR_C
%token LOW_O GRE_C
%token DOT

%%

sequence:
				dots
		|		dots pair sequence
		|		dots pseudoknot sequence
		;

dots:
				/* epsilon */	{ $$ = 0; }
		|		DOT dots		{ $$ = $2 + 1; }
		;

bras_O:
				BRA_O			{ $$ = 1; }
		|		BRA_O bras_O	{ $$ = $2 + 1; }
		;

bras_C:
				BRA_C			{ $$ = 1; }
		|		BRA_C bras_C	{ $$ = $2 + 1; }
		;

pair:
				PAR_O surface PAR_C
		;

surface:
	   			dots 			{ IS1($1); }
		|		dots pair dots	{ IS2($1, $3); }
		|		multiloop 		{ IS3_and_more($1); }
		;

multiloop:
				multiloop pair dots 		{ $$ = $1 + 1; }
        |		dots pair dots pair dots 	{ $$ = 2; }
        ;

pseudoknot:
		  		pseudoknot_pair dots bras_C { pseudoknot($1, $3); }

pseudoknot_pair:
				PAR_O dots pseudoknot_pair dots PAR_C 	{ $$ = $3; }
		|		PAR_O dots bras_O dots PAR_C		 			{ $$ = $3; }
		;
%%

void IS1(int size) {
	/*
	Process hairpin loop
	and update the counter
	Input:
		size: integer of the size in nucleotide of the hairpin
	No output
	*/
	if (size >= 3) {
		printf("\thairpin of size %d\n", size);
		nb_hairpin++;
	} else {
		printf("INVALID hairpin of size %d\n", size);
	}
}

void IS2(int left_size, int right_size) {
	/*
	Analyze what kind of irreducible surface of order 2 it is
	and update the corresponding counter
	Input:
		left_size: integer of the number of nucleotide on the 5' end
		right_size: integer of the number of nucleotide on the 3' end
	No output
	*/
	if (left_size == 0) {
		if (right_size == 0) {	// stem
			printf("\tstem\n");
			nb_stem++;
		} else {				// right bulge
			printf("\tright bulge of size %d\n", right_size);
			nb_bulge++;
		}
	} else {
		if (right_size == 0) {	// left bulge
			printf("\tleft bulge of size %d\n", left_size);
			nb_bulge++;
		} else {				// internal loop 
			printf("\tinternal loop of size %d\n", left_size + right_size);
			nb_internal_loop++;
		}
	}
}

void IS3_and_more(int nb_structures) {
	/*
	Process multiloop
	and update the counter
	Input:
		nb_structures: integer of the number of structures contained in the multiloop
	No output
	*/
	printf("\tmultiloop with %d structures\n", nb_structures);
	nb_multiloop++;
}

void pseudoknot(int nb_bra_o, int nb_bra_c) {
	/*
	Process pseudoknot by checking if there is an equal number of
	opening bracket and closing bracket
	then update the counter
	Input:
		nb_bra_o: integer of the number of '['
		nb_bra_c: integer of the number of ']'
	No output
	*/
	if (nb_bra_o != nb_bra_c) {
		printf("INVALID pseudoknot: %d opening brackets for %d closing brackets\n", nb_bra_o, nb_bra_c);
	} else {
		printf("\tpseudoknot\n");
		nb_pseudoknot++;
	}
}

int main(int argc, char *argv[]) {
	/*
	Input:
		argc: number of arguments
		argv: vector of arguments
	Output:
		exit status as integer
	*/
	if (argc >= 2) yyin = fopen(argv[1], "r");
	printf("Secondary structure analysis of the DBN sequence:\n");
	yyparse();
	printf("Total counts:\n");
	printf("%d hairpin%c\n", nb_hairpin, (nb_hairpin > 1)?'s':' ');
	printf("%d stem%c\n", nb_stem, (nb_stem > 1)?'s':' ');
	printf("%d bulge%c\n", nb_bulge, (nb_bulge > 1)?'s':' ');
	printf("%d internal loop%c\n", nb_internal_loop, (nb_internal_loop > 1)?'s':' ');
	printf("%d multiloop%c\n", nb_multiloop, (nb_multiloop > 1)?'s':' ');
	printf("%d pseudoknot%c\n\n", nb_pseudoknot, (nb_multiloop > 1)?'s':' ');
	return 0;
}
