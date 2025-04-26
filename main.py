from compiler.Parser import *
import sys

if __name__ == "__main__":

    # source = sys.argv[1]

    # try:
    #     with open(source, "r") as arquivo:
    #         code = arquivo.read()
    # except FileNotFoundError:
    #     code = source

    igniscript_counting_example_corrected = """
        greenLight

        ligado status tune carOn pitStop
        marcha horsepower tune 1 pitStop

        i horsepower tune 1 pitStop
        limite horsepower tune 10 pitStop
        msg plate tune "" pitStop // Declare msg variable for the string

        duringEngineRev (i underride limite gearUp 1) greenLight
            // Explicitly build the string using turboBoost
            msg tune "Contando: " turboBoost i pitStop
            flash(msg) pitStop
            i tune i gearUp 1 pitStop
        redLight

        ligado tune carOff pitStop

        redLight
        """

    Parser.run(igniscript_counting_example_corrected)