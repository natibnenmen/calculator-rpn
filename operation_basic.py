from operations import register

@register('-', 0)
def subtract(num1, num2):
    return num2 - num1

@register('*', 1)
def multiply(num1, num2):
    return num2 * num1

@register('+', 0)
def add(num1, num2):
    return num2 + num1