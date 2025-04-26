# Igniscript

Igniscript e uma linguagem de programacao que utiliza conceitos tradicionais de logica, atribuicao, controle de fluxo e entrada/saida para programar o comportamento do painel de um carro.

O programa interage com atributos do carro como velocidade, RPM, marcha, entre outros, e deve gerenciar recursos como gasolina, respeitar limites mecanicos e responder a condicoes como o motor estar ligado ou nao.

Com o objetivo de ensinar e incentivar pessoas que gostam de carros a aprender programacao, Igniscript adota um linguajar simples e familiar, transformando conceitos tecnicos em comandos intuitivos. Ao usar combustivel como recurso limitado, ela estimula o pensamento logico com foco na eficiencia. No processo, a linguagem continua com potencial como uma ferramenta para resolver problemas computacionais, exemplo no final da pagina.

---
## O carro possui o seguinte estado interno:

- `gasolina` (100 litros)  cada operacao consome 1 litro
- `rpm`
- `velocidade`
- `ligado` (carOn ou carOff)
- `marcha`
- `cavalos` (potencia do motor  influencia a velocidade de execucao)

## Regras de execucao

- Cada operacao computacional (binaria, unaria, laco, condicional) consome:
  - +100 RPM
  - -1 litro de gasolina

- o carro comeca com 120 cavalos (quanto mais cavalos menor e o tempo para compilar.)
- e possivel aumentar a cavalaria do carro, mas isso gasta mais gasolina por operacao.

- O `rpm` nao pode ser alterado diretamente pelo programador.
- O programador e responsavel por trocar de marcha usando `marcha tune marcha gearUp 1`.

### Limites de RPM por marcha

| Marcha | RPM Maximo | Operacoes permitidas |
|--------|------------|----------------------|
| 1      | 2000       | 20                   |
| 2      | 4000       | 20                   |
| 3      | 6000       | 20                   |
| 4      | 8000       | 20                   |
| 5      | 10000      | 20                   |

- Se ultrapassar o RPM da marcha atual, o programa encerra com erro.
- Se acabar a gasolina, o carro desliga imediatamente.

---

## EBNF da Igniscript

```ebnf
<programa>         ::= { <instrucao> }

<instrucao>        ::= <declaracao>
                     | <atribuicao>
                     | <impressao>
                     | <entrada>
                     | <info> //falta implementar!!!
                     | <condicional>
                     | <repeticao>
                     | "neutral"

<bloco>            ::= "greenLight" { <instrucao> } "redLight"

<declaracao>       ::= identifier "horsepower"
                     | identifier "plate"
                     | identifier "status"

<atribuicao>       ::= identifier "tune" <bexpr> "pitStop"

<impressao>        ::= "flash" "(" <bexpr> ")" "pitStop"

<entrada>          ::= identifier "tune" "sensor()" "pitStop"

<info>             ::= "info" "(" ")" "pitStop" // falta implementar!!

<condicional>      ::= "checkIgnition" "(" <bexpr> ")" <bloco> [ "backup" <bloco> ]

<repeticao>        ::= "duringEngineRev" "(" <bexpr> ")" <bloco>

<bexpr>            ::= <bterm> { "ignite" <bterm> }

<bterm>            ::= <relExpr> { "traction" <relExpr> }

<relExpr>          ::= <expr> ( "sameAs" | "overdrive" | "underride" ) <expr>

<expr>             ::= <termo> { ("gearUp" | "gearDown" | "turboBoost") <termo> }

<termo>            ::= <fator> { ("accelerate" | "clutch") <fator> }

<fator>            ::= horsepower
                     | status
                     | plate
                     | identifier
                     | "gearUp" <fator>
                     | "gearDown" <fator>
                     | "reverse" <fator>
                     | "(" <bexpr> ")"
                     | "sensor()"

<type>              ::= "horsepower" | "status" | "plate"

<boolean>           ::= "carOn" | "carOff"

<number>            ::= [ "-" ] <digit> { <digit> }

<string>            ::= "\""" {{ qualquer_caractere_que_nao_seja_aspas }} "\"""

<id>                ::= <letter> {{ <letter> | <digit> | "_" }}

<letter>            ::= "a" | ... | "z" | "A" | ... | "Z"
<digit>             ::= "0" | ... | "9"
 
```

---

## Tabela de Equivalencia Lexical

| Tipo lexico tradicional | Token na Igniscript            |
|-------------------------|--------------------------------|
| i32                     | horsepower                     |
| bool                    | status                         |
| str                     | plate                          |
| true / false            | carOn / carOff                 |
| =                       | tune                           |
| ;                       | pitStop                        |
| + / -                   | gearUp / gearDown              |
| * / /                   | accelerate / clutch            |
| ++                      | turboBoost                     |
| !                       | reverse                        |
| && / ||                 | traction / ignite              |
| == / < / >              | sameAs / underride / overdrive |
| if / else               | checkIgnition / backup         |
| while                   | duringEngineRev                |
| { / }                   | greenLight / redLight          |
| print(...)              | flash(...)                     |
| read()                  | sensor()                       |
| ; (comando vazio)       | neutral                        |
| info()                  | info()                         |

---

## Desafio proposto: O Desafio de Gauss. Objetivo: ensinar a programar utilizando um alfabeto familiar para quem gosta de carros, incentivando o uso de uma solucao otima.

Programe a Igniscript para calcular a soma de todos os numeros de 1 a 100, e exibir o resultado.

O resultado correto deve ser: 5050.

Restricoes:
- Voce pode usar no maximo 5 operacoes computacionais (i.e. consumir no maximo 5 litros de gasolina e 500 RPM)
- O programa deve terminar com:
  - Pelo menos 95 litros de gasolina
  - RPM inferior a 2000
  - Na primeira marcha
  - Desligar o carro apos uso

Dica:
- Fazer soma numero a numero com `duringEngineRev` acaba com a gasolina do carro.
- Aplique uma solucao matematica otimizada, pesquise sobre formula de Gauss:

---

## Exemplo de solucao correta

```car

greenLight

ligado status tune carOn pitStop
marcha horsepower tune 1 pitStop

n horsepower tune 100 pitStop
aux horsepower tune n gearUp 1 pitStop
soma horsepower tune n accelerate aux pitStop
soma tune soma clutch 2 pitStop

flash("Soma de 1 a 100: soma") pitStop
info() pitStop

ligado status tune carOff pitStop
redLight


```