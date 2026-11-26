"""Configures Windows time sync and syncs the clock when the program starts."""

import os
import platform
import subprocess
from pathlib import Path

WINDOWS_DIR = os.environ.get("SystemRoot", r"C:\Windows")
POWERSHELL = os.path.join(WINDOWS_DIR, "System32", "WindowsPowerShell", "v1.0", "powershell.exe")
SCRIPT = Path(__file__).parent / "sync_time.ps1"


def resync_clock() -> bool:
    """Set up Windows time sync and sync the clock now, with administrator rights.

    Runs sync_time.ps1 as administrator, so Windows shows a box asking for
    permission. Click Yes. Does nothing on Linux/Mac, where the operating
    system handles syncing by itself.

    Returns:
        True if the sync worked (or if not on Windows), False if it failed
        or permission was refused.
    """
    if platform.system() != "Windows":
        return True

    # Start a second PowerShell as administrator that runs the script, wait for it,
    # and pass on its exit code
    command = (
        f"$p = Start-Process -FilePath '{POWERSHELL}' "
        f"-ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','\"{SCRIPT}\"' "
        f"-Verb RunAs -WindowStyle Hidden -Wait -PassThru; exit $p.ExitCode"
    )

    try:
        result = subprocess.run([POWERSHELL, "-NoProfile", "-Command", command])
    except FileNotFoundError as err:
        print("WARNING: could not start PowerShell, clock not synced!")
        print(err)
        return False

    if result.returncode != 0:
        print("WARNING: could not sync the clock (or permission was refused).")
        return False
    return True