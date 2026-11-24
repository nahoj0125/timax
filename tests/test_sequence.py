from timax_cue.sequence import CueSequence


def test_counts_up_and_wraps():
    seq = CueSequence(3)
    results = [seq.next_cue() for _ in range(7)]
    assert results == [1, 2, 3, 1, 2, 3, 1]
