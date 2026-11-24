import time


class SecondClock:
    def wait_for_next_second(self) -> None:
        now = time.time()
        next_second = int(now) + 1
        time.sleep(next_second - now)
        return next_second
