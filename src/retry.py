import time
import functools
import logging


def retry(exceptions, tries=3, delay=1, backoff=2):
    """
    Retry calling the decorated function using exponential backoff.

    :param exceptions: Exception(s) to catch.
    :param tries: Number of attempts.
    :param delay: Initial delay between attempts.
    :param backoff: Multiplier applied to the delay after each failure.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _tries, _delay = tries, delay
            while _tries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logging.warning(
                        f"{func.__name__} failed with {e!r}. "
                        f"Retrying in {_delay}s... ({_tries - 1} tries left)"
                    )
                    time.sleep(_delay)
                    _tries -= 1
                    _delay *= backoff

            # Last attempt — let exceptions bubble up
            return func(*args, **kwargs)

        return wrapper

    return decorator
