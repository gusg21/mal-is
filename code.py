# MAL: Make a Lisp
# by Gus

import sys
import reader
import printer
import mytypes

ENV = {
    "symbols" : {
        "+" : lambda a,b: a+b,
        "-" : lambda a,b: a-b,
        "*" : lambda a,b: a*b,
        "/" : lambda a,b: int(a/b),
        "^" : lambda a,b: a**b,
    },
    "keywords" : {
        
    }
}

def eval_ast(ast:mytypes.MalType, env:dict):
    if ast.my_type == "symbol":
        try:
            return env["symbols"][ast.content]
        except:
            print("Symbol look up error: {}".format(ast.content))
    elif ast.my_type in ["list", "vector"]:
        ret = []
        for item in ast.content:
            ret.append(EVAL(item))
        return ret
    else:
        return ast

def READ(input):
    '''Breaks the user's input into tokens'''
    return reader.read_str(input)

def EVAL(ast):
    '''Evaluates its input (tokens, probably)'''
    if ast.my_type not in ["list", "vector"]:
        return eval_ast(ast, ENV)
    else:
        if not ast.content:
            return ast
        else:
            evaled = eval_ast(ast, ENV)
            return evaled[0](*evaled[1:])

def PRINT(input):
    '''Processes its input for print to the console'''
    return printer.print_str(input)

def repl():
    '''READ-EVAL-PRINT Loop.'''

    print("IS lang REPL\npython version " + str(sys.version_info) + "\n")

    done = False
    while not done:
        try:
            inp = input("is]] ")
        except (KeyboardInterrupt, EOFError): # Break on Ctrl-D or Ctrl-C
            done = True
            break

        if not inp: # Break on empty
            done = True
            break

        result = PRINT(EVAL(READ(inp)))
        print(result)

if __name__ == "__main__":
    repl()