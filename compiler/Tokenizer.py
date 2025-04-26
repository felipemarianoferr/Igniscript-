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
            "flash": "flash", # print
            "sensor": "sensor", # read
            "info": "info",
            "neutral": "neutral", # ; (empty command)
            "tune": "tune", # =
            "pitStop": "pitStop", # ;
            "greenLight": "greenLight", # {
            "redLight": "redLight", # }
            "checkIgnition": "checkIgnition", # if
            "backup": "backup", # else
            "duringEngineRev": "duringEngineRev", # while
            # Types
            "horsepower": "horsepower", # i32 (Used for type declaration)
            "status": "status", # bool (Used for type declaration)
            "plate": "plate", # str (Used for type declaration)
            # Boolean Literals
            "carOn": "carOn", # true
            "carOff": "carOff", # false
            # Operators handled in identifier check
            "gearUp": "gearUp", # +
            "gearDown": "gearDown", # -
            "accelerate": "accelerate", # *
            "clutch": "clutch", # /
            "turboBoost": "turboBoost", # ++ (string concat)
            "ignite": "ignite", # ||
            "traction": "traction", # &&
            "sameAs": "sameAs", # ==
            "overdrive": "overdrive", # >
            "underride": "underride", # <
            "reverse": "reverse", # ! (unary logical not)
            "turbo": "turbo",
            "brake": "brake",
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
            # Allow letters, digits, underscore in identifiers
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
                val += self.source[self.position]
                self.position += 1

            # Check if it's a keyword/type/literal
            if val in self.keywords:
                token_type = self.keywords[val]
                # Special handling for boolean literals to store actual boolean value
                if token_type == 'carOn':
                    self.next = Token('status_literal', True) # Treat carOn as bool True
                elif token_type == 'carOff':
                    self.next = Token('status_literal', False) # Treat carOff as bool False
                # Use specific token types for language types when used as keywords
                elif token_type == 'horsepower':
                     self.next = Token('TYPE_HORSEPOWER', val)
                elif token_type == 'status':
                     self.next = Token('TYPE_STATUS', val)
                elif token_type == 'plate':
                     self.next = Token('TYPE_PLATE', val)
                # Handle sensor keyword - parser will check for ()
                elif token_type == 'sensor':
                     self.next = Token('sensor', val)
                else:
                    # General keyword
                    self.next = Token(token_type, val)
            else:
                self.next = Token('identifier', val) # Regular identifier
            return

        raise Exception(f"Unrecognised character: '{current_char}' at position {self.position}")