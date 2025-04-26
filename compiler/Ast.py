class Node():
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st, cs):
        pass

class Info(Node):
     def Evaluate(self, st, cs):

          print(cs.get_state_info())

class BinOp(Node):
    def Evaluate(self, st, cs):
        op_name = f"BinOp '{self.value}'"
        cs.notify_engine_required_operation(op_name)

        tuple1 = self.children[0].Evaluate(st, cs)
        tuple2 = self.children[1].Evaluate(st, cs)
        type1 = tuple1[1]
        type2 = tuple2[1]
        val1 = tuple1[0]
        val2 = tuple2[0]

        result = None
        result_type = None

        if self.value == '+':
            if type1 == 'i32' and type2 == 'i32':
                result = val1 + val2
                result_type = 'i32'
            else:
                raise Exception(f"TypeError: Operator '+' (gearUp) only supports i32 (horsepower), not '{type1}' and '{type2}'")

        elif self.value == '-':
            if type1 == 'i32' and type2 == 'i32':
                result = val1 - val2
                result_type = 'i32'
            else:
                raise Exception(f"TypeError: Operator '-' (gearDown) only supports i32 (horsepower), not '{type1}' and '{type2}'")

        elif self.value == '*':
            if type1 == 'i32' and type2 == 'i32':
                result = val1 * val2
                result_type = 'i32'
            else:
                raise Exception(f"TypeError: Operator '*' (accelerate) only supports i32 (horsepower), not '{type1}' and '{type2}'")

        elif self.value == '/':
            if type1 == 'i32' and type2 == 'i32':
                if val2 == 0:
                     raise Exception("RuntimeError: Division by zero")
                result = val1 // val2
                result_type = 'i32'
            else:
                raise Exception(f"TypeError: Operator '/' (clutch) only supports i32 (horsepower), not '{type1}' and '{type2}'")

        elif self.value == '||':
            if type1 == 'bool' and type2 == 'bool':
                result = val1 or val2
                result_type = 'bool'
            else:
                raise Exception(f"TypeError: Operator '||' (ignite) only supports bool (status), not '{type1}' and '{type2}'")

        elif self.value == '&&':
            if type1 == 'bool' and type2 == 'bool':
                result = val1 and val2
                result_type = 'bool'
            else:
                raise Exception(f"TypeError: Operator '&&' (traction) only supports bool (status), not '{type1}' and '{type2}'")

        elif self.value == '==':
             if type1 == type2 and type1 in ['i32', 'bool', 'str']:
                 result = val1 == val2
                 result_type = 'bool'
             else:
                 raise Exception(f"TypeError: Operator '==' (sameAs) cannot compare types '{type1}' and '{type2}'")

        elif self.value == '<':
             if type1 == 'i32' and type2 == 'i32':
                 result = val1 < val2
                 result_type = 'bool'
             elif type1 == 'str' and type2 == 'str':
                  result = val1 < val2
                  result_type = 'bool'
             else:
                 raise Exception(f"TypeError: Operator '<' (underride) only supports i32 (horsepower) or str (plate) comparison, not '{type1}' and '{type2}'")

        elif self.value == '>':
             if type1 == 'i32' and type2 == 'i32':
                 result = val1 > val2
                 result_type = 'bool'
             elif type1 == 'str' and type2 == 'str':
                  result = val1 > val2
                  result_type = 'bool'
             else:
                 raise Exception(f"TypeError: Operator '>' (overdrive) only supports i32 (horsepower) or str (plate) comparison, not '{type1}' and '{type2}'")

        elif self.value == '++':
             s1 = ('carOn' if val1 else 'carOff') if type1 == 'bool' else str(val1)
             s2 = ('carOn' if val2 else 'carOff') if type2 == 'bool' else str(val2)
             result = s1 + s2
             result_type = 'str'
        else:
             raise Exception(f"Internal Error: Unknown BinOp operator '{self.value}'")

        cs.consume_resources(op_name)

        return (result, result_type)

class UnOp(Node):
    def Evaluate(self, st, cs):
        op_name = f"UnOp '{self.value}'"
        cs.notify_engine_required_operation(op_name)

        val, tipo = self.children[0].Evaluate(st, cs)

        result = None
        result_type = None

        if self.value == '!':
            if tipo != 'bool':
                raise Exception(f"TypeError: Operator '!' (reverse) only supports bool (status), not '{tipo}'")
            result = not val
            result_type = 'bool'
        elif self.value == '-':
            if tipo != 'i32':
                raise Exception(f"TypeError: Operator '-' (gearDown) only supports i32 (horsepower), not '{tipo}'")
            result = -val
            result_type = 'i32'
        elif self.value == '+':
            if tipo != 'i32':
                raise Exception(f"TypeError: Operator '+' (gearUp) only supports i32 (horsepower), not '{tipo}'")
            result = val
            result_type = 'i32'
        else:
             raise Exception(f"Internal Error: Unknown UnOp operator '{self.value}'")

        cs.consume_resources(op_name)

        return (result, result_type)


