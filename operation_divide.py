
from operations_reg import register

@register('/', 0)
def divide(num1, num2):
    if num2 == 0:
        raise ZeroDivisionError("Division by zero is not allowed")
    return num2 / num1
