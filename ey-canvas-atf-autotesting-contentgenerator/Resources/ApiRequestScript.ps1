param(
    [Parameter(Mandatory=$true)]
    [string]$url,

    [Parameter(Mandatory=$true)]
    [string]$headers,

    [Parameter(Mandatory=$true)]
    [string]$method,

    $body
)

$customObject = $headers | ConvertFrom-Json
$body = ConvertFrom-Json $body
$body = ConvertTo-JSON $body -Depth 6

$dictionary = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
foreach ($property in $customObject.PSObject.Properties) {
      $dictionary.Add($property.Name, $property.Value)
}

$response = Invoke-RestMethod -Uri $url -Method $method -Headers $dictionary -Body $body -ContentType "application/json"
$response | ConvertTo-Json
