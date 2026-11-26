"""Start of the program. Run with: python -m timax_cue"""
import time
import logging

from .clock import SecondClock
from .packet import GoCuePacket
from .sender import TimaxSender
from .sequence import CueSequence
from .logsetup import setup_logging
from .timesync import resync_clock

HOST = "192.168.0.7" # The IP adress to send to
PORT = 59331 # UDP Port the timax listens to
NUM_CUES = 26 # Number of cues to cycle through
NTP_SERVER = "ntp2.sptime.se" # The NTP server to sync time against


def main() -> None:
    clock = SecondClock()
    cues = CueSequence(NUM_CUES)
    sender = TimaxSender(HOST, PORT)

    logging.info("Syncing the clock with...", NTP_SERVER)
    if resync_clock(NTP_SERVER):
        logging.info("Clock synced.")
    else:
        logging.warning("Continuing anyway, but cues may be off")

    while True:
        second = clock.wait_for_next_second()
        cue = cues.next_cue()
        packet = GoCuePacket(cue)
        try:
            sender.send(packet)
        except OSError as err:
            logging.warning("Could not send cue %d: %s", cue, err)

        utc = time.strftime("%H:%M:%S", time.gmtime(second))
        logging.info("%s UTC  cue %d", utc, cue)


if __name__ == "__main__":
    main()
