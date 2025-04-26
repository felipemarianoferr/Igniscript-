class Token:
    def __init__(self, tipoToken, valorToken):
        self.tipoToken = tipoToken
        self.valorToken = valorToken

    def __str__(self):
        return f"Token({self.tipoToken}, {repr(self.valorToken)})"

class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
        self.num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        self.keywords = {
            # Commands / Statements
            "flash": "flash",
            "sensor": "sensor",
            "info": "info",
            "neutral": "neutral",
            "tune": "tune",
            "pitStop": "pitStop",
            "greenLight": "greenLight",
            "redLight": "redLight",
            "checkIgnition": "checkIgnition",
            "backup": "backup",
            "duringEngineRev": "duringEngineRev",
            # Types
            "horsepower": "horsepower",
            "status": "status",
            "plate": "plate",
            # Boolean Literals
            "carOn": "carOn",
            "carOff": "carOff",
            # Operators (Unary 'turbo'/'brake' removed)
            "gearUp": "gearUp", # Handles both unary and binary +
            "gearDown": "gearDown", # Handles both unary and binary -
            "accelerate": "accelerate", # *
            "clutch": "clutch", # /
            "turboBoost": "turboBoost", # ++
            "ignite": "ignite", # ||
            "traction": "traction", # &&
            "sameAs": "sameAs", # ==
            "overdrive": "overdrive", # >
            "underride": "underride", # <
            "reverse": "reverse", # !
            # Removed 'turbo' and 'brake'
        }
        self.selectNext()

    def selectNext(self):

        while self.position < len(self.source) and self.source[self.position] in (' ', '\n', '\r', '\ufeff', '\t'):
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token('EOF','')
            return

        current_char = self.source[self.position]

        if current_char in self.num:
            val = current_char
            self.position += 1
            while self.position < len(self.source) and self.source[self.position] in self.num:
                val += self.source[self.position]
                self.position += 1
            if self.position < len(self.source) and self.source[self.position].isalpha():
                 raise Exception(f"Syntax error: Invalid number format near '{val}{self.source[self.position]}'")
            self.next = Token('horsepower_literal', int(val))
            return

        if current_char == '"':
            self.position += 1
            val = ''
            while self.position < len(self.source) and self.source[self.position] != '"':
                val += self.source[self.position]
                self.position += 1
            if self.position >= len(self.source):
                raise Exception("Unterminated string literal")
            self.position += 1
            self.next = Token('plate_literal', val)
            return

        if current_char == '(':
            self.next = Token('OPEN', '(')
            self.position += 1
            return
        if current_char == ')':
            self.next = Token('CLOSE', ')')
            self.position += 1
            return

        if current_char.isalpha():
            val = current_char
            self.position += 1
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
                val += self.source[self.position]
                self.position += 1

            if val in self.keywords:
                token_type = self.keywords[val]
                if token_type == 'carOn':
                    self.next = Token('status_literal', True)
                elif token_type == 'carOff':
                    self.next = Token('status_literal', False)
                elif token_type == 'horsepower':
                     self.next = Token('TYPE_HORSEPOWER', val)
                elif token_type == 'status':
                     self.next = Token('TYPE_STATUS', val)
                elif token_type == 'plate':
                     self.next = Token('TYPE_PLATE', val)
                elif token_type == 'sensor':
                     self.next = Token('sensor', val)
                else:
                    self.next = Token(token_type, val)
            else:
                self.next = Token('identifier', val)
            return

        raise Exception(f"Unrecognised character: '{current_char}' at position {self.position}")