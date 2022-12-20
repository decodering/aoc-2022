from time import perf_counter, perf_counter_ns


class Timer:
    class TimerError(Exception):
        """
        A custom exception used to report errors in use of Timer class.

        ns_mode can be activated to avoid the precision loss caused by
        the float type when calling perf_counter(). Accuracy is the same.
        """

    # Some constants
    NANOSECS_IN_SEC = 10**9

    def __init__(
        self,
        ns_mode: bool = False,
        return_ns: bool = False,
        silent: bool = True,
    ):
        self._start_time = None
        self.ns_mode = ns_mode
        self.return_ns = return_ns
        self.silent = silent
        self.timer_func = perf_counter if not ns_mode else perf_counter_ns

    def start(self) -> None:
        """Start a new timer"""
        if self._start_time is not None:
            raise self.TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = self.timer_func()

    def stop(self, print: bool = None) -> float:
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise self.TimerError(f"Timer is not running. Use .start() to start it")
        elapsed_time = self.timer_func() - self._start_time
        unit_time = "nanoseconds" if self.return_ns else "seconds"
        self._start_time = None

        if self.return_ns and not self.ns_mode:
            elapsed_time *= self.NANOSECS_IN_SEC
        elif not self.return_ns and self.ns_mode:
            elapsed_time /= self.NANOSECS_IN_SEC

        print = print if print is not None else (not self.silent)
        if print:
            self._print(f"Elapsed time: {elapsed_time:0.4f} {unit_time}")
        return elapsed_time

    @staticmethod
    def _print(string: str):
        print(string)