class While(Node):
    def Evaluate(self, st, cs):
        op_name = "While (duringEngineRev)"
        iteration_check_name = op_name + " condition check"

        while True:
             cs.notify_engine_required_operation(iteration_check_name)
             cond_val, cond_type = self.children[0].Evaluate(st, cs)
             if cond_type != 'bool':
                 raise Exception(f"TypeError: While condition (duringEngineRev) must be bool (status), not '{cond_type}'")

             cs.consume_resources(iteration_check_name)

             if not cond_val:
                 break

             self.children[1].Evaluate(st, cs)

class If(Node):
    def Evaluate(self, st, cs):
        op_name = "If (checkIgnition)"
        condition_check_name = op_name + " condition check"

        cs.notify_engine_required_operation(condition_check_name)
        cond_val, cond_type = self.children[0].Evaluate(st, cs)
        if cond_type != 'bool':
            raise Exception(f"TypeError: If condition (checkIgnition) must be bool (status), not '{cond_type}'")

        block_executed = False
        if cond_val:
            self.children[1].Evaluate(st, cs)
            block_executed = True
        elif len(self.children) > 2:
            self.children[2].Evaluate(st, cs)
            block_executed = True

        if block_executed:
            cs.consume_resources(op_name)


class Read(Node):
    def Evaluate(self, st, cs):
        op_name = "Read (sensor)"

        try:
             user_input = input()
             return (int(user_input), 'i32')
        except ValueError:
             raise Exception("RuntimeError: Invalid input via sensor(), expected an integer (horsepower).")
        except EOFError:
             raise Exception("RuntimeError: Input stream closed unexpectedly during sensor().")


class Block(Node):
    def Evaluate(self, st, cs):
        for child in self.children:
            child.Evaluate(st, cs)

class Assignment(Node):
    def Evaluate(self, st, cs):
        key = self.children[0].value
        op_name = f"Assignment to '{key}'"

        is_turning_engine_on = (key == 'ligado' and isinstance(self.children[1], BoolVal) and self.children[1].value is True)

        if not is_turning_engine_on:
             cs.notify_engine_required_operation(op_name)

        value_tuple = self.children[1].Evaluate(st, cs)
        new_value = value_tuple[0]

        if key == 'marcha':
             if value_tuple[1] != 'i32':
                  raise TypeError(f"Cannot assign type '{value_tuple[1]}' to 'marcha', expected horsepower (i32).")
             cs.set_gear(new_value)
        elif key == 'ligado':
             if value_tuple[1] != 'bool':
                  raise TypeError(f"Cannot assign type '{value_tuple[1]}' to 'ligado', expected status (bool).")
             cs.set_engine_on_off(new_value)
        elif key == 'cavalos':
             if value_tuple[1] != 'i32':
                  raise TypeError(f"Cannot assign type '{value_tuple[1]}' to 'cavalos', expected horsepower (i32).")
             cs.set_horsepower(new_value)
        else:
             st.setter(key, value_tuple)


class Identifier(Node):
    def Evaluate(self, st, cs):
        
        return st.getter(self.value)

class Print(Node):
    def Evaluate(self, st, cs):
        op_name = "Print (flash)"
        
        value, type = self.children[0].Evaluate(st, cs)

        if type == 'bool':
             output_str = 'carOn' if value else 'carOff'
             print(output_str)
        else:
             print(value)


class IntVal(Node):
    def Evaluate(self, st, cs):
        return (self.value, 'i32')

class BoolVal(Node):
    def Evaluate(self, st, cs):
        return (self.value, 'bool')

class StrVal(Node):
    def Evaluate(self, st, cs):
        return (self.value, 'str')

class VarDec(Node):
    def Evaluate(self, st, cs):
        igniscript_type = self.value
        identifier_node = self.children[0]
        var_name = identifier_node.value
        op_name = f"Variable Declaration '{var_name}'"

        if len(self.children) == 1:
            st.create_variable(var_name, None, igniscript_type)
        elif len(self.children) == 2:
            expression_node = self.children[1]
            value_tuple = expression_node.Evaluate(st, cs)
            st.create_variable(var_name, value_tuple, igniscript_type)
            
            if var_name == 'marcha':
                if value_tuple[1] == 'i32': cs.set_gear(value_tuple[0])
                else: raise TypeError(f"Cannot initialize 'marcha' with type '{value_tuple[1]}'")
            elif var_name == 'ligado':
                 if value_tuple[1] == 'bool': cs.set_engine_on_off(value_tuple[0])
                 else: raise TypeError(f"Cannot initialize 'ligado' with type '{value_tuple[1]}'")
            elif var_name == 'cavalos':
                 
                 if value_tuple[1] == 'i32': cs.set_horsepower(value_tuple[0])
                 else: raise TypeError(f"Cannot initialize 'cavalos' with type '{value_tuple[1]}'")
        else:
             raise Exception(f"Internal Error: VarDec node expected 1 or 2 children, got {len(self.children)}")

class NoOp(Node):
    def Evaluate(self, st, cs):
        pass