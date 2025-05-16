from compiler.Ast import *
from compiler.Tokenizer import Tokenizer
from compiler.SymbolTable import SymbolTable
from compiler.PrePro import PrePro
from compiler.CarState import CarState
from compiler.Code import Code

class Parser:

    tokenizer = None

    def parseTerm():
        ast_node = Parser.parseFactor()
        while Parser.tokenizer.next.tipoToken in ['accelerate', 'clutch', 'turboBoost']:
            op_token = Parser.tokenizer.next.tipoToken
            Parser.tokenizer.selectNext()
            right_node = Parser.parseFactor()

            if op_token == 'accelerate':
                op_symbol = '*'
            elif op_token == 'clutch':
                op_symbol = '/'
            elif op_token == 'turboBoost':
                op_symbol = '++'
            else:
                 raise Exception(f"Unexpected term operator: {op_token}")

            bin_op = BinOp(op_symbol, [ast_node, right_node])
            ast_node = bin_op

        return ast_node

    def parseBoolTerm():
        ast_node = Parser.parseRelExpression()
        while Parser.tokenizer.next.tipoToken in ['traction']:
            Parser.tokenizer.selectNext()
            bin_op = BinOp('&&', [ast_node, Parser.parseRelExpression()])
            ast_node = bin_op
        return ast_node

    def parseBoolExpression():
        ast_node = Parser.parseBoolTerm()
        while Parser.tokenizer.next.tipoToken in ['ignite']:
            Parser.tokenizer.selectNext()
            bin_op = BinOp('||', [ast_node, Parser.parseBoolTerm()])
            ast_node = bin_op
        return ast_node

    def parseRelExpression():
        ast_node = Parser.parseExpression()
        while Parser.tokenizer.next.tipoToken in ['sameAs', 'underride', 'overdrive']:
            op_token = Parser.tokenizer.next.tipoToken
            Parser.tokenizer.selectNext()
            right_node = Parser.parseExpression()

            if op_token == 'sameAs':
                op_symbol = '=='
            elif op_token == 'underride':
                op_symbol = '<'
            elif op_token == 'overdrive':
                op_symbol = '>'
            else:
                raise Exception(f"Unexpected relational operator: {op_token}")

            bin_op = BinOp(op_symbol, [ast_node, right_node])
            ast_node = bin_op
        return ast_node

    def parseFactor():
        token = Parser.tokenizer.next

        if token.tipoToken == 'horsepower_literal':
            int_val = IntVal(token.valorToken, [])
            Parser.tokenizer.selectNext()
            return int_val
        elif token.tipoToken == 'status_literal':
            bool_val = BoolVal(token.valorToken, [])
            Parser.tokenizer.selectNext()
            return bool_val
        elif token.tipoToken == 'plate_literal':
            str_val = StrVal(token.valorToken, [])
            Parser.tokenizer.selectNext()
            return str_val

        elif token.tipoToken == 'identifier':
            identifier = Identifier(token.valorToken, [])
            Parser.tokenizer.selectNext()
            return identifier

        elif token.tipoToken == 'gearUp':
            Parser.tokenizer.selectNext()
            un_op = UnOp('+', [Parser.parseFactor()])
            return un_op
        elif token.tipoToken == 'gearDown':
            Parser.tokenizer.selectNext()
            un_op = UnOp('-', [Parser.parseFactor()])
            return un_op
        elif token.tipoToken == 'reverse':
            Parser.tokenizer.selectNext()
            un_op = UnOp('!', [Parser.parseFactor()])
            return un_op

        elif token.tipoToken == 'OPEN':
            Parser.tokenizer.selectNext()
            result = Parser.parseBoolExpression()
            if Parser.tokenizer.next.tipoToken == 'CLOSE':
                Parser.tokenizer.selectNext()
                return result
            else:
                raise Exception ("Syntax Error: Expected ')'")

        elif token.tipoToken == 'sensor':
             Parser.tokenizer.selectNext()
             if Parser.tokenizer.next.tipoToken == 'OPEN':
                 Parser.tokenizer.selectNext()
                 if Parser.tokenizer.next.tipoToken == 'CLOSE':
                     Parser.tokenizer.selectNext()
                     return Read('sensor', [])
                 else:
                     raise Exception ("Syntax Error: Expected ')' after 'sensor('")
             else:
                 raise Exception ("Syntax Error: Expected '(' after 'sensor'")

        else:
            raise Exception (f"Syntax Error: Unexpected token '{token.tipoToken}' value '{token.valorToken}' found when parsing factor")

    def parseBlock():
        Parser.tokenizer.selectNext()
        block = Block('Block', [])
        while Parser.tokenizer.next.tipoToken != 'redLight':
            if Parser.tokenizer.next.tipoToken == 'EOF':
                raise Exception('Syntax Error: Expected "redLight" but found EOF')

            if Parser.tokenizer.next.tipoToken == 'neutral':
                 Parser.tokenizer.selectNext()
                 if Parser.tokenizer.next.tipoToken != 'pitStop':
                      raise Exception('Syntax Error: Expected "pitStop" after "neutral"')
                 Parser.tokenizer.selectNext()
            elif Parser.tokenizer.next.tipoToken == 'pitStop':
                 Parser.tokenizer.selectNext()
            else:
                child = Parser.parseStatement()
                if child is not None:
                   block.children.append(child)

        Parser.tokenizer.selectNext()
        if len(block.children) == 0:
             return NoOp('NoOp', [])

        return block


    def parseStatement():
        token = Parser.tokenizer.next

        if token.tipoToken == 'identifier':
            identifier_node = Identifier(token.valorToken, [])
            Parser.tokenizer.selectNext()

            if Parser.tokenizer.next.tipoToken in ['TYPE_HORSEPOWER', 'TYPE_STATUS', 'TYPE_PLATE']:
                var_type_token = Parser.tokenizer.next
                Parser.tokenizer.selectNext()

                if var_type_token.tipoToken == 'TYPE_HORSEPOWER':
                     type_str = 'horsepower'
                elif var_type_token.tipoToken == 'TYPE_STATUS':
                     type_str = 'status'
                elif var_type_token.tipoToken == 'TYPE_PLATE':
                     type_str = 'plate'
                else:
                     raise Exception(f"Internal Error: Unexpected type token {var_type_token.tipoToken}")

                if Parser.tokenizer.next.tipoToken == 'tune':
                    Parser.tokenizer.selectNext()
                    expr_node = Parser.parseBoolExpression()

                    if Parser.tokenizer.next.tipoToken != 'pitStop':
                        raise Exception('Syntax Error: Expected "pitStop" after assignment expression')
                    Parser.tokenizer.selectNext()

                    var_decl = VarDec(type_str, [identifier_node, expr_node])
                    return var_decl

                elif Parser.tokenizer.next.tipoToken == 'pitStop':
                     Parser.tokenizer.selectNext()
                     var_decl = VarDec(type_str, [identifier_node])
                     return var_decl
                else:
                     raise Exception(f'Syntax Error: Expected "tune" or "pitStop" after type "{var_type_token.valorToken}"')

            elif Parser.tokenizer.next.tipoToken == 'tune':
                Parser.tokenizer.selectNext()
                expr_node = Parser.parseBoolExpression()

                if Parser.tokenizer.next.tipoToken != 'pitStop':
                    raise Exception('Syntax Error: Expected "pitStop" after assignment expression')
                Parser.tokenizer.selectNext()

                assignment_node = Assignment('=', [identifier_node, expr_node])
                return assignment_node
            else:
                 raise Exception(f'Syntax Error: Expected type keyword or "tune" after identifier "{token.valorToken}"')

        elif token.tipoToken == 'flash':
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.tipoToken == 'OPEN':
                Parser.tokenizer.selectNext()
                expr_node = Parser.parseBoolExpression()
                if Parser.tokenizer.next.tipoToken == 'CLOSE':
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.tipoToken != 'pitStop':
                        raise Exception('Syntax Error: Expected "pitStop" after flash(...)')
                    Parser.tokenizer.selectNext()

                    print_node = Print('flash', [expr_node])
                    return print_node
                else:
                    raise Exception('Syntax Error: Expected ")" after flash expression')
            else:
                raise Exception('Syntax Error: Expected "(" after "flash"')

        elif token.tipoToken == 'duringEngineRev':
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.tipoToken == 'OPEN':
                Parser.tokenizer.selectNext()
                cond_node = Parser.parseBoolExpression()
                if Parser.tokenizer.next.tipoToken == 'CLOSE':
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.tipoToken != 'greenLight':
                        raise Exception('Syntax Error: Expected "greenLight" after duringEngineRev(...)')
                    block_node = Parser.parseBlock()

                    while_node = While('duringEngineRev', [cond_node, block_node])
                    return while_node
                else:
                    raise Exception('Syntax Error: Expected ")" after duringEngineRev condition')
            else:
                raise Exception('Syntax Error: Expected "(" after "duringEngineRev"')

        elif token.tipoToken == 'checkIgnition':
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.tipoToken == 'OPEN':
                Parser.tokenizer.selectNext()
                cond_node = Parser.parseBoolExpression()
                if Parser.tokenizer.next.tipoToken == 'CLOSE':
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.tipoToken != 'greenLight':
                         raise Exception('Syntax Error: Expected "greenLight" after checkIgnition(...)')
                    if_block_node = Parser.parseBlock()

                    if_node = If('checkIgnition', [cond_node, if_block_node])

                    if Parser.tokenizer.next.tipoToken == 'backup':
                        Parser.tokenizer.selectNext()
                        if Parser.tokenizer.next.tipoToken != 'greenLight':
                             raise Exception('Syntax Error: Expected "greenLight" after backup')
                        else_block_node = Parser.parseBlock()
                        if_node.children.append(else_block_node)

                    return if_node
                else:
                    raise Exception('Syntax Error: Expected ")" after checkIgnition condition')
            else:
                raise Exception('Syntax Error: Expected "(" after "checkIgnition"')

        elif token.tipoToken == 'info':
             Parser.tokenizer.selectNext()
             if Parser.tokenizer.next.tipoToken == 'OPEN':
                 Parser.tokenizer.selectNext()
                 if Parser.tokenizer.next.tipoToken == 'CLOSE':
                     Parser.tokenizer.selectNext()
                     if Parser.tokenizer.next.tipoToken == 'pitStop':
                          Parser.tokenizer.selectNext()

                          return Info('info', [])
                     else:
                          raise Exception('Syntax Error: Expected "pitStop" after info()')
                 else:
                     raise Exception ("Syntax Error: Expected ')' after 'info('")
             else:
                 raise Exception ("Syntax Error: Expected '(' after 'info'")

        else:
            raise Exception(f'Syntax Error: Unexpected token "{token.tipoToken}" value "{token.valorToken}" when expecting a statement')


    def parseExpression():
        ast_node = Parser.parseTerm()
        while Parser.tokenizer.next.tipoToken in ['gearUp', 'gearDown']:
            op_token = Parser.tokenizer.next.tipoToken
            Parser.tokenizer.selectNext()
            right_node = Parser.parseTerm()

            if op_token == 'gearUp':
                op_symbol = '+'
            elif op_token == 'gearDown':
                op_symbol = '-'
            else:
                 raise Exception(f"Unexpected expression operator: {op_token}")

            bin_op = BinOp(op_symbol, [ast_node, right_node])
            ast_node = bin_op
        return ast_node

    def run(source, output_filename):
        initial_hp = 120.0
        try:
            hp_input = input("Enter initial horsepower (default 120): ")
            if hp_input.strip():
                initial_hp = float(hp_input)
                if initial_hp <= 0:
                    print("Warning: Horsepower must be positive. Using default 120.")
                    initial_hp = 120.0
            else:
                print("Using default horsepower 120.")
                initial_hp = 120.0
        except ValueError:
            print("Invalid horsepower input. Using default 120.")
            initial_hp = 120.0
        except EOFError:
            print("No input received for horsepower. Using default 120.")
            initial_hp = 120.0

        filtered_source = PrePro.filter(source)
        Parser.tokenizer = Tokenizer(filtered_source)
        st = SymbolTable({})
        cs = CarState(initial_horsepower=initial_hp)

        if Parser.tokenizer.next.tipoToken != 'greenLight':
            raise Exception('Syntax Error: Program must start with "greenLight"')

        ast_root = Parser.parseBlock()

        # ✅ Validação do AST para etapa atual (ids e Generate)
        def walk_ast(node):
            assert hasattr(node, "id"), f"Nó {type(node).__name__} não tem id"
            assert hasattr(node, "Generate"), f"Nó {type(node).__name__} não tem Generate"
            for child in node.children:
                walk_ast(child)

        walk_ast(ast_root)
        print("✅ AST construída com sucesso com IDs e métodos Generate disponíveis.")

        if Parser.tokenizer.next.tipoToken != 'EOF':
            raise Exception(f"Syntax Error: Unconsumed tokens remaining starting with {Parser.tokenizer.next}")

        # Execução do interpretador (modo Evaluate)
        ast_root.Evaluate(st, cs)

        if cs.ligado:
            raise Exception("RuntimeError: Program finished with engine still 'carOn'.")

        # Geração de código Assembly
        Code.header()
        ast_root.Generate(st)
        Code.footer()
        Code.dump(output_filename)

        return None
