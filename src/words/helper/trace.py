from collections.abc import Callable
import inspect


def trace(args: list[str]):
    """
    Print function name and optionally the provided args.
    Only works on functions that take no kwargs.
    """

    def inner(func: Callable):
        def inner_wrap(*func_args, **kwargs):
            params = inspect.signature(func).parameters
            param_keys = list(params.keys())
            print_args = ", ".join([f"{arg}={func_args[param_keys.index(arg)]}" for arg in args])
            print(f"{func.__name__}({print_args})")
            return func(*func_args, **kwargs)

        return inner_wrap

    return inner
