from compiler.Parser import *
import sys

if __name__ == "__main__":

    igniscript_teste_minimo = """
    greenLight
        flash(1) pitStop
        ligado tune carOff pitStop
    redLight
    """

    Parser.run(igniscript_teste_minimo, "saida.asm")