# filename: applied_tests.py

# Test basic syntax parsing and evaluation (pre-CarState)
igniscript_gauss_syntax_test = """
greenLight
ligado status tune carOn pitStop
marcha horsepower tune 1 pitStop
n horsepower tune 100 pitStop
aux horsepower tune n gearUp 1 pitStop
soma horsepower tune n accelerate aux pitStop
soma tune soma clutch 2 pitStop
temp_plate plate tune "Soma de 1 a 100: " turboBoost soma pitStop
flash(temp_plate) pitStop
info() pitStop
ligado tune carOff pitStop
redLight
"""

# Test basic resource consumption and info() command (Post-CarState)
igniscript_test_basic_consumption = """
greenLight
    info() pitStop
    ligado status tune carOn pitStop
    marcha horsepower tune 1 pitStop
    info() pitStop
    temp horsepower pitStop
    temp tune 5 gearUp 3 pitStop
    info() pitStop
    ligado tune carOff pitStop
redLight
"""

# Test running out of gas (requires high HP input, e.g., 1000)
igniscript_test_out_of_gas = """
greenLight
    ligado status tune carOn pitStop
    marcha horsepower tune 1 pitStop
    i horsepower tune 0 pitStop
    limit horsepower tune 101 pitStop
    info() pitStop
    duringEngineRev (i underride limit) greenLight
        i tune i gearUp 1 pitStop
        flash(i) pitStop
        info() pitStop
    redLight
    info() pitStop
redLight
"""

# Test hitting RPM limit in Gear 1 (requires 120 HP input)
igniscript_test_rpm_limit_g1_corrected = """
greenLight
    ligado status tune carOn pitStop
    marcha horsepower tune 1 pitStop
    i horsepower tune 0 pitStop
    limit horsepower tune 10 pitStop
    info() pitStop
    duringEngineRev (i underride limit) greenLight
        i tune i gearUp 1 pitStop
        flash(i) pitStop
        info() pitStop
    redLight
    flash("Error: RPM limit not triggered!") pitStop
redLight
"""

# Test shifting gears before hitting RPM limit (requires 120 HP input)
igniscript_test_gear_shift_final_corrected = """
greenLight
    ligado status tune carOn pitStop
    marcha horsepower tune 1 pitStop
    i horsepower tune 0 pitStop
    limit horsepower tune 5 pitStop
    flash("Running in Gear 1 towards limit...") pitStop
    info() pitStop
    duringEngineRev (i underride limit) greenLight
        i tune i gearUp 1 pitStop
        flash(i) pitStop
        info() pitStop
    redLight
    flash("Reached near Gear 1 limit. Shifting...") pitStop
    info() pitStop
    marcha tune 2 pitStop
    flash("Now in Gear 2.") pitStop
    info() pitStop
    temp horsepower pitStop
    temp tune i gearUp 1 pitStop
    flash("Performed operation in Gear 2.") pitStop
    flash(temp) pitStop
    info() pitStop
    ligado tune carOff pitStop
redLight
"""

# Test attempting computational operation in Neutral (Gear 0)
igniscript_test_neutral_gear = """
greenLight
    ligado status tune carOn pitStop
    info() pitStop
    temp horsepower pitStop
    temp tune 1 gearUp 1 pitStop
    info() pitStop
    flash("Error: Operation allowed in Neutral gear!") pitStop
    ligado tune carOff pitStop
redLight
"""

# Test attempting operation while engine is off
igniscript_test_engine_off = """
greenLight
    info() pitStop
    temp horsepower pitStop
    temp tune 5 pitStop
    flash("Error: Assignment allowed while engine off!") pitStop
redLight
"""

# Test increased gas consumption with higher horsepower (requires high HP input, e.g., 240)
igniscript_test_hp_gas = """
greenLight
    ligado status tune carOn pitStop
    marcha horsepower tune 1 pitStop
    info() pitStop
    temp horsepower pitStop
    temp tune 1 gearUp 1 pitStop
    info() pitStop
    ligado tune carOff pitStop
redLight
"""

