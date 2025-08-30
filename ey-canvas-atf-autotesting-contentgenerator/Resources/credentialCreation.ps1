param(
    $target,
    $userName,
    $userPassword
)

$password = ConvertTo-SecureString $userPassword -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential ($userName, $password)
New-StoredCredential -Target $target -Credential $credential