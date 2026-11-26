import time
"""Timing waits for each whole second on the compuers clock"""

class SecondClock:
    """Wakes up exactly on each whole second
    
    Uses computer's own clock, which the operating system keep synced."""
    def wait_for_next_second(self) -> None:
        """Sleep until next whole second.
        
        Example: if the time is 1000.734, it sleeps 0.266 secondsand returns 1001
        
        Returns:
            The whole second it wakes up at as Unix time"""
        now = time.time()
        next_second = int(now) + 1
        time.sleep(next_second - now)
        return next_second
