import pytest
from timax_cue.packet import GoCuePacket


def test_matches_arduino_packet():
    assert GoCuePacket(1).to_bytes() == bytes(
        [0x7D, 0x00, 0x03, 0x04, 0, 0, 0, 0x01, 0, 0, 0, 0, 0, 0]
    )


@pytest.mark.parametrize("cue", [-1, 256])
def test_reject_inavlid_cue(cue):
    with pytest.raises(ValueError):
        GoCuePacket(cue)


@pytest.mark.parametrize("cue", [0, 1, 255])
def test_valid_cue(cue):
    data = GoCuePacket(cue).to_bytes()
    assert len(data) == 14
    assert data[7] == cue
