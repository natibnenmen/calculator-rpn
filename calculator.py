import re
from math import *
from operations import operators as operations
import traceback


def is_float(string: str):
    return string.replace(".", "", 1).isdigit()


def operations_to_rgx(operations):
    float_regex = "\d*\.?\d+|[\(\)]"
    for key in operations.keys():
        float_regex += "|" + "[\\" + key + "]"
    return re.compile(float_regex)


def tokenize(string, rgx):
    string = string.replace(" ", "")

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

rgx = operations_to_rgx(operations)    

def process_expression(expression):
    tokenized = tokenize(expression, rgx)
    print("TOKENS: ", tokenized)
    rpn = to_rpn(tokenized)
    print("RPN: ", rpn)
    result = calculate(rpn)
    print("RESULT: ", result)
    return result


if __name__ == "__main__":
    
    print(f'operators: {operations}')
    rgx = operations_to_rgx(operations)
    while True:
        inp = input("> ")
        if inp == "exit":
            break
        tokenized = tokenize(inp, rgx)
        print("TOKENS: ", tokenized)
        rpn = to_rpn(tokenized)
        print("RPN: ", rpn)
        result = calculate(rpn)
        print("RESULT: ", result)