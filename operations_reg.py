from collections import namedtuple
import importlib
import os
import sys
import traceback
from utils import load_modules

'''
This module holds the operators in the 'operators' dictionary.
Each operator is a dynamically loaded using the register function as a decorator registry.
The load_modules function is used to load all the modules that start with 'operation_', in which the specific operators are implemented.
Adding a new operator is as simple as adding a new module that starts with 'operation_' and implementing the operator as a function, including the operator, 
the precedence and the operation function.
'''

operator = namedtuple('operator', 'priority operation')
operators = {}


def register(op_key, precedence):
    
    def register_function(func):
        if op_key in operators:
            raise ValueError(f'Error: The operator {op_key} is already registered!')
        operators[op_key] =  operator(precedence, func)
        return func

    return register_function


load_modules("operation_")

