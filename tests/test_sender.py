import socket
from timax_cue.packet import GoCuePacket
from timax_cue.sender import TimaxSender


def test_sends_packet_over_udp():
    fake_timax = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    fake_timax.bind(("127.0.0.1", 0))
    fake_timax.settimeout(1)
    host, port = fake_timax.getsockname()

    sender = TimaxSender(host, port)
    sender.send(GoCuePacket(5))
    sender.close()

    received = fake_timax.recv(64)
    fake_timax.close()

    # 'pytest -s', otherwise pytest hides all prints.
    print(received)
    print(received.hex(" "))
    assert received == GoCuePacket(5).to_bytes()
