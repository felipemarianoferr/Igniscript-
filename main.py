from compiler.Parser import *
import sys

if __name__ == "__main__":

    igniscript_direct_reverse_test = """
    greenLight
    inteiro horsepower tune 10 pitStop
    flash(inteiro gearUp gearDown 5) pitStop
    redLight
    """
    
    Parser.run(igniscript_direct_reverse_test)