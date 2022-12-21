from contextlib import ContextDecorator
from dataclasses import dataclass
from functools import wraps
from time import perf_counter, perf_counter_ns
from typing import Callable, ClassVar


@dataclass
class Timer(ContextDecorator):
    """
    Source: https://realpython.com/python-timer/

    A custom exception used to report errors in use of Timer class.

    ns_mode can be activated to avoid the precision loss caused by
    the float type when calling perf_counter(). Accuracy is the same.

    Additions:
    * Add a logging function
    """

    class TimerError(Exception):
        """A custom exception used to report errors in use of Timer class."""

    # Some constants
    NANOSECS_IN_SEC: ClassVar[int] = 10**9
    DEFAULT_TEXT: ClassVar[str] = "Elapsed time: {:0.4f} {}"

    # A class variable for keeping track accumulated time per object
    timers: ClassVar[dict] = {}

    # Main parameters
    _start_time = None
    ns_mode: bool = False
    return_ns: bool = False
    silent: bool = True
    timer_func: Callable = None
    logger: Callable = print
    name: str = None
    text: str = None
    supress_errors: bool = False

    def __post_init__(self):

        if self.name is not None:
            # Adds key to dict with value if not exists, otherwise returns already existing key's val
            self.timers.setdefault(self.name, 0)
        if self.timer_func is None:
            self.timer_func = perf_counter if not self.ns_mode else perf_counter_ns
        if self.text is None:
            self.text = self.text if self.text is not None else self.DEFAULT_TEXT

    def __call__(self, func):
        """
        (Optional when inheriting from DecoratorClass mixin). Support using Timer as a decorator.
        Only executes when being used as a decorator, and NOT context manager!

        @Timer()
        def some_func():
            ...
            return

        Every time timer is used as a decorator, itasically wraps the timer, and calls
        the function the Timer class is wrapped on!:

        With Timer as timer:
            function()

        For further features, i.e. creating a decorator factory, pls refer to decorator.py template!

        NOTE: As of now, this is not useful as there is no printing function on __exit__.
        """

        @wraps(func)
        def wrapper_timer(*args, **kwargs):
            # Performs __enter__ and __exit__ when used as a decorator!
            with self as _:
                return func(*args, **kwargs)

        return wrapper_timer

    def __enter__(self):
        """Start a new timer as a context manager"""
        self.start()
        return self

    def __exit__(self, *exc_info):
        """
        Stop the context manager timer.
        If __exit__ is set to True, will supress errors experienced in the with block (see https://stackoverflow.com/a/54077119/10002593)!

        exc_info = (exc_type, exc_value, exc_tb). Further reading: https://docs.python.org/3/reference/datamodel.html#object.__exit__
        """
        self.stop()
        return self.supress_errors

    def start(self) -> None:
        """Start a new timer"""
        if self._start_time is not None:
            raise self.TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = self.timer_func()

    def stop(
        self, reset: bool = False, soft: bool = False, print: bool = None
    ) -> float:
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise self.TimerError(f"Timer is not running. Use .start() to start it")
        elapsed_time = self.timer_func() - self._start_time
        unit_time = "nanoseconds" if self.return_ns else "seconds"
        if not soft:
            self._start_time = None

        if self.return_ns and not self.ns_mode:
            elapsed_time *= self.NANOSECS_IN_SEC
        elif not self.return_ns and self.ns_mode:
            elapsed_time /= self.NANOSECS_IN_SEC

        if self.name:
            # Add elapsed_time in seconds to accumulated timer!!
            self.timers[self.name] += (
                elapsed_time
                if not self.ns_mode
                else (elapsed_time / self.NANOSECS_IN_SEC)
            )

        print = print if print is not None else (not self.silent)
        if print and self.logger:
            self.logger(self.text.format(elapsed_time, unit_time))
        self._start_time = self.timer_func() if reset else self._start_time
        return elapsed_time
