# Configures Windows to keep its clock synced with ntp2.sptime.se, then syncs now.
# Run with administrator rights. Safe to run many times.

# Keep the time service always running
Set-Service -Name w32time -StartupType Automatic
Start-Service -Name w32time

# Sync every 64 s (2^6) to ~17 min (2^10)
$config = "HKLM:\SYSTEM\CurrentControlSet\Services\W32Time\Config"
Set-ItemProperty -Path $config -Name MinPollInterval -Value 6 -Type DWord
Set-ItemProperty -Path $config -Name MaxPollInterval -Value 10 -Type DWord

# Use ntp2.sptime.se as the time server, and apply the settings
w32tm /config /manualpeerlist:"ntp2.sptime.se,0x8" /syncfromflags:manual /update
w32tm /config /update

# Give the service a moment to pick up the new server, then sync now
Start-Sleep -Seconds 2
w32tm /resync /rediscover
exit $LASTEXITCODE