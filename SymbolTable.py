class SymbolTable:

    def __init__(self):
        self.scopes = [{}]

    def enter_scoppe(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()

    def declare(self, name, var_type):
        self.scopes[-1][name] = var_type

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
            
        return None
    
