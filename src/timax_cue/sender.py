import socket
from .packet import GoCuePacket


class TimaxSender:
    def __init__(self, host: str, port: int) -> None:
        self._adress = (host, port)
        # AF_INET = IPv4, SOCK_DGRAM = UDP.
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, packet: GoCuePacket) -> None:
        self._sock.sendto(packet.to_bytes(), self._adress)

    def close(self) -> None:
        self._sock.close()
