from collections import namedtuple
import importlib
import os
import sys
import traceback


#res_type = namedtuple('res_type', 'function')
res_type_map = {}


def register(res_type):
    
    def register_function(func):
        if res_type in res_type_map:
            raise ValueError(f'Error: The res_type {res_type} is already registered!')
        res_type_map[res_type] =  func
        return func

    return register_function

    
def load_modules():

    try:
        for file in os.listdir(os.path.dirname(__file__)):
            if file.endswith('.py') and not file.startswith('_'):
                if file.startswith('response_type'):
                    module_name = file[:file.find('.py')]
                    print(f'module_name: {module_name}')
                    if module_name not in sys.modules:
                        globals()[module_name] = importlib.import_module(module_name)
                        print(f'Imported {module_name}')
    except Exception as e:
        print(f'traceback.format_exc(): \n {traceback.format_exc()}')
        print(f'Exception: {e}')

load_modules()

