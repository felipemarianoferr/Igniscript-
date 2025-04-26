/* parser.y */
%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int yylex(void);                
void yyerror(const char *s);

%}

%union {
    int    ival;
    char  *sval;
}


%token <ival>  NUMBER
%token <sval>  IDENT STRING

%type <sval> fator

%token CARON CAROFF HORSEPOWER STATUS PLATE
%token TUNE PITSTOP GEARUP GEARDOWN ACCELERATE CLUTCH TURBOBOOST REVERSE
%token TRACTION IGNITE SAMEAS OVERDRIVE UNDERRIDE
%token CHECKIGNITION BACKUP DURING
%token GREENLIGHT REDLIGHT
%token FLASH SENSOR INFO NEUTRAL

%type <ival> expr termo relExpr bexpr bterm

%left IGNITE
%left TRACTION
%nonassoc SAMEAS OVERDRIVE UNDERRIDE
%left GEARUP GEARDOWN
%left TURBOBOOST
%left ACCELERATE CLUTCH
%right REVERSE

%%

programa
    : /* vazio */
    | programa instrucao
    ;

instrucao
    : bloco
    | declaracao
    | atribuicao
    | impressao
    | info_stmt
    | condicional
    | repeticao
    | NEUTRAL PITSTOP
    ;

declaracao
    : IDENT HORSEPOWER PITSTOP
    | IDENT HORSEPOWER TUNE bexpr PITSTOP
    | IDENT STATUS PITSTOP
    | IDENT STATUS TUNE bexpr PITSTOP
    | IDENT PLATE PITSTOP
    | IDENT PLATE TUNE bexpr PITSTOP
    ;

atribuicao
    : IDENT TUNE bexpr PITSTOP
    ;

impressao
    : FLASH '(' bexpr ')' PITSTOP
    ;

info_stmt
    : INFO '(' ')' PITSTOP
    ;

condicional
    : CHECKIGNITION '(' bexpr ')' GREENLIGHT programa REDLIGHT
    | CHECKIGNITION '(' bexpr ')' GREENLIGHT programa REDLIGHT
      BACKUP GREENLIGHT programa REDLIGHT
    ;

repeticao
    : DURING '(' bexpr ')' GREENLIGHT programa REDLIGHT
    ;

bloco
    : GREENLIGHT programa REDLIGHT
    ;

bexpr
    : bterm
    | bexpr IGNITE bterm      { $$ = $1 || $3; }
    ;

bterm
    : relExpr
    | bterm TRACTION relExpr  { $$ = $1 && $3; }
    ;

relExpr
    : expr                    { $$ = $1; }
    | expr SAMEAS expr        { $$ = $1 == $3; }
    | expr OVERDRIVE expr     { $$ = $1 >  $3; }
    | expr UNDERRIDE expr     { $$ = $1 <  $3; }
    ;

expr
    : termo                   { $$ = $1; }
    | expr GEARUP termo       { $$ = $1 + $3; }
    | expr GEARDOWN termo     { $$ = $1 - $3; }
    | expr TURBOBOOST termo   { $$ = $1 * $3; }
    ;

termo
    : fator                   { $$ = atoi($1); free($1); }
    | termo ACCELERATE fator  { $$ = $1 * atoi($3); free($3); }
    | termo CLUTCH fator      { $$ = $1 / atoi($3); free($3); }
    ;

fator
    : NUMBER {
        char buf[32];
        snprintf(buf, sizeof(buf), "%d", $1);
        $$ = strdup(buf);
    }
    | STRING           { $$ = strdup($1); }
    | IDENT            { $$ = strdup($1); }
    | CARON            { $$ = strdup("1"); }
    | CAROFF           { $$ = strdup("0"); }
    | GEARUP fator     { $$ = strdup($2); }
    | GEARDOWN fator   { $$ = strdup($2); }
    | REVERSE fator    { $$ = strdup($2); }
    | '(' bexpr ')'    { $$ = strdup("1"); }
    | SENSOR           { $$ = strdup("sensor()"); }
    ;

%%

int yydebug = 1;
int main(void) {
    yydebug = 1;
    return yyparse();
}

void yyerror(const char *s) {
    fprintf(stderr, "Erro sintático: %s\n", s);
}
