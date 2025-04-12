# Igniscript

Uma linguagem de programacao tematica inspirada no universo automotivo.

---

## EBNF

```
<program>           ::= { <statement> }

<statement>         ::= <declaration>
                     | <assignment>
                     | <print>
                     | <conditional>
                     | <loop>
                     | "pitStop"

<declaration>       ::= <id> <type> [ "tune" <relationalExpr> ] "pitStop"

<assignment>        ::= <id> "tune" <relationalExpr> "pitStop"

<print>             ::= "flash" "(" <relationalExpr> ")" "pitStop"

<conditional>       ::= "checkIgnition" "(" <relationalExpr> ")"
                        "greenLight" { <statement> }
                      [ "backup" "greenLight" { <statement> } ]
                        "redLight"

<loop>              ::= "duringEngineRev" "(" <relationalExpr> ")"
                        "greenLight" { <statement> }
                        "redLight"

<relationalExpr>    ::= <expression> [ ("sameAs" | "overdrive" | "underride") <expression> ]

<expression>        ::= <term> { ("gearUp" | "gearDown") <term> }

<term>              ::= <factor> { ("accelerate" | "clutch") <factor> }

<factor>            ::= <number>
                     | <boolean>
                     | <string>
                     | <id>
                     | "sensor" "(" ")"
                     | "(" <relationalExpr> ")"
                     | "+" , <factor>
                     | "-" , <factor>

<type>              ::= "horsepower" | "status" | "plate"

<boolean>           ::= "carOn" | "carOff"

<number>            ::= [ "-" ] <digit> { <digit> }

<string>            ::= "\""" {{ qualquer_caractere_que_nao_seja_aspas }} "\"""

<id>                ::= <letter> {{ <letter> | <digit> | "_" }}

<letter>            ::= "a" | ... | "z" | "A" | ... | "Z"
<digit>             ::= "0" | ... | "9"
```

---

## Tabela de Equivalencia

| Sua Linguagem             | Programacao Tradicional           |
|---------------------------|-----------------------------------|
| `nome horsepower`         | Declaracao de variavel inteira    |
| `nome plate`              | Declaracao de variavel string     |
| `nome status`             | Declaracao de variavel booleana   |
| `nome tune valor`         | Atribuicao                        |
| `sensor()`                | Entrada de dados                  |
| `flash("mensagem")`       | Impressao                         |
| `pitStop`                 | Fim de instrucao                  |
| `gearUp`                  | Soma (`+`)                        |
| `gearDown`                | Subtracao (`-`)                   |
| `accelerate`              | Multiplicacao (`*`)               |
| `clutch`                  | Divisao (`/`)                     | 
| `carOn`                   | Verdadeiro (`true`)               |
| `carOff`                  | Falso (`false`)                   |
| `checkIgnition (cond)`    | Condicional (`if`)                |
| `backup`                  | Alternativa (`else`)              |
| `greenLight`              | Inicio de bloco                   |
| `redLight`                | Fim de bloco                      |
| `duringEngineRev (cond)`  | Laco de repeticao (`while`)       |
| `sameAs`                  | Igualdade (`==`)                  |
| `overdrive`               | Maior que (`>`)                   |
| `underride`               | Menor que (`<`)                   |
| `( ... )`                 | Agrupamento                       |

---

## Exemplo de Codigo

```txt
rpm horsepower tune sensor() pitStop
alert status tune carOn pitStop

checkIgnition (rpm overdrive 4000)
greenLight
    flash("RPM too high!") pitStop
    alert tune carOff pitStop
redLight

duringEngineRev (rpm underride 6000)
greenLight
    rpm tune rpm gearUp 500 pitStop
    flash("Increasing speed...") pitStop
redLight
```
## Traducao para C

```txt

#include <stdio.h>

int main() {
    int rpm;
    int alert;

    scanf("%d", &rpm);

    alert = 1;

    if (rpm > 4000) {
        printf("RPM too high!\n");
        alert = 0; // false (carOff)
    }

    while (rpm < 6000) {
        rpm = rpm + 500;
        printf("Increasing speed...\n");
    }

    return 0;
}

```
