import mytypes

def print_str(mal_object:mytypes.MalType) -> str:
    print(mal_object)

    if mal_object is None:
        return ""

    if callable(mal_object):
        return "<builtin (python function)>"

    if mal_object.my_type in ["list", "vector"]:
        if mal_object.my_type == "list":
            parens = ("(", ")")
        else:
            parens = ("[", "]")

        results = []
        for item in mal_object.content:
            results.append(print_str(item))
        return parens[0] + " ".join(results) + parens[1]
    elif mal_object.my_type == "number":
        return str(mal_object.content)
    elif mal_object.my_type == "symbol":
        return "symbol: " + mal_object.content
    elif mal_object.my_type == "string":
        return "str:\"" + mal_object.content + "\""
    elif mal_object.my_type == "keyword":
        return "keyword:" + mal_object.content
    elif mal_object.my_type == "bool":
        return str(mal_object.content)
    elif mal_object.my_type == "nil":
        return "nil"
    elif mal_object.my_type == "function":
        return "<function>"
    else:
        return "Printing error"