Param($requiredVersion,
$pat_token
)

function Get-CurrentVersion {
    param (
        [string]$LibraryName
    )
    try {
        $currentVersionInfo = pip show $LibraryName 2>&1 | Select-String "Version"
        if ($null -ne $currentVersionInfo) {
            $currentVersion = $currentVersionInfo.Line.Split(' ')[1]
            return $currentVersion
        } else {
            Write-Host "The library '$LibraryName' is not installed or the version information could not be retrieved."
            return $null
        }
    } catch {
        Write-Host "An error occurred while attempting to show the package information: $_"
        return $null
    }
}

$currentVersion = Get-CurrentVersion -LibraryName 'CTE-ADO-Script-less'
  Write-Host "currentVersion: $currentVersion"
  Write-Host "requiredVersion: $requiredVersion"

 
if (($currentVersion -eq $requiredVersion) ) {
        Write-Host "requiredVersion Is already installed."
    } else {
            Write-Host "Installing the version $requiredVersion"
            if (($null -ne $currentVersion) ){
                pip uninstall CTE-ADO-Script-less -y
                pip uninstall selenium -y
            }
            pip install CTE-ADO-Script-less==${requiredVersion} --index-url https://build:${pat_token}@eysbp.pkgs.visualstudio.com/_packaging/ADO-Scriptless/pypi/simple
       
        Write-Host "The scriptles version has been updated from: $requiredVersion to the version: $currentVersion."
    }
