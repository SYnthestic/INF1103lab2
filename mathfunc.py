def add(x, y):
    """Returns the sum of x and y."""
    return x + y

def subtract(x, y):
    """Returns the difference of x and y."""
    return x - y

def multiply(x, y):
    """Returns the product of x and y."""
    return x * y

def divide(x, y):
    """Returns the quotient of x and y. Raises ValueError if y is zero."""
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x / y

def square(x):
    """Returns the square of x."""
    return x * x

def cube(x):
    """Returns the cube of x."""
    return x * x * x

def power(x, n):
    """Returns x raised to the power of n."""
    return x ** n

def apply_function(func, value):
    """Applies a given function to a value."""
    return func(value)