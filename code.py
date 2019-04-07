#!python

# MAL: Make a Lisp
# by Gus

import sys
import reader
import printer
import mytypes
import env
import core

ENV = env.Env(None)
for symbol, function in core.ns.items():
    ENV.set_(mytypes.MalSymbol(symbol), function)

def eval_ast(ast:mytypes.MalType, env):
    print(env)
    if isinstance(ast, mytypes.MalSymbol):
        # try:
        print(str(type(env)) + "Type")
        print(str(env) + "value")
        return env.get(ast)
        # except:
            # print("Symbol look up error: {}".format(ast.content))
    elif ast.my_type in ["list", "vector"]:
        ret = []
        print(ast.content)
        for item in ast.content:
            ret.append(EVAL(item, env))
        return ret
    else:
        return ast

def READ(input):
    print("akjbe")

    '''Breaks the user's input into tokens'''
    return reader.read_str(input)

def EVAL(ast, _env:env.Env):
    '''Evaluates its input (tokens, probably)'''
    print("Ca")

    while True:
        # print("LLLLLLLLLLLLLLLLLLLLLLLLLLL :::: !!!!!!! ;;;; :" + str(ast.content[1].content))

        print(ast.my_type, _env)
        
        print("THE ASSYMETRICAL SYNTAX TABLE::::: !!!! " + str(ast.content))
        if ast.my_type not in ["list", "vector"]:
            print("non list, breaking out")
            return eval_ast(ast, _env)

        try:
            a0 = ast.content[0]
        except IndexError:
            return mytypes.MalList([])
        try:
            a1 = ast.content[1]
        except IndexError:
            a1 = mytypes.MalNil()
        try:
            a2 = ast.content[2]
        except IndexError:
            a2 = mytypes.MalNil()
        print("LARGE EGG " + str(a0))

        if "def!" == a0.content:
            print("^^^^^^^" + str(a1) + str(a2))
            res = EVAL(a2, _env)
            return _env.set_(a1, res)
        elif "let*" == a0.content:
            new_env = env.Env(ENV)
            a1, a2 = ast.content[1], ast.content[2]
            for i in range(0, len(a1.content), 2):
                new_env.set_(a1.content[i], EVAL(a1.content[i+1], new_env))
            env = new_env
            ast = a2
            continue
        elif "do" == a0.content:
            a1 = ast.content[1]
            l = len(a1)
            i = 0
            for item in a1.content:
                if i != l:
                    last = eval_ast(item, _env)
                else:
                    ast = item
                    continue
                i += 1
            return last
        elif "if" == a0.content:
            try:
                a3 = ast.content[3]
            except IndexError:
                a3 = None

            if EVAL(a1, _env).content:
                print("IT WAS TRUUEE!!!!")
                return EVAL(a2, _env)
            else:
                print("FALSEEE! NOT TRUEEE!!")
                if a3 != None:
                    return EVAL(a3, _env)
                else:
                    return mytypes.MalNil()
        elif "fn*" == a0.content:
            print("murder " + str(type(a1)))
            return mytypes.MalFuntion(EVAL, env.Env, a2, _env, a1)
        else:
            if not ast.content:
                return ast
            else:
                evaled = eval_ast(ast, _env)
                print(evaled)
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

        result = PRINT(EVAL(READ(inp), ENV))
        print(result)

if __name__ == "__main__":
    repl()
