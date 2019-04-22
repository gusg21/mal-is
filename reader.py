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
        print("token ----> " + token)
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

def read_list(reader:Reader, start="(", end=")", isvec=False):
    ast = []

    token = reader.next()

    if token != start:
        print("malformed list")
        sys.exit(1)

    while True:
        token = reader.peek()
        if token == end:
            break

        thing = read_form(reader)
        if thing is not None:
            ast.append(thing)

    reader.next()

    if isvec:
        return mytypes.MalVector(ast)
    else:
        return mytypes.MalList(ast)

def read_atom(reader:Reader):
    token = reader.next()

    print(token)

    if token.isnumeric():
        return mytypes.MalNumber(float(token))
    elif token[0] == "\"":
        return mytypes.MalString(read_str_(token))
    elif token[0] == ":":
        return mytypes.MalKeyword(token[1:])
    elif token == "true":
        return mytypes.MalBool(True)
    elif token == "false":
        return mytypes.MalBool(False)
    elif token == "nil":
        return mytypes.MalNil()
    else:
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
