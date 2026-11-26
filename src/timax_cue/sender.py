import socket
from .packet import GoCuePacket
"""Sends packet to the timax unit over the network"""

class TimaxSender:
    """Sends packets to one timax unit over UDP.
    Create it once with timax adress, then call send() for every packet.
    Call close() when you are done."""
    def __init__(self, host: str, port: int) -> None:
        """Store the adressand open a UP socket.
        
        Args: 
            host: the timax IP adress
            port: The UDP port the timax listens to"""
        self._adress = (host, port)
        # AF_INET = IPv4, SOCK_DGRAM = UDP.
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, packet: GoCuePacket) -> None:
        """Sends one packet to the timax unit
        
        Args:
            packet: The packet to send
            
        Raises:
            OSError: If the networkrefuses to sendor no network connection"""
        print("Sending cue", packet.cue, "to", self._adress, "->", packet.to_bytes().hex(" "))
        self._sock.sendto(packet.to_bytes(), self._adress)

    def close(self) -> None:
        """Closes the socket"""
        self._sock.close()
