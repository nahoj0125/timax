from dataclasses import dataclass

HEADER = bytes([0x7D, 0x00, 0x03, 0x04])
PACKET_SIZE = 14
CUE_INDEX = 7


@dataclass(frozen=True)
class GoCuePacket:
    cue: int

    def __post_init__(self) -> None:
        if not 0 <= self.cue <= 255:
            raise ValueError(f"cue must be 0-255, got {self.cue}")

    def to_bytes(self) -> bytes:
        # Gives 00 * 14.
        data = bytearray(PACKET_SIZE)
        # Slices length of header.
        data[:len(HEADER)] = HEADER
        data[CUE_INDEX] = self.cue
        return bytes(data)
