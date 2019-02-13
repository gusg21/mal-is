import regex
import mytypes
import sys

class Reader():
    def __init__(self, tokens, position=0):
        self.tokens = tokens
        self.position = position

    def next(self):
        self.position += 1
        return self.tokens[self.position-1]

    def peek(self):
        if len(self.tokens) > self.position:
            return self.tokens[self.position]
        else:
            return None

def tokenize(string):
    raw_tokens = regex.split(
        r"[\s,]*(~@|[\[\]{}()'`~^@]|\"(?:\\.|[^\\\"])*\"?|;.*|[^\s\[\]{}('\"`,;)]*)", string
        )
        
    for token in raw_tokens:
        if token == "":
            raw_tokens.remove(token)
            
    return raw_tokens

def read_str(string):
    return read_form(Reader(tokenize(string)))

def read_str_(token:str):
    internal = token[1:len(token) - 1]

    internal.replace("\\\n", "\n")
    internal.replace("\\\\", "\\")
    internal.replace("\\\"", "\"")
    
    return internal

def read_list(reader:Reader, start="(", end=")", isvec=False) -> list:
    ast = []

    token = reader.next()

    if token != start:
        print("malformed list")
        sys.exit(1)

    while token != end:
        ast.append(read_form(reader))
        token = reader.peek()

    if isvec:
        return mytypes.MalVector(ast)
    else:
        return mytypes.MalList(ast)

def read_atom(reader:Reader):
    token = reader.next()

    if token.isnumeric():
        return mytypes.MalNumber(float(token))
    elif token[0] == "\"":
        return mytypes.MalString(read_str_(token))
    elif token[0] == ":":
        return mytypes.MalKeyword(token[1:])
    elif token in mytypes.SYMBOLS.keys():
        return mytypes.MalSymbol(token)

def read_form(reader:Reader):
    token = reader.peek()

    if token == None:
        return

    if token == "(":
        return read_list(reader)
    if token == "[": # read vector
        return read_list(reader, "[", "]", True)
    else:
        return read_atom(reader)