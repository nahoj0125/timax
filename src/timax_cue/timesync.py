"""Configures Windows time sync and syncs the clock when the program starts."""

import ctypes
import os
import platform
import subprocess
from pathlib import Path

WINDOWS_DIR = os.environ.get("SystemRoot", r"C:\Windows")
POWERSHELL = os.path.join(WINDOWS_DIR, "System32", "WindowsPowerShell", "v1.0", "powershell.exe")
SCRIPT = Path(__file__).parent / "sync_time.ps1"


def _is_admin() -> bool:
    """Check whether the program is already running with administrator rights.

    Returns:
        True if it is (e.g. when started by Task Scheduler at boot), False otherwise.
    """
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def _run_script_directly(server: str) -> int:
    """Run sync_time.ps1 with this process's rights. Used when already administrator.

    Args:
        server: The NTP server to sync with, e.g. "ntp2.sptime.se".

    Returns:
        The script's exit code: 0 if the sync worked.
    """
    result = subprocess.run(
        [POWERSHELL, "-NoProfile", "-ExecutionPolicy", "Bypass",
         "-File", str(SCRIPT), "-Server", server]
    )
    return result.returncode


def _run_script_as_admin(server: str) -> int:
    """Run sync_time.ps1 as administrator. Windows shows a box asking for permission.

    Args:
        server: The NTP server to sync with, e.g. "ntp2.sptime.se".

    Returns:
        The script's exit code: 0 if the sync worked, non-zero if it failed
        or permission was refused.
    """
    command = (
        f"$p = Start-Process -FilePath '{POWERSHELL}' "
        f"-ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','\"{SCRIPT}\"','-Server','{server}' "
        f"-Verb RunAs -WindowStyle Hidden -Wait -PassThru; exit $p.ExitCode"
    )
    result = subprocess.run([POWERSHELL, "-NoProfile", "-Command", command])
    return result.returncode


def resync_clock(server: str) -> bool:
    """Set up Windows time sync against the given server and sync the clock now.

    If the program already has administrator rights (started at boot), it runs
    directly. Otherwise Windows asks for permission: click Yes.
    Does nothing on Linux/Mac, where the operating system syncs by itself.

    Args:
        server: The NTP server to sync with, e.g. "ntp2.sptime.se".

    Returns:
        True if the sync worked (or if not on Windows), False otherwise.
    """
    if platform.system() != "Windows":
        return True

    try:
        if _is_admin():
            exit_code = _run_script_directly(server)
        else:
            exit_code = _run_script_as_admin(server)
    except FileNotFoundError as err:
        print("WARNING: could not start PowerShell, clock not synced!")
        print(err)
        return False

    if exit_code != 0:
        print("WARNING: could not sync the clock (or permission was refused).")
        return False
    return True