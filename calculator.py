import re
from math import *
from operations_reg import operators as operations
import traceback

class Calculator:

    #staticmethod
    def __init__(self, operations):
        self._rgx = Calculator._operations_to_rgx(operations) 

    #staticmethod
    def _is_float(string):
        return string.replace(".", "", 1).isdigit()

    #staticmethod
    def _operations_to_rgx(operations):
        float_regex = "\d*\.?\d+|[\(\)]"
        for key in operations.keys():
            float_regex += "|" + "[\\" + key + "]"
        return re.compile(float_regex)


    def _tokenize(self, string):
        string = string.replace(" ", "")

        results = self._rgx.finditer(string)
        self._expr_list = []
        for reg in results:
            start, end = reg.span()
            self._expr_list.append(string[start: end])


    def _to_rpn(self):
        self._rpn_tokens = []
        op_stack = []

        for token in self._expr_list:
            # Add number to rpn tokens
            if (Calculator._is_float(token)):
                self._rpn_tokens.append(token)
            # Add opening bracket to operation stack
            elif token == "(":
                op_stack.append(token)
            # Consumes all operations until matching opening bracket
            elif token == ")":
                while op_stack[-1] != "(":
                    self._rpn_tokens.append(op_stack.pop())
                op_stack.pop()
            elif token in list(operations.keys()):
                try:
                    # Check if we have operations that have higher priority on
                    # the op_stack and add them to self._rpn_tokens so that they are evaluated first:
                    token_priority = operations[token].priority
                    while op_stack[-1] != "(" and operations[op_stack[-1]].priority >= token_priority:
                        self._rpn_tokens.append(op_stack.pop())
                except IndexError:  # op_stack is empty
                    pass
                # Add the current operation to the op_stack:
                op_stack.append(token)

        # Add remaining operations to rpn tokens
        while len(op_stack) != 0:
            self._rpn_tokens.append(op_stack.pop())


    def _calculate(self):
        val_stack = []

        for token in self._rpn_tokens:
            if (Calculator._is_float(token)):
                val_stack.append(token)
            elif token in list(operations.keys()):
                args = []
                for x in range(operations[token].operation.__code__.co_argcount):
                    # If this throws an error user didn't give enough args
                    args.append(float(val_stack.pop()))
                result = operations[token].operation(*args)
                val_stack.append(result)

        # If the value stack is bigger than one we probably made an error with the input
        assert len(val_stack) == 1
        self._result =  val_stack[0]


    def process_expression(self, expression):
        print(f"EXPRESSION: {expression}")
        self._tokenize(expression)
        print(f"TOKENS: {self._expr_list}")
        self._to_rpn()
        print(f"RPN: {self._rpn_tokens}")
        self._calculate()
        print(f"RESULT: {self._result}")
        return self._result


