class SymbolTable():
    def __init__(self, symbols):
        self.symbols = symbols
        
        self.type_map = {
            "horsepower": "i32",
            "status": "bool",
            "plate": "str"
        }


    def getter(self, key):
        if key in self.symbols:
            return self.symbols[key]
        
        raise Exception(f"KeyError: Variable '{key}' accessed before assignment or declaration.")

    def setter(self, key, value):
        if key not in self.symbols:
            raise Exception(f"Variable '{key}' not declared before assignment.")

        stored_type = self.symbols[key][1]
        assigned_type = value[1]

        if stored_type != assigned_type:
            
            expected_type = stored_type
            found_type = assigned_type
            raise Exception(f"TypeError: Cannot assign type '{found_type}' to variable '{key}' of type '{expected_type}'.")

        self.symbols[key] = value

    def create_variable(self, name, value, declared_type_igniscript):
        if name in self.symbols:
            raise Exception(f"Variable '{name}' already declared.")

        if declared_type_igniscript not in self.type_map:
            raise Exception(f"Internal Error: Unknown declared type '{declared_type_igniscript}' received by SymbolTable.")
        internal_type = self.type_map[declared_type_igniscript]

        if value is None:
            
            if internal_type == "i32":
                default_value = 0
            elif internal_type == "bool":
                default_value = False 
            elif internal_type == "str":
                default_value = ""
            else:
                
                 raise Exception(f"Internal Error: Cannot assign default value for internal type '{internal_type}'.")
            self.symbols[name] = (default_value, internal_type)
        else:
            
            assigned_value, assigned_type = value
            if assigned_type != internal_type:
                raise Exception(f"TypeError: Cannot initialize variable '{name}' declared as '{declared_type_igniscript}' (expects internal type '{internal_type}') with value of type '{assigned_type}'.")
            self.symbols[name] = (assigned_value, internal_type)