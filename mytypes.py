class MalType: # OOP style typing
    my_type:str = "empty" # AAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAA
    
    def __init__(self, content):
        self.content = content

class MalList(MalType): # List type (+ 4 4)
    my_type = "list"

    def __init__(self, items:list):
        self.content = items

EmptyList = MalList([])

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

    def __int__(self):
        return int(self.content)

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

class MalBool(MalType):
    my_type = "bool"

    def __init__(self, content):
        self.content = content

class MalNil(MalType):
    my_type = "nil"

    def __init__(self):
        self.content = None

class MalFuntion(MalType):
    my_type = "function"

    def __init__(self, _eval, BigEEnv, ast, env, params):
        self.eval = _eval
        self.ast = ast
        self.env = env
        self.params = params
        self.bigEEnv = BigEEnv
        self.content = self.fn
    
    def fn(self, args):
        return self.eval(self.ast, self.bigEEnv(self.env, self.params, MalList(args)))
    
    def __call__(self, *args):
        return self.fn(args)
