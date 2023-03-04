import time
from functools import wraps


def function_timer(func):
    @wraps(func)
    def function(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Function {func} took {time.time() - start}")
        return result
    return function
