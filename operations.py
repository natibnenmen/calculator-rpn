from collections import namedtuple
import importlib
import os
import sys
import traceback


operator = namedtuple('operator', 'priority lmbd')
operators = {}


def register(op_key, precedence):
    
    def register_function(func):
        if op_key in operators:
            raise ValueError(f'Error: The operator {op_key} is already registered!')
        operators[op_key] =  operator(precedence, func)
        return func

    return register_function

    
def load_modules():

    try:
        for file in os.listdir(os.path.dirname(__file__)):
            if file.endswith('.py') and not file.startswith('_'):
                if file.startswith('operation_'):
                    module_name = file[:file.find('.py')]
                    if module_name not in sys.modules:
                        globals()[module_name] = importlib.import_module(module_name)
                        print(f'Imported {module_name}')
    except Exception as e:
        print(f'traceback.format_exc(): \n {traceback.format_exc()}')
        print(f'Exception: {e}')

load_modules()

