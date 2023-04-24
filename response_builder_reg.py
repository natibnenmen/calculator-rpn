from collections import namedtuple
import importlib
import os
import sys
import traceback
import utils

'''
This module is responsible for building the response to the client. The input is the response type which is received from the client and the result.
It is build in a way that it is easy to add new response types. The response types are dynamically loaded using the register function as a decorator registry.
The load_modules function is used to load all the modules that start with 'response_type_', in which the specific response types are implemented.
This way, when new response types are added, they are automatically loaded and registered.
In both cases when no response type is specified, or the response type from the client is not found in the registry,  the default response type is used.
'''

res_type_map = {}

# This is the interface function to the client(the server.py module in this case)
def build_response(response_type, result):
    return res_type_map.get(response_type, res_type_map.get('default'))(result)


def register(res_type):
    
    def register_function(func):
        if res_type in res_type_map:
            raise ValueError(f'Error: The res_type {res_type} is already registered!')
        res_type_map[res_type] =  func
        return func

    return register_function

    
utils.load_modules('response_type_')

