from compiler.Parser import *
import sys

if __name__ == "__main__":

    igniscript_direct_reverse_test = """
    greenLight
        ligado status tune carOn pitStop
        marcha horsepower tune 1 pitStop
        engineRunning status pitStop
        engineRunning tune carOn pitStop
        flash("Initial engine status:") pitStop
        flash(engineRunning) pitStop
        flash("Directly reversed status:") pitStop
        flash(reverse engineRunning) pitStop // reverse is UnOp, needs engine/gear
        ligado tune carOff pitStop
    redLight
    """

    Parser.run(igniscript_direct_reverse_test)