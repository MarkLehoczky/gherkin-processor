from functools import wraps


def before(*before_functions):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for before_function in before_functions:
                before_function()
            return func(*args, **kwargs)
        return wrapper
    return decorator

def after(*after_functions):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            for after_function in after_functions:
                after_function()
            return result
        return wrapper
    return decorator
