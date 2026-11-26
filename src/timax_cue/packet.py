"""Builds the UDP message that tells the timax which cue to play"""

from dataclasses import dataclass

HEADER = bytes([0x7D, 0x00, 0x03, 0x04]) # Fixed start of every cue message.
PACKET_SIZE = 14 # Total length of the message in bytes.
CUE_INDEX = 7 # Position of the cue number in the message. 


@dataclass(frozen=True)
class GoCuePacket:
    """A single message for the timax.
    
    The object is read-only (frozen), so message can not be change after its creation."""
    cue: int

    def __post_init__(self) -> None:
        """Check the cue number right after creation of the packet.
        
        Raises:
            ValueError: If the cue is outside of 0-255"""
        if not 0 <= self.cue <= 255:
            raise ValueError(f"cue must be 0-255, got {self.cue}")

    def to_bytes(self) -> bytes:
        """Builds the 14 bytes that are sent over the networkk.
        
        Layout: header: (7D 00 03 04), the cue number at byte 7, 0 everywhere else.
        
        Returns:
            The finished message. Example for cue 5:
            7D 00 03 04 00 00 00 05 00 00 00 00 00 00"""
        data = bytearray(PACKET_SIZE)
        data[:len(HEADER)] = HEADER # Slices length of header.
        data[CUE_INDEX] = self.cue
        return bytes(data)
