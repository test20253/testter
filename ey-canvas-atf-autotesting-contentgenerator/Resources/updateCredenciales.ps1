param(
    [Parameter(Mandatory=$true)]
    [string]$targetUser,

    [Parameter(Mandatory=$true)]
    [string]$newEmail,

    [Parameter(Mandatory=$true)]
    [string]$newPassword
)

# Path to the .env file
$envFilePath = ".env"

# Regex pattern for matching the target user's line
$pattern = "^$targetUser\s*=\s*\{\s*'userName':\s*'([^'])*'\s*,\s*'password':\s*'([^'])'*.*"

try {
    # Read the file line by line
    $fileContent = Get-Content -Path $envFilePath -ErrorAction Stop

    # Variable to store the updated content
    $updatedContent = $fileContent | ForEach-Object {
        if ($_ -match $pattern) {
            # Replace if a match is found
            "$targetUser={'userName': '$newEmail','password': '$newPassword','credentialUserName': '$targetUser'}"
        }
        else {
            # Keep the original line if no match is found
            $_
        }
    }

    # Write the updated content back to the file
    $updatedContent | Set-Content -Path $envFilePath -ErrorAction Stop

    Write-Host "Values of email and password updated for the user $targetUser."
}
catch {
    Write-Host "Error: $_"
}
