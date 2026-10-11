
Get-CimInstance Win32_Process -Filter "name = 'chrome.exe'" | ForEach-Object {
    if ($_.CommandLine -match "Worker-W") {
        Write-Output "$($_.ProcessId) : $($_.CommandLine)"
    }
}
