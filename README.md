# Igniscript

Igniscript is a programming language that uses traditional concepts of logic, assignment, control flow, and input/output to program the behavior of a car’s dashboard.

The program interacts with car attributes such as speed, RPM, gear, among others, and must manage resources like fuel, respect mechanical limits, and respond to conditions such as whether the engine is on or off.

With the aim of teaching and encouraging car enthusiasts to learn programming, Igniscript adopts simple and familiar language, turning technical concepts into intuitive commands. By using fuel as a limited resource, it stimulates logical thinking with a focus on efficiency. In the process, the language still has potential as a tool for solving computational problems, as shown in the example at the end of the page.

---
## The car has the following internal state:

- `gasoline` (100 liters)  each operation consumes 1 liter  
- `rpm`  
- `speed`  
- `on` (carOn or carOff)  
- `gear`  
- `horsepower` (engine power influences execution speed)  

## Execution rules

- Each computational operation (binary, unary, loop, conditional) consumes:  
  - +100 RPM  
  - -1 liter of gasoline  

- The car starts with 120 horsepower (the more horsepower, the shorter the compile time).  
- It is possible to increase the car’s horsepower, but this consumes more gasoline per operation.

- `rpm` cannot be altered directly by the programmer.  
- The programmer is responsible for shifting gears using `gear tune gear gearUp 1`.  

### RPM Limits per gear

| Gear | Max RPM | Allowed operations |
|------|---------|--------------------|
| 1    | 2000    | 20                 |
| 2    | 4000    | 20                 |
| 3    | 6000    | 20                 |
| 4    | 8000    | 20                 |
| 5    | 10000   | 20                 |

- If the RPM of the current gear is exceeded, the program terminates with an error.  
- If the fuel runs out, the car shuts off immediately.  

---

## Igniscript EBNF

```ebnf
<program>           ::= { <instruction> }

<instruction>       ::= <declaration>
                     | <assignment>
                     | <print>
                     | <input>
                     | <info> // not implemented yet!!!
                     | <conditional>
                     | <loop>
                     | "neutral"

<block>             ::= "greenLight" { <instruction> } "redLight"

<declaration>       ::= identifier "horsepower"
                     | identifier "plate"
                     | identifier "status"

<assignment>        ::= identifier "tune" <bexpr> "pitStop"

<print>             ::= "flash" "(" <bexpr> ")" "pitStop"

<input>             ::= identifier "tune" "sensor()" "pitStop"

<info>              ::= "info" "(" ")" "pitStop"  // not implemented yet!!!

<conditional>       ::= "checkIgnition" "(" <bexpr> ")" <block> [ "backup" <block> ]

<loop>              ::= "duringEngineRev" "(" <bexpr> ")" <block>

<bexpr>             ::= <bterm> { "ignite" <bterm> }

<bterm>            ::= <relExpr> { "traction" <relExpr> }

<relExpr>           ::= <expr> ( "sameAs" | "overdrive" | "underride" ) <expr>

<expr>              ::= <term> { ("gearUp" | "gearDown" | "turboBoost") <term> }

<term>              ::= <factor> { ("accelerate" | "clutch") <factor> }

<factor>            ::= horsepower
                     | status
                     | plate
                     | identifier
                     | "gearUp" <fator>
                     | "gearDown" <factor>
                     | "reverse" <factor>
                     | "(" <bexpr> ")"
                     | "sensor()"

<type>              ::= "horsepower" | "status" | "plate"

<boolean>           ::= "carOn" | "carOff"

<number>            ::= [ "-" ] <digit> { <digit> }

<string>            ::= "\"" {{ any_character_except_quote }} "\""

<id>                ::= <letter> {{ <letter> | <digit> | "_" }}

<letter>            ::= "a" | ... | "z" | "A" | ... | "Z"
<digit>             ::= "0" | ... | "9"

| Traditional lexical type | Token in Igniscript            |   |                   |
| ------------------------ | ------------------------------ | - | ----------------- |
| i32                      | horsepower                     |   |                   |
| bool                     | status                         |   |                   |
| str                      | plate                          |   |                   |
| true / false             | carOn / carOff                 |   |                   |
| =                        | tune                           |   |                   |
| ;                        | pitStop                        |   |                   |
| + / -                    | gearUp / gearDown              |   |                   |
| \* / /                   | accelerate / clutch            |   |                   |
| ++                       | turboBoost                     |   |                   |
| !                        | reverse                        |   |                   |
| && /                     |                                |   | traction / ignite |
| == / < / >               | sameAs / underride / overdrive |   |                   |
| if / else                | checkIgnition / backup         |   |                   |
| while                    | duringEngineRev                |   |                   |
| { / }                    | greenLight / redLight          |   |                   |
| print(...)               | flash(...)                     |   |                   |
| read()                   | sensor()                       |   |                   |
| ; (empty command)        | neutral                        |   |                   |
| info()                   | info()                         |   |                   |

Proposed challenge: The Gauss Challenge
Objective: to teach programming using an alphabet familiar to car enthusiasts, encouraging the use of an optimal solution.

Write an Igniscript program to calculate the sum of all numbers from 1 to 100 and display the result.

The correct result should be: 5050.

Constraints:

You may use at most 5 computational operations (i.e., consume at most 5 liters of gasoline and 500 RPM).

The program must end with:

At least 95 liters of gasoline

RPM below 2000

In first gear

Turn off the car after use

Tip:

Summing number by number with duringEngineRev uses up the car's gasoline.

Apply an optimized mathematical solution, research the Gauss formula:

greenLight

on status tune carOn pitStop
gear horsepower tune 1 pitStop

n horsepower tune 100 pitStop
aux horsepower tune n gearUp 1 pitStop
sum horsepower tune n accelerate aux pitStop
sum tune sum clutch 2 pitStop

flash("Sum of 1 to 100: sum") pitStop
info() pitStop

on status tune carOff pitStop
redLight
