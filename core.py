import mytypes
import printer
import reader

def fn_print(a):
    print("OUTPUT: " + printer.print_str(a))

    return mytypes.MalNil()

def fn_list(*a):
    return mytypes.MalList(a)

def fn_list_q(a):
    return mytypes.MalBool(a.my_type == "list")

def fn_empty_q(a):
    return mytypes.MalBool(len(a.content) == 0)

def fn_count(a):
    return mytypes.MalNumber(len(a.content))

def fn_str(*a):
    string = ""
    for item in a:
        string += str(item.content)
    return mytypes.MalString(string)

def fn_equal(a, b):
    return mytypes.MalBool((a.content == b.content) and (a.my_type == b.my_type))

def fn_gt(a, b):
    return mytypes.MalBool(a.content > b.content)

def fn_gte(a, b):
    return mytypes.MalBool(a.content >= b.content)

def fn_lt(a, b):
    return mytypes.MalBool(a.content < b.content)

def fn_lte(a, b):
    return mytypes.MalBool(a.content <= b.content)

def fn_read_string(a):
    return reader.read_str(a.content)

ns = {
    "+": lambda a,b: mytypes.MalNumber(int(a.content)+int(b.content)),
    "-": lambda a,b: mytypes.MalNumber(int(a.content)-int(b.content)),
    "*": lambda a,b: mytypes.MalNumber(int(a.content)*int(b.content)),
    "/": lambda a,b: mytypes.MalNumber(int(a.content)/int(b.content)),

    "=": fn_equal,
    ">": fn_gt,
    ">=": fn_gte,
    "<": fn_lt,
    "<=": fn_lte,

    "prn": fn_print,
    "list": fn_list,
    "list?": fn_list_q,
    "empty?": fn_empty_q,
    "count": fn_count,
    "str": fn_str,

    "read-string": fn_read_string,
}