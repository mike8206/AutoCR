import multiprocessing.pool
import functools

def timeOut(max_timeout):
    """Timeout decorator, parameter in seconds."""
    def timeout_decorator(item):
        """Wrap the original function."""
        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            """Closure for function."""
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            try:
               # raises a TimeoutError if execution exceeds max_timeout
                return async_result.get(max_timeout)
            except TimeoutError:
                raise
            finally:
                pool.close()
        return func_wrapper
    return timeout_decorator