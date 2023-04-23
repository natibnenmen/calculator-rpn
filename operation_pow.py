import operations

@operations.register('^', 2)
def power(num1, num2):
    return num2 ** num1