import mytypes
import sys

class Env():
    def __init__(self, outer, binds=mytypes.EmptyList, exprs=mytypes.EmptyList):
        self.outer = outer
        self.data = {}

        i = 0
        for item in binds.content:
            self.set_(item, exprs.content[i])
            i += 1

    def set_(self, symbol:mytypes.MalSymbol, val:mytypes.MalType):
        self.data[symbol] = val
        return self.data[symbol]

    def get_key_content(self):
        contents = []

        for key in self.data.keys():
            contents.append(key.content)
        
        return contents
    
    def find(self, symbol:mytypes.MalSymbol):
        keys = self.get_key_content()

        print("Searching for symbol \"{}\" in {}".format(symbol.content, keys))

        if symbol.content in keys:
            print("Found")
            return self
        else:
            if self.outer is not None:
                return self.outer.find(symbol)
            else:
                print("no variable up to top level")
                sys.exit(1)
    
    def get(self, symbol:mytypes.MalSymbol):
        print(symbol, self.find(symbol))
        env = self.find(symbol)
        for item in env.data.keys():
            if item.content == symbol.content:
                return env.data[item]