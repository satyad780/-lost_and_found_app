# Create GitHub repo and push via HTTPS
# Prompts securely for a GitHub Personal Access Token (repo scope)
param()

$token = Read-Host -AsSecureString 'Paste a GitHub Personal Access Token (repo scope) and press Enter'
$ptr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($token)
$pat = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($ptr)

$body = @{ name = 'lost_and_found_app'; private = $false } | ConvertTo-Json

try {
    $resp = Invoke-RestMethod -Uri 'https://api.github.com/user/repos' -Method Post -Headers @{ Authorization = "token $pat"; 'User-Agent' = 'lost_and_found_app' } -Body $body
    Write-Host "Repo created at: $($resp.html_url)"
} catch {
    if ($_.Exception.Response -ne $null) {
        $status = $_.Exception.Response.StatusCode.Value__
        Write-Host "GitHub API error: $status"
        Write-Host $_.Exception.Message
        if ($status -eq 422) {
            Write-Host "It looks like a repo with that name already exists in your account. I'll switch to using the existing repo and attempt to push."
        } else {
            exit 1
        }
    } else {
        Write-Host $_.Exception.Message
        exit 1
    }
}

# Set HTTPS remote and push (will prompt for credentials if needed)
git remote set-url origin https://github.com/satyalankar/lost_and_found_app.git
Write-Host 'Pushing to https://github.com/satyalankar/lost_and_found_app.git (you may be prompted for credentials: use your GitHub username and the PAT as the password)...'
git push -u origin master

Write-Host 'Done.'
