import re
from math import *
from collections import namedtuple

OpBehaviour = namedtuple('OpBehaviour', 'priority lmbd')

operations = {
    "+": OpBehaviour(0, lambda x, y: y+x),
    "-": OpBehaviour(0, lambda x, y: y-x),
    "/": OpBehaviour(1, lambda x, y: y/x),
    "*": OpBehaviour(1, lambda x, y: y*x),
    "!": OpBehaviour(2, lambda x: gamma(1+x)),
    "%": OpBehaviour(2, lambda x: x/100),
    "^": OpBehaviour(2, lambda x, y: y**x),
    "sin": OpBehaviour(99, lambda x: sin(x)),
    "cos": OpBehaviour(99, lambda x: cos(x)),
    "tan": OpBehaviour(99, lambda x: tan(x)),
    "asin": OpBehaviour(99, lambda x: asin(x)),
    "acos": OpBehaviour(99, lambda x: acos(x)),
    "atan": OpBehaviour(99, lambda x: atan2(x)),
    "ln": OpBehaviour(99, lambda x: log(x)),
    "log": OpBehaviour(99, lambda x: log10(x)),
    "sqrt": OpBehaviour(99, lambda x: sqrt(x)),
    "fact": OpBehaviour(99, lambda x: factorial(x)),
    "gamma": OpBehaviour(99, lambda x: gamma(x)),
}


def is_float(string: str):
    return string.replace(".", "", 1).isdigit()


def tokenize(string):
    string = string.replace(" ", "")

    # What the fuck?
    float_regex = "\d*\.?\d+|[\(\)]"
    for key in operations.keys():
        if len(key) == 1:
            float_regex += "|" + "[\\" + key + "]"
        else:
            float_regex += "|" + key
        # "|".join(operations)
        # pass
    rgx = re.compile(float_regex)

    results = rgx.finditer(string)
    exprList = []
    for reg in results:
        start, end = reg.span()
        exprList.append(string[start: end])
    return exprList


def to_rpn(tokens):
    rpn_tokens = []
    op_stack = []

    for token in tokens:
        # Add number to rpn tokens
        if (is_float(token)):
            rpn_tokens.append(token)
        # Add opening bracket to operation stack
        elif token == "(":
            op_stack.append(token)
        # Consumes all operations until matching opening bracket
        elif token == ")":
            while op_stack[-1] != "(":
                rpn_tokens.append(op_stack.pop())
            op_stack.pop()
        elif token in list(operations.keys()):
            try:
                # Check if we have operations that have higher priority on
                # the op_stack and add them to rpn_tokens so that they are evaluated first:
                token_priority = operations[token].priority
                while op_stack[-1] != "(" and operations[op_stack[-1]].priority >= token_priority:
                    rpn_tokens.append(op_stack.pop())
            except IndexError:  # op_stack is empty
                pass
            # Add the current operation to the op_stack:
            op_stack.append(token)

    # Add remaining operations to rpn tokens
    while len(op_stack) != 0:
        rpn_tokens.append(op_stack.pop())

    return rpn_tokens


def calculate(rpn_tokens):
    val_stack = []

    for token in rpn_tokens:
        if (is_float(token)):
            val_stack.append(token)
        elif token in list(operations.keys()):
            args = []
            for x in range(operations[token].lmbd.__code__.co_argcount):
                # If this throws an error user didn't give enough args
                args.append(float(val_stack.pop()))
            result = operations[token].lmbd(*args)
            val_stack.append(result)

    # If the value stack is bigger than one we probably made an error with the input
    assert len(val_stack) == 1
    return val_stack[0]


# Some tests

def calculate_string(string):
    tokenized = tokenize(string)
    rpn = to_rpn(tokenized)
    return calculate(rpn)


assert isclose(cos(25), calculate_string("cos(25)"))
assert isclose(1+25/5*3 ** 10, calculate_string("1+25/5*3^10"))

a = gamma(1+sin(1)) + gamma(4+1) - sqrt(4)
b = calculate_string("sin(1)! + 4! - sqrt(4)")
assert isclose(a, b)

# REPL
while True:
    inp = input("> ")
    if inp == "exit":
        break
    tokenized = tokenize(inp)
    print("TOKENS: ", tokenized)
    rpn = to_rpn(tokenized)
    print("RPN: ", rpn)
    result = calculate(rpn)
    print("RESULT: ", result)