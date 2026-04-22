import time
from functools import wraps


def time_it(func):
    """Decorator to measure how long a function takes to run."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"⏱️ {func.__name__} took {end - start:.4f} seconds")
        return result

    return wrapper


# Usage: @time_it before any function definition
