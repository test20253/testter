$naming_convention = '*.json'
$path_of_lock_files = 'C:\agents_information\lock_windows'
$path_of_unlock_files = 'C:\agents_information\unlock_windows'
$path_of_timeout_files = 'C:\agents_information\logs\timeout'
$path_of_success_files = 'C:\agents_information\logs\success'

while ($true) {
    Start-Sleep 10
    $files = Get-ChildItem -Path $path_of_lock_files -Filter $naming_convention -Recurse | ForEach-Object {$_.Name}
    $unlock_files = Get-ChildItem -Path $path_of_unlock_files -Filter $naming_convention -Recurse | ForEach-Object {$_.Name}
    $current_date = Get-Date -Format "yyyyMMddHHmmssffffff"
    $current_date = [datetime]::parseexact($current_date, 'yyyyMMddHHmmssffffff', $null)
    $already_running_flag = $false

    function createJSONFileOnPath([PSCustomObject]$json, [String]$path){
        Write-Host "Creating json on path $path"
        $json | ConvertTo-Json -depth 100 | Set-Content "$path"
    }

    function removeFileOnPath($path) {
        Write-Host "Removing file from path $path"
        Remove-Item -Path "$path" -Force
    }

    function getDateFromFileName($file_name) {
        $file_date = $file_name.split(".json")[0]
        $file_date = [datetime]::parseexact($file_date, 'yyyyMMddHHmmssffffff', $null)
        return $file_date
    }

    function getFileJSONContent($path) {
        Write-Host "Getting content of fily on path $path"
        $file_content = [PSCustomObject](Get-Content "$path" | Out-String | ConvertFrom-Json)
        return $file_content
    }

    #IS THERE A FILE ALREADY RUNNING?
    foreach ($file_name in $files) {
        $file_content = getFileJSONContent("$path_of_lock_files\$file_name")

        if ($file_content.status -eq "RUNNING") {
            $already_running_flag = $true
            $finished_successfully = $false
            $file_content.execution_date = [datetime]::parseexact($file_content.execution_date, 'yyyyMMddHHmmssffffff', $null)

            foreach ($file_name_unlock in $unlock_files) {
                $file_content_unlock = getFileJSONContent("$path_of_unlock_files\$file_name_unlock")
                if ($file_content_unlock.job_id -eq $file_content.job_id) {
                    removeFileOnPath("$($file_content.agent_id)\EXECUTE.JSON")
                    $file_content.status = "SUCCESS"
                    createJSONFileOnPath $file_content "$path_of_success_files\$file_name"
                    
                    $file_content_unlock.status = "SUCCESS"
                    createJSONFileOnPath $file_content_unlock "$path_of_success_files\$file_name_unlock"
                    removeFileOnPath("$path_of_unlock_files\$file_name_unlock")
                    $finished_successfully = $true
                    break;
                }
            }

            if ($finished_successfully -eq $false) {
                if ($current_date -gt $file_content.execution_date.AddSeconds($file_content.timeout)) {
                    removeFileOnPath("$($file_content.agent_id)\EXECUTE.JSON")
                    $file_content.status = "TIMEOUT_EXECUTION"
                    createJSONFileOnPath $file_content "$path_of_timeout_files\$file_name"
                    removeFileOnPath("$path_of_lock_files\$file_name")
                } else {
                    $already_running_flag = $true
                    Start-Sleep 10
                    break;
                }
            }
        }
    }

    $files = Get-ChildItem -Path $path_of_lock_files -Filter $naming_convention -Recurse | ForEach-Object {$_.Name}
    #THERE IS NO FILE RUNNING
    if ($already_running_flag -eq $false) {
        foreach ($file_name in $files) {
            $file_content = getFileJSONContent("$path_of_lock_files\$file_name")
            $file_date = getDateFromFileName($file_name)
            
            if ($current_date -gt $file_date.AddMinutes(9)) {
                $file_content.status = "TIMEOUT_RETRIEVAL"
                createJSONFileOnPath $file_content "$path_of_timeout_files\$file_name"
                removeFileOnPath("$path_of_lock_files\$file_name")
            }
        }

        $files = Get-ChildItem -Path $path_of_lock_files -Filter $naming_convention -Recurse | ForEach-Object {$_.Name}
        if ($files.Count -gt 0) {
            $file_name = $files | Select-Object -First 1
            $file_content = getFileJSONContent("$path_of_lock_files\$file_name")
            $file_content.status = "RUNNING"
            $file_content | Add-Member -MemberType NoteProperty -Name "execution_date" -Value $current_date
            createJSONFileOnPath $file_content "$($file_content.agent_id)\EXECUTE.JSON"
            removeFileOnPath("$path_of_lock_files\$file_name")
            createJSONFileOnPath $file_content "$path_of_lock_files\$file_name"
            Start-Sleep ($file_content.timeout)
        }
    }
}
