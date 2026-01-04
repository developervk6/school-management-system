# Git Repository Setup Guide

## Current Status
✅ Git is initialized
✅ Placeholder remote has been removed
⚠️ You need to add your actual GitHub repository

## Option 1: Connect to Existing GitHub Repository

If you already have a GitHub repository created:

```powershell
# Replace YOUR_USERNAME and YOUR_REPO_NAME with your actual values
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Then push your code
git push -u origin master
```

**Or using SSH (if you have SSH keys set up):**
```powershell
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin master
```

## Option 2: Create New GitHub Repository

### Step 1: Create Repository on GitHub
1. Go to https://github.com/new
2. Repository name: `school-management-system` (or any name you prefer)
3. Description: "School Management Web Application using Flask"
4. Choose Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### Step 2: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```powershell
# Add the remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/school-management-system.git

# Push your code
git push -u origin master
```

## Option 3: Use GitHub CLI (if installed)

If you have GitHub CLI (`gh`) installed:

```powershell
# Create repository and push in one command
gh repo create school-management-system --public --source=. --remote=origin --push
```

## Authentication

### For HTTPS:
- GitHub no longer accepts passwords for Git operations
- You need to use a **Personal Access Token (PAT)**

**To create a PAT:**
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name and select scopes: `repo` (full control)
4. Copy the token
5. When pushing, use the token as your password (username is your GitHub username)

### For SSH:
- Set up SSH keys on GitHub
- More secure and convenient for regular use

## Verify Setup

After adding the remote, verify it:

```powershell
git remote -v
```

You should see your repository URL.

## Common Commands

```powershell
# Check status
git status

# Add all files
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push origin master

# Pull latest changes
git pull origin master
```

## Troubleshooting

### "Repository not found" error:
- Check that the repository exists on GitHub
- Verify the URL is correct
- Make sure you have access to the repository

### "Authentication failed" error:
- For HTTPS: Use Personal Access Token instead of password
- For SSH: Make sure your SSH key is added to GitHub

### "Permission denied" error:
- Check your GitHub username and repository name
- Verify you have write access to the repository

