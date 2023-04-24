import os
import importlib
import traceback
import sys


def load_modules(module_name_prefix):

    try:
        for file in os.listdir(os.path.dirname(__file__)):
            if file.endswith('.py') and not file.startswith('_'):
                if file.startswith(module_name_prefix):
                    module_name = file[:file.find('.py')]
                    if module_name not in sys.modules:
                        globals()[module_name] = importlib.import_module(module_name)
                        print(f'Imported {module_name}')
    except Exception as e:
        print(f'traceback.format_exc(): \n {traceback.format_exc()}')
        print(f'Exception: {e}')