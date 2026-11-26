# Configures Windows to keep its clock synced with an NTP server, then syncs now.
# The server is given with -Server 
# Run with administrator rights. Safe to run many times.
param([string]$Server = "ntp2.sptime.se")
# Keep the time service always running
Set-Service -Name w32time -StartupType Automatic
Start-Service -Name w32time

# Sync every 64 s (2^6) to ~17 min (2^10)
$config = "HKLM:\SYSTEM\CurrentControlSet\Services\W32Time\Config"
Set-ItemProperty -Path $config -Name MinPollInterval -Value 6 -Type DWord
Set-ItemProperty -Path $config -Name MaxPollInterval -Value 10 -Type DWord

# Use the given server as the time source, and apply the settings
w32tm /config /manualpeerlist:"$Server,0x8" /syncfromflags:manual /update
w32tm /config /update

# Give the service a moment to pick up the new server, then sync now
Start-Sleep -Seconds 2
w32tm /resync /rediscover
exit $LASTEXITCODE