"""Start of the program. Run with: python -m timax_cue"""
import time

from .clock import SecondClock
from .packet import GoCuePacket
from .sender import TimaxSender
from .sequence import CueSequence
from .timesync import resync_clock

HOST = "192.168.0.7" # The IP adress to send to
PORT = 59331 # UDP Port the timax listens to
NUM_CUES = 26 # Number of cues to cycle through


def main() -> None:
    clock = SecondClock()
    cues = CueSequence(NUM_CUES)
    sender = TimaxSender(HOST, PORT)

    print("Syncing the clock with NTP...")
    if resync_clock():
        print("Clock synced.")
    else:
        print("Continuing anyway, but cues may be off")

    while True:
        second = clock.wait_for_next_second()
        cue = cues.next_cue()
        packet = GoCuePacket(cue)
        sender.send(packet)

        utc = time.strftime("%H:%M:%S", time.gmtime(second))
        print(f"{utc} UTC cue {cue}")


if __name__ == "__main__":
    main()
