# MAL: Make a Lisp
# by Gus

import sys

def READ(input):
    return input

def EVAL(input):
    return input

def PRINT(input):
    return input

def repl():
    print("IS lang REPL\npython version " + str(sys.version_info) + "\n")

    done = False
    while not done:
        try:
            inp = input("is]] ")
        except (KeyboardInterrupt, EOFError):
            done = True
            break

        if not inp:
            done = True
            break

        result = PRINT(EVAL(READ(inp)))
        print(result)

if __name__ == "__main__":
    repl()