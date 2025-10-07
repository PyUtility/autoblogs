# -*- encoding: utf-8 -*-

"""
A Set of Custom Decorators for AutoBlogs Module

The decorator module is designed to ease tasks and perform complex
operations. The internal behaviour of the agents are altered using the
following decorators.
"""

import time
import random
import functools

from typing import Any, Callable, Optional, Type, Tuple, Union

def retry(
        max_attempts : int = 3,
        backoff_factor : float = 2.0,
        initial_delay : float = 1.0,
        jitter : float = 0.5,
        retry_on : Optional[Union[Type[Exception], Tuple]] = None,
        verbose : bool = True
    ) -> Callable:
    """
    Provide ``@retry`` Exponential-Backoff Operator for Failed Calls

    Wraps a callable function and retries to re-call the API when
    there is :class:`app.src.errors.errors.AIRateLimitError` error
    raised. The sleeping parameter ``initial_delay`` determines the
    factor like $initial_delay * (backoff_factor ** max_attempts)$
    seconds between each attempts (plus an optional random jitter).

    :type  max_attempts: int
    :param max_attempts: Total number of call attempts (including the
        first attempt) before the application finally fails. Defaults
        to 3 attempts.

    :type  backoff_factor: float
    :param backoff_factor: Multiplier added to the delay (exponential)
        on each retry, defaults to 2.0 factor.

    :type  initial_delay: float
    :param initial_delay: Seconds to sleep after the first failure,
        defaults to 1 sec.

    :type  jitter: float
    :param jitter: Maximum random seconds added to each delay to avoid
        thundering herds; default to 0.5 factor.

    :type  retry_on: type | tuple | None
    :param retry_on: Exception type(s) that should trigger a retry.
        When ``None`` (default) all the exceptions are retried.

    :type  verbose: bool
    :param verbose: Prints retry attempt details to ``stdout``,
        defaults to True.
    """

    _retry_on = retry_on if retry_on is not None else Exception

    def decorator(func : Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            _last_exec : Optional[Exception] = None

            for attempt in range(1, max_attempts + 1):
                try:
                    func(*args, **kwargs)
                except _retry_on as exc:
                    _last_exec = exc

                    if attempt == max_attempts:
                        if verbose:
                            print("Max. Retries Failed.")
                        break
                    else:
                        _delay = initial_delay * (
                            backoff_factor ** (attempt - 1)
                        ) + random.uniform(0, jitter)

                        if verbose:
                            print(
                                f"VERBOSE: retry({func.__name__}) "
                                f"attempt {attempt}/{max_attempts} failed - "
                                f"retrying in {_delay:.2f}s; error: {exc}"
                            )

                        time.sleep(_delay)
            raise _last_exec
        return wrapper
    return decorator
