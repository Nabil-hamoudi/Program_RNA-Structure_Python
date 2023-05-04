%{

#include "find_structures.tab.h"

%}


%%
"."		{ return DOT;}

"("		{ return PAR_O;}
")"		{ return PAR_C;}

"["		{ return BRA_O;}
"]"		{ return BRA_C;}

"{"		{ return CUR_O;}
"}"		{ return CUR_C;}

"<"		{ return LOW_O;}
">"		{ return GRE_C;}

[ \t]	{;} /* Ignore les espaces */
\n		{ return 0; } /* fin de traitement par yylex */
. 		{return yytext[0];}
%%
