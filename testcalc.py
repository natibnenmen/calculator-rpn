from calculator import Calculator
from operations_reg import operators as operations

if __name__ == "__main__":

    calc = Calculator(operations)
    while True:
        inp = input("> ")
        if inp == "exit":
            break

        print(calc.process_expression(inp))