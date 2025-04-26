class Node():
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        pass

class BinOp(Node):
    def Evaluate(self, st):
        tuple1 = self.children[0].Evaluate(st)
        tuple2 = self.children[1].Evaluate(st)
        type1 = tuple1[1]
        type2 = tuple2[1]
        val1 = tuple1[0]
        val2 = tuple2[0]

        if self.value == '+':
            if type1 == 'i32' and type2 == 'i32':
                return (val1 + val2, 'i32')
            else:
                raise Exception(f"TypeError: Operator '+' (gearUp) only supports i32 (horsepower), not '{type1}' and '{type2}'")

        elif self.value == '-':
            if type1 == 'i32' and type2 == 'i32':
                return (val1 - val2, 'i32')
            else:
                raise Exception(f"TypeError: Operator '-' (gearDown) only supports i32 (horsepower), not '{type1}' and '{type2}'")

        elif self.value == '*':
            if type1 == 'i32' and type2 == 'i32':
                return (val1 * val2, 'i32')
            else:
                raise Exception(f"TypeError: Operator '*' (accelerate) only supports i32 (horsepower), not '{type1}' and '{type2}'")

        elif self.value == '/':
            if type1 == 'i32' and type2 == 'i32':
                if val2 == 0:
                     raise Exception("RuntimeError: Division by zero")
                return (val1 // val2, 'i32')
            else:
                raise Exception(f"TypeError: Operator '/' (clutch) only supports i32 (horsepower), not '{type1}' and '{type2}'")

        elif self.value == '||':
            if type1 == 'bool' and type2 == 'bool':
                return (val1 or val2, 'bool')
            else:
                raise Exception(f"TypeError: Operator '||' (ignite) only supports bool (status), not '{type1}' and '{type2}'")

        elif self.value == '&&':
            if type1 == 'bool' and type2 == 'bool':
                return (val1 and val2, 'bool')
            else:
                raise Exception(f"TypeError: Operator '&&' (traction) only supports bool (status), not '{type1}' and '{type2}'")

        elif self.value == '==':
             if type1 == type2 and type1 in ['i32', 'bool', 'str']:
                 return (val1 == val2, 'bool')
             else:
                 raise Exception(f"TypeError: Operator '==' (sameAs) cannot compare types '{type1}' and '{type2}'")


        elif self.value == '<':
             if type1 == 'i32' and type2 == 'i32':
                 return (val1 < val2, 'bool')
             elif type1 == 'str' and type2 == 'str':
                  return (val1 < val2, 'bool')
             else:
                 raise Exception(f"TypeError: Operator '<' (underride) only supports i32 (horsepower) or str (plate) comparison, not '{type1}' and '{type2}'")

        elif self.value == '>':
             if type1 == 'i32' and type2 == 'i32':
                 return (val1 > val2, 'bool')
             elif type1 == 'str' and type2 == 'str':
                  return (val1 > val2, 'bool')
             else:
                 raise Exception(f"TypeError: Operator '>' (overdrive) only supports i32 (horsepower) or str (plate) comparison, not '{type1}' and '{type2}'")

        elif self.value == '++':
             # Convert booleans to 'carOn'/'carOff' before string conversion for turboBoost
             s1 = ('carOn' if val1 else 'carOff') if type1 == 'bool' else str(val1)
             s2 = ('carOn' if val2 else 'carOff') if type2 == 'bool' else str(val2)
             return (s1 + s2, 'str')

class UnOp(Node):
    def Evaluate(self, st):
        val, tipo = self.children[0].Evaluate(st)

        if self.value == '!':
            if tipo != 'bool':
                raise Exception(f"TypeError: Operator '!' (reverse) only supports bool (status), not '{tipo}'")
            return (not val, 'bool')
        elif self.value == '-':
            if tipo != 'i32':
                raise Exception(f"TypeError: Operator '-' (brake) only supports i32 (horsepower), not '{tipo}'")
            return (-val, 'i32')
        elif self.value == '+':
            if tipo != 'i32':
                raise Exception(f"TypeError: Operator '+' (turbo) only supports i32 (horsepower), not '{tipo}'")
            return (val, 'i32')


class While(Node):
    def Evaluate(self, st):
        while True:
             cond_val, cond_type = self.children[0].Evaluate(st)
             if cond_type != 'bool':
                 raise Exception(f"TypeError: While condition (duringEngineRev) must be bool (status), not '{cond_type}'")
             if not cond_val:
                 break
             self.children[1].Evaluate(st)


class If(Node):
    def Evaluate(self, st):
            cond_val, cond_type = self.children[0].Evaluate(st)
            if cond_type != 'bool':
                raise Exception(f"TypeError: If condition (checkIgnition) must be bool (status), not '{cond_type}'")
            if cond_val:
                self.children[1].Evaluate(st)
            elif len(self.children) > 2:
                self.children[2].Evaluate(st)

class Read(Node):
    def Evaluate(self, st):
        try:
             user_input = input()
             # Attempt to return based on expected type? Or always i32?
             # For now, keep as original, returning i32 for sensor()
             return (int(user_input), 'i32')
        except ValueError:
             raise Exception("RuntimeError: Invalid input via sensor(), expected an integer (horsepower).")
        except EOFError:
             raise Exception("RuntimeError: Input stream closed unexpectedly during sensor().")


class Block(Node):
    def Evaluate(self, st):
        for child in self.children:
            child.Evaluate(st)

class Assignment(Node):
    def Evaluate(self, st):
        key = self.children[0].value
        value_tuple = self.children[1].Evaluate(st)
        st.setter(key, value_tuple)

class Identifier(Node):
    def Evaluate(self, st):
        return st.getter(self.value)

class Print(Node):
    def Evaluate(self, st):
        value, type = self.children[0].Evaluate(st)
        if type == 'bool':
             output_str = 'carOn' if value else 'carOff'
             print(output_str)
        else:
             print(value)


class IntVal(Node):
    def Evaluate(self, st):
        return (self.value, 'i32')

class BoolVal(Node):
    def Evaluate(self, st):
        return (self.value, 'bool')

class StrVal(Node):
    def Evaluate(self, st):
        return (self.value, 'str')

class VarDec(Node):
    def Evaluate(self, st):
        igniscript_type = self.value
        identifier_node = self.children[0]

        if len(self.children) == 1: # Handle declaration only: identifier type pitStop
            st.create_variable(identifier_node.value, None, igniscript_type)
        elif len(self.children) == 2: # Handle declaration with assignment: identifier type tune expr pitStop
            expression_node = self.children[1]
            value_tuple = expression_node.Evaluate(st)
            st.create_variable(identifier_node.value, value_tuple, igniscript_type)
        else:
             # This case should ideally not be reached if the parser is correct
             raise Exception(f"Internal Error: VarDec node expected 1 or 2 children, got {len(self.children)}")

class NoOp(Node):
    def Evaluate(self, st):
        pass