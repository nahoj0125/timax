# TiMax Cue

## Configure NTP Server
Simply change the varible in \_\_main__.py
```python
NTP_SERVER = xxxxxxxx
```

## Configure auto start
1. Open Task Scheduler

Press Start, type `Schemaläggaren`  (Task Scheduler) and open it.

In the right-hand panel, click Skapa aktivitet… (Create Task…). **Don't use "Create Basic Task"**, which lacks the settings you need.

2. The General tab
`Name: TiMax Cue`
Click Change User or Group…, type `SYSTEM`, click Check Names, then OK. This makes it run without anyone logging in.
Tick Run with highest privileges. This gives it _administrator rights_, so the clock sync works without the "Yes" box.
3. The Triggers tab

Click New…:

Begin the task: At startup
Under Advanced settings, tick Delay task for: 30 seconds, so the network has time to start.
Make sure Enabled is ticked. Click OK.
4. The Actions tab

Click New…, choose Start a program, and fill in:

Program/script:
`C:\Windows\System32\cmd.exe`
Add arguments:
`/c ""C:\Users\servi\timax\.venv\Scripts\python.exe" -u -m timax_cue >> "C:\Users\servi\timax\timax.log" 2>&1"`
Start in:
`C:\Users\servi\timax`

Copy the arguments **exactly**, _including the double quotes at the start_. Click OK.

5. The Conditions tab

Untick Start the task only if the computer is on AC power. Otherwise a laptop wouldn't start it on battery.

6. The Settings tab
Tick Allow task to be run on demand, so you can test it.
Tick Run task as soon as possible after a scheduled start is missed.
Tick If the task fails, restart every: 1 minute, Attempt to restart up to: 999 times.
Untick "Stop the task if it runs longer than". This is important: by default Windows stops it after 3 days.

Click OK. Windows may ask for your password.

7. Test it

In the list in the middle, find TiMax Cue, right-click it and choose Run. Then watch the log in PowerShell:

```powershell
Get-Content C:\Users\servi\timax\timax.log -Wait -Tail 10
```

The cues should appear. 

To change anything later, right-click the task and choose Properties.

## What to do when TiMax is not reacting?
In order: is the task running → are cues in the log → are there "could not send" warnings → does ping reach the TiMax → is UDP control enabled in the TiMax.

## How to restart
End and Run in Task Scheduler, or reboot the computer.

## Duoble cues?
Don't start it by hand while the task runs. There will be double cues then.

## Timax settings
What does each cue do?
1. NRH2 kam
2. NRH2 sten
3. NRH2 saltkar
4. H2 penvessare
5. RH2 tendsticka
6. RH2 vattenglas
7. NRH2 bok
8. NRH2 kam
9. NRH2 sten
10. NRH2 saltkar
11. H2 penvessare
12. RH2 tendsticka
13. RH2 vattenglas
14. NRH" bok

## Check lateancy to NTP
```powershell
w32tm /stripchart /computer:ntp2.sptime.se /samples:5 /dataonly
```

## Legacy
[Old arduino sctech](legacy/arduino_sctech.txt)