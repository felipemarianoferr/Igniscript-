%{
#include "parser.tab.h"
#include <string.h>
#include <stdlib.h>
%}

%option noyywrap
%x COMMENT

%%

"/*"                { BEGIN(COMMENT); }
<COMMENT>"*/"       { BEGIN(INITIAL); }
<COMMENT>.          ;
<COMMENT>\n         ;

"greenLight"        { return GREENLIGHT; }
"redLight"          { return REDLIGHT; }

\"[^\"]*\"          {
                      yylval.sval = strdup(yytext + 1);
                      yylval.sval[strlen(yylval.sval) - 1] = '\0';
                      return STRING;
                    }

"carOn"             { return CARON; }
"carOff"            { return CAROFF; }
"horsepower"        { return HORSEPOWER; }
"status"            { return STATUS; }
"plate"             { return PLATE; }
"tune"              { return TUNE; }
"pitStop"           { return PITSTOP; }
"gearUp"            { return GEARUP; }
"gearDown"          { return GEARDOWN; }
"accelerate"        { return ACCELERATE; }
"clutch"            { return CLUTCH; }
"turboBoost"        { return TURBOBOOST; }
"reverse"           { return REVERSE; }
"traction"          { return TRACTION; }
"ignite"            { return IGNITE; }
"sameAs"            { return SAMEAS; }
"overdrive"         { return OVERDRIVE; }
"underride"         { return UNDERRIDE; }
"checkIgnition"     { return CHECKIGNITION; }
"backup"            { return BACKUP; }
"duringEngineRev"   { return DURING; }
"flash"             { return FLASH; }
"sensor"            { return SENSOR; }
"info"              { return INFO; }
"neutral"           { return NEUTRAL; }

"("                 { return '('; }
")"                 { return ')'; }

[0-9]+              { yylval.ival = atoi(yytext); return NUMBER; }

[a-zA-Z_][a-zA-Z0-9_]* {
                      yylval.sval = strdup(yytext);
                      return IDENT;
                    }

[ \t\r\n]+          ;
"//".*              ;

.                   { return *yytext; }

%%
