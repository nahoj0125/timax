import time

from .clock import SecondClock
from .packet import GoCuePacket
from .sender import TimaxSender
from .sequence import CueSequence


HOST = "127.0.0.1"
PORT = 0
NUM_CUES = 14


def main() -> None:
    clock = SecondClock()
    cues = CueSequence(NUM_CUES)
    sender = TimaxSender(HOST, PORT)

    while True:
        second = clock.wait_for_next_second()
        cue = cues.next_cue()
        packet = GoCuePacket(cue)
        sender.send(packet)

        utc = time.strftime("%H:%M:%S", time.gmtime(second))
        print(f"{utc} UTC cue {cue}")


if __name__ == "__main__":
    main()
