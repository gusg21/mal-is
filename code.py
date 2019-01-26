# MAL: Make a Lisp
# by Gus

import sys

def READ(input):
    '''Breaks the user's input into tokens'''
    return input

def EVAL(input):
    '''Evaluates its input (tokens, probably)'''
    return input

def PRINT(input):
    '''Processes its input for print to the console'''

    return input

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