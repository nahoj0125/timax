class CueSequence:
    def __init__(self, count: int) -> None:
        self._count = count
        self._current = 0

    def next_cue(self) -> int:
        self._current = self._current % self._count + 1
        return self._current
