import time
from typing import Callable

# returns result and execution time of the passed function as an array
elapseTimeWithResult: Callable[
    [type(lambda x: None), ...], float
] = lambda f, *args: (
    lambda s=time.process_time(): [f(*args), time.process_time() - s]
)()

# returns execution time of the passed function
elapseTime: Callable[
    [type(lambda x: None), ...], float
] = lambda f, *args: elapseTimeWithResult(f, *args)[1]
