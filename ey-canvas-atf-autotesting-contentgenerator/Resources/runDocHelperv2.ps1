function Get-DocCredential {

    $credential = Get-StoredCredential -Target 'eydocument' -ErrorAction SilentlyContinue

    if(!$credential){
        $credential = Get-Credential
    }
    return $credential
}

function Stop-DocProcess {

    $eyDocProcess = Get-Process -ProcessName "EY.Canvas.DocumentHelper.*" -ErrorAction SilentlyContinue

    if($eyDocProcess){
      $eyDocProcess | ForEach-Object {
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
        Write-Host $_.Name $_.Id "process was stopped"
      }
    }      
}

function Start-DocProcess {
    param(
        $path,
        $credential
    )

    Start-Process $path -Credential $credential
    $eyDocProcess = Get-Process -ProcessName "EY.Canvas.DocumentHelper.Monitor" -ErrorAction SilentlyContinue
    if($eyDocProcess){
      Write-Host "EY.Canvas.DocumentHelper.Monitor process Is running"
    }
    else{
      Write-Host "EY.Canvas.DocumentHelper.Monitor process Is NOT running"
    }      
}

$docHelperPath = "C:\Program Files (x86)\EY.Canvas.DocumentHelper.Installer\EY.Canvas.DocumentHelper.Monitor.exe"
$userCredential = Get-DocCredential
Stop-DocProcess
Start-DocProcess -path $docHelperPath -credential $userCredential