# Test error condition if program finishes with engine still on
igniscript_test_final_engine_on = """
greenLight
    ligado status tune carOn pitStop
    marcha horsepower tune 1 pitStop
    temp horsepower pitStop
    temp tune 1 gearUp 0 pitStop
redLight
"""

# Test conditional logic (if/else) and boolean operators (and/or) - ADAPTED for CarState
igniscript_conditional_test = """
greenLight
    ligado status tune carOn pitStop  // ADDED SETUP
    marcha horsepower tune 1 pitStop // ADDED SETUP
    num1 horsepower pitStop
    num2 horsepower pitStop
    result_and status pitStop
    result_or status pitStop
    flash("Enter first number (horsepower):") pitStop
    num1 tune sensor() pitStop
    flash("Enter second number (horsepower):") pitStop
    num2 tune sensor() pitStop
    result_and tune (num1 overdrive 5) traction (num2 underride 10) pitStop
    result_or tune (num1 sameAs 0) ignite (num2 sameAs 0) pitStop
    flash("Testing AND (num1 > 5 traction num2 < 10):") pitStop
    checkIgnition (result_and) greenLight
        flash("  Condition is carOn (True)") pitStop
    redLight
    backup greenLight
        flash("  Condition is carOff (False)") pitStop
    redLight
    flash("Testing OR (num1 == 0 ignite num2 == 0):") pitStop
    checkIgnition (result_or) greenLight
        flash("  At least one number is zero.") pitStop
    redLight
    backup greenLight
        flash("  Neither number is zero.") pitStop
    redLight
    temp horsepower pitStop
    flash("Testing Odd/Even for num1:") pitStop
    temp tune num1 clutch 2 pitStop
    temp tune temp accelerate 2 pitStop
    checkIgnition (num1 sameAs temp) greenLight
         flash("  Num1 seems Even") pitStop
    redLight
    backup greenLight
         flash("  Num1 seems Odd") pitStop
    redLight
    ligado tune carOff pitStop
redLight
"""

# Test odd/even logic with single input - ADAPTED for CarState
igniscript_odd_even_test = """
greenLight
    ligado status tune carOn pitStop  // ADDED SETUP
    marcha horsepower tune 1 pitStop // ADDED SETUP
    num horsepower pitStop
    temp horsepower pitStop
    flash("Enter a number (horsepower):") pitStop
    num tune sensor() pitStop
    temp tune num clutch 2 pitStop
    temp tune temp accelerate 2 pitStop
    flash("Result:") pitStop
    checkIgnition (num sameAs temp) greenLight
         flash("  Num is Even") pitStop
    redLight
    backup greenLight
         flash("  Num is Odd") pitStop
    redLight
    ligado tune carOff pitStop
redLight
"""

# Test 'reverse' (NOT) operator directly in flash command - ADAPTED for CarState
igniscript_direct_reverse_test = """
greenLight
    ligado status tune carOn pitStop  // ADDED SETUP
    marcha horsepower tune 1 pitStop // ADDED SETUP
    engineRunning status pitStop
    engineRunning tune carOn pitStop
    flash("Initial engine status:") pitStop
    flash(engineRunning) pitStop
    flash("Directly reversed status:") pitStop
    flash(reverse engineRunning) pitStop // reverse is UnOp, needs engine/gear
    ligado tune carOff pitStop
redLight
"""

# Final Gauss problem test with concatenation for printing
igniscript_gauss_final_test = """
greenLight
    ligado status tune carOn pitStop
    marcha horsepower tune 1 pitStop
    n horsepower tune 100 pitStop
    aux horsepower tune n gearUp 1 pitStop
    soma horsepower tune n accelerate aux pitStop
    soma tune soma clutch 2 pitStop
    temp_plate plate pitStop
    temp_plate tune "Soma de 1 a 100: " turboBoost soma pitStop
    flash(temp_plate) pitStop
    info() pitStop
    ligado tune carOff pitStop
redLight
"""