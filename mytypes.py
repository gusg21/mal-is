class MalType: # OOP style typing
    my_type:str = "empty" # AAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAA
    
    def __init__(self, content):
        self.content = content

class MalList(MalType): # List type (+ 4 4)
    my_type = "list"

    def __init__(self, items:list):
        self.content = items

class MalNumber(MalType): # Number type
    my_type = "number"

    def __init__(self, number:float):
        self.content = number
    
    def __add__(self, other):
        return MalNumber(self.content + other.content)
    
    def __sub__(self, other):
        return MalNumber(self.content - other.content)
    
    def __mul__(self, other):
        return MalNumber(self.content * other.content)
    
    def __div__(self, other):
        return MalNumber(self.content / other.content)
    
    def __pow__(self, other):
        return MalNumber(self.content ** other.content)

class MalSymbol(MalType): # Operational symbol (+ - * / etc.)
    my_type = "symbol"

    def __init__(self, symbol:str):
        self.content = symbol

class MalString(MalType):
    my_type = "string"

    def __init__(self, string:str):
        self.content = string

class MalKeyword(MalType):
    my_type = "keyword"

    def __init__(self, name):
        self.content = name

class MalVector(MalType):
    my_type = "vector"

    def __init__(self, content):
        self.content = content

SYMBOLS = {
    "+" : "plus", 
    "=" : "equal", 
    "-" : "minus", 
    "*" : "multiply", 
    "/" : "divide", 
    ">" : "greater than", 
    "<" : "less than",
    "^" : "power"
} # symbols that qualify as MalSymbol
