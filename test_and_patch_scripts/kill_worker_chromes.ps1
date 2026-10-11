
Get-CimInstance Win32_Process | Where-Object { 
    $_.Name -eq 'chrome.exe' -and $_.CommandLine -like '*stickman-video-automation\Workers*' 
} | ForEach-Object { 
    Write-Output "Killing PID: $($_.ProcessId)"
    Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue 
}
