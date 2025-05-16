from compiler.Parser import *
import sys

if __name__ == "__main__":

    igniscript_teste_flash_inteiro = """
    greenLight
        ligado status tune carOn pitStop
        flash(1) pitStop
        ligado tune carOff pitStop
    redLight
    """



    Parser.run(igniscript_teste_flash_inteiro, "saida.asm")