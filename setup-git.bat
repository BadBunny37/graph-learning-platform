@echo off
echo Initializing Git repository...
git init

echo Adding all files...
git add .

echo Committing files...
git commit -m "Add Vercel API endpoint and fix 404 error"

echo.
echo Git repository initialized!
echo.
echo Next steps:
echo 1. Create a new repository on GitHub
echo 2. Copy the repository URL
echo 3. Run: git remote add origin YOUR_GITHUB_URL
echo 4. Run: git push -u origin main
echo.
pause
