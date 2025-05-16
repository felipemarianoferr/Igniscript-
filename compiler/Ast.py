
from compiler.Code import Code

class Node():
    current_id = 0

    @staticmethod
    def newId():
        Node.current_id += 1
        return Node.current_id

    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newId()

    def Evaluate(self, st, cs):
        pass

    def Generate(self, st):
        raise NotImplementedError(f"Generate() not implemented for {type(self).__name__}")

class Info(Node):
    def Evaluate(self, st, cs):
        print(cs.get_state_info())

    def Generate(self, st):
        pass

class BinOp(Node):
    def Evaluate(self, st, cs):
        pass

    def Generate(self, st):
        pass

class UnOp(Node):
    def Evaluate(self, st, cs):
        pass

    def Generate(self, st):
        pass

class While(Node):
    def Evaluate(self, st, cs):
        pass

    def Generate(self, st):
        pass

class If(Node):
    def Evaluate(self, st, cs):
        pass

    def Generate(self, st):
        pass

class Read(Node):
    def Evaluate(self, st, cs):
        pass

    def Generate(self, st):
        pass

class Block(Node):
    def Evaluate(self, st, cs):
        pass

    def Generate(self, st):
        for child in self.children:
            child.Generate(st)

class Assignment(Node):
    def Evaluate(self, st, cs):
        pass

    def Generate(self, st):
        pass

class Identifier(Node):
    def Evaluate(self, st, cs):
        pass

    def Generate(self, st):
        pass

class Print(Node):
    def Evaluate(self, st, cs):
        pass

    def Generate(self, st):
        pass

class IntVal(Node):
    def Evaluate(self, st, cs):
        return (self.value, 'i32')

    def Generate(self, st):
        pass

class BoolVal(Node):
    def Evaluate(self, st, cs):
        return (self.value, 'bool')

    def Generate(self, st):
        pass

class StrVal(Node):
    def Evaluate(self, st, cs):
        return (self.value, 'str')

    def Generate(self, st):
        pass

class VarDec(Node):
    def Evaluate(self, st, cs):
        pass

    def Generate(self, st):
        pass

class NoOp(Node):
    def Evaluate(self, st, cs):
        pass

    def Generate(self, st):
        pass