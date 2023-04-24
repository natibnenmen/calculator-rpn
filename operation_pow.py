import operations_reg

@operations_reg.register('^', 2)
def power(num1, num2):
    return num2 ** num1