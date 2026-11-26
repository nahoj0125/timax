"""Keeps track of which cue comes next."""

class CueSequence:
    """Counts through the cues and starts over on 1 """
    def __init__(self, count: int) -> None:
        """Sets up the counterso the first callto next_cue() returns 1
        
        Args:
            count: How many cues there are."""
        self._count = count
        self._current = 0

    def next_cue(self) -> int:
        """Steps one cue forward and return it. After the last cue it starts over at 1.
        
        Returns:
            The new cue number, between 1 and count"""
        self._current = self._current % self._count + 1
        return self._current
