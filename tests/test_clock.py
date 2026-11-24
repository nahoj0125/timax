import time
from timax_cue.clock import SecondClock


def test_wakes_up_on_a_whole_second():
    clock = SecondClock()
    second = clock.wait_for_next_second()
    now = time.time()

    assert now >= second
    assert now - second < 0.05
