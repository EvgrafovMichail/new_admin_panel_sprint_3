from typing import Callable, Any
from functools import wraps
from random import uniform
from time import sleep

from common.log import EventLogger


logger = EventLogger("backoff")


def backoff(
    start_sleep_time: float = 0.1,
    factor: float = 2,
    sleep_time_limit: float = 10
) -> Callable[[Callable], Callable]:
    def backoff_wrapper(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
        degree_curr = 0

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            nonlocal degree_curr

            while True:
                try:
                    result = func(*args, **kwargs)

                except Exception:
                    logger.error(
                        f"fail to complete {func.__name__} due to exception: ",
                        exc_info=True,
                    )

                    sleep_time_base = min(
                        start_sleep_time * (factor ** degree_curr),
                        sleep_time_limit,
                    ) / 2
                    sleep_time = sleep_time_base + uniform(0, sleep_time_base)
                    degree_curr += 1

                    logger.debug(f"try again after {sleep_time} seconds")
                    sleep(sleep_time)
                
                else:
                    break

            degree_curr = 0
            return result
        
        return wrapper
    
    return backoff_wrapper
