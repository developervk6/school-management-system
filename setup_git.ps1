# GitHub Repository Setup Script
# Edit the variables below with your GitHub information

$GITHUB_USERNAME = "YOUR_USERNAME_HERE"  # Replace with your GitHub username
$REPO_NAME = "school-management-system"  # Change if you want a different name

# Check if variables are set
if ($GITHUB_USERNAME -eq "YOUR_USERNAME_HERE") {
    Write-Host "`n❌ Please edit this script and set your GitHub username!" -ForegroundColor Red
    Write-Host "`nOpen setup_git.ps1 and replace YOUR_USERNAME_HERE with your actual GitHub username" -ForegroundColor Yellow
    exit
}

# Check if git remote already exists
$existingRemote = git remote get-url origin 2>$null
if ($existingRemote) {
    Write-Host "`n⚠️  Remote 'origin' already exists: $existingRemote" -ForegroundColor Yellow
    $response = Read-Host "Do you want to remove it and add a new one? (y/n)"
    if ($response -eq "y" -or $response -eq "Y") {
        git remote remove origin
        Write-Host "✓ Removed existing remote" -ForegroundColor Green
    } else {
        Write-Host "Cancelled." -ForegroundColor Yellow
        exit
    }
}

# Add the remote
$remoteUrl = "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
Write-Host "`n📦 Adding remote repository..." -ForegroundColor Cyan
Write-Host "   URL: $remoteUrl" -ForegroundColor Gray

git remote add origin $remoteUrl

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Remote added successfully!" -ForegroundColor Green
    
    # Verify
    Write-Host "`n📋 Current remotes:" -ForegroundColor Cyan
    git remote -v
    
    Write-Host "`n✅ Setup complete!" -ForegroundColor Green
    Write-Host "`nNext steps:" -ForegroundColor Yellow
    Write-Host "1. Make sure the repository exists on GitHub" -ForegroundColor White
    Write-Host "2. If not, create it at: https://github.com/new" -ForegroundColor White
    Write-Host "3. Then push your code: git push -u origin master" -ForegroundColor White
    Write-Host "`nNote: You'll need a Personal Access Token for authentication" -ForegroundColor Gray
} else {
    Write-Host "❌ Failed to add remote. Check your repository URL." -ForegroundColor Red
}

