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
        ret = mytypes.MalList([])
        print(ast.content)
        for item in ast.content:
            ret.content.append(EVAL(item, env))
        return ret
    else:
        return ast

def READ(input):
    print("akjbe")

    '''Breaks the user's input into tokens'''
    return reader.read_str(input)

def is_pair(ast):
    if ast.my_type not in ["list", "vector"]:
        return False

    return len(ast.content) > 0

def is_macro_call(ast, env):
    if ast.my_type == "list":
        if ast.content[0].my_type == "symbol":
            symbol = env.get(ast.content[0])
            if symbol.my_type == "function":
                if symbol.is_macro:
                    return True

    return False

def macroexpand(ast, env):
    while is_macro_call(ast, env):
        ast = env.get(ast.content[0])(*ast.content[1:])
    
    return ast

def quasiquote(a):
    print("QUASIQUOTING: {}".format(printer.print_str(a)))

    if not is_pair(a):
        return mytypes.MalList([mytypes.MalSymbol("quote"), a])
    elif a.content[0].content == "unquote":
        print("Found unquote")
        return a.content[1]
    elif is_pair(a.content[0]) and a.content[0].content[0].content == "splice-unquote":
        return mytypes.MalList([mytypes.MalSymbol("concat"), a.content[0].content[1], quasiquote(mytypes.MalList(a.content[1:]))])
    else:
        return mytypes.MalList([mytypes.MalSymbol("cons"), quasiquote(a.content[0]), quasiquote(mytypes.MalList(a.content[1:]))])

def EVAL(ast, _env:env.Env):
    '''Evaluates its input (tokens, probably)'''
    print("Ca")

    # print("LLLLLLLLLLLLLLLLLLLLLLLLLLL :::: !!!!!!! ;;;; :" + str(ast.content[1].content))

    print(ast.my_type, _env)
    print(str(ast.content) + " MEMES")
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

    if callable(a0):
        return a0(*ast.content[1:])

    ast = macroexpand(ast, _env)
    
    if a0.my_type == "symbol":
        if "def!" == a0.content:
            print("^^^^^^^" + str(a1) + str(a2))
            res = EVAL(a2, _env)
            return _env.set_(a1, res)
        elif "defmacro!" == a0.content:
            print("^^^^^^^" + str(a1) + str(a2))
            res = EVAL(a2, _env)
            res.is_macro = True
            return _env.set_(a1, res)
        elif "let*" == a0.content:
            new_env = env.Env(ENV)
            a1, a2 = ast.content[1], ast.content[2]
            for i in range(0, len(a1.content), 2):
                new_env.set_(a1.content[i], EVAL(a1.content[i+1], new_env))
            return EVAL(a2, new_env)
        elif "do" == a0.content:
            a1 = ast.content[1]
            for item in a1.content:
                last = eval_ast(item, _env)
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
            return mytypes.MalFuntion(EVAL, env.Env, a2, _env, a1)
        elif "quote" == a0.content:
            return a1
        elif "quasiquote" == a0.content:
            return EVAL(quasiquote(ast.content[1]), _env)
        elif "macroexpand" == a0.content:
            return macroexpand(a1, _env)
        else:
            if not ast.content:
                return ast
            else:
                evaled = eval_ast(ast, _env)
                print("Evaluated Object " + str(evaled))
                print("Evaluated Content " + str(evaled.content))
                return evaled.content[0](*evaled.content[1:])
def PRINT(input):
    '''Processes its input for print to the console'''
    return printer.print_str(input)

def rep(s):
    return PRINT(EVAL(READ(s), ENV))

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

        result = rep(inp)
        print(result)

def fn_slurp(a):
    f = open(a.content)
    data = f.read()
    f.close()
    print(data + " \"slurped\"")
    return mytypes.MalString(data)

def fn_load_file(a):
    print("Loaded data: " + fn_slurp(a).content)
    data = mytypes.MalString("{}".format(fn_slurp(a).content))
    print(data.content)
    return EVAL(reader.read_str(data.content), ENV)

def fn_eval(a):
    print("Core function \"EVAL\" ran with arg " + str(a.content))
    return EVAL(a, ENV)

ENV.set_(mytypes.MalSymbol("eval"), fn_eval)
ENV.set_(mytypes.MalSymbol("slurp"), fn_slurp)
# ENV.set_(mytypes.MalSymbol("load-file"), fn_load_file)

rep("(def! load-file (fn* (f) (eval (read-string (str (slurp f))))))")

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        rep("(load-file \"{}\")".format(sys.argv[1]))

    repl()
