# Vercel Deployment Quick Fix Guide

## Current Issue: 404 NOT_FOUND Error

You're getting a 404 error because Vercel needs the new files to be uploaded. Here's what to do:

### Step 1: Verify Files Exist Locally

Make sure these files exist in your project:
- ✅ `api/index.py`
- ✅ `api/requirements.txt`
- ✅ `vercel.json` (updated)

### Step 2: Upload to Vercel

Since you're uploading files directly to Vercel (not using Git), you need to:

1. **Zip your entire project folder** including the new `api` directory
2. **Delete the old deployment** in Vercel (optional but recommended)
3. **Upload the new zip file** to Vercel

OR use the Vercel CLI:

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

### Step 3: Set Environment Variables

In Vercel Dashboard → Your Project → Settings → Environment Variables:

Add these 3 variables:
```
SUPABASE_URL=https://ohhdqlciitoihqzyxqcn.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9oaGRxbGNpaXRvaWhxenl4cWNuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM4NTcyNjUsImV4cCI6MjA3OTQzMzI2NX0.s1mTR-UFVULzbh1d_Z_LMNqFxbYH04OfFzPIBDHa-mM
GEMINI_API_KEY=your_actual_gemini_api_key
```

### Step 4: Test the API

After deployment, test these URLs:

1. **Root API**: `https://your-site.vercel.app/api`
   - Should return: `{"status": "ok", "message": "Graph Learning Platform API"}`

2. **Health Check**: `https://your-site.vercel.app/api/health`
   - Should return: `{"status": "ok"}`

3. **Your Dashboard**: `https://your-site.vercel.app/dashboard.html`
   - Should load the dashboard

### Alternative: Use Git (Recommended)

If you want automatic deployments:

```bash
# Initialize git in your project
cd "c:/Users/sruja/OneDrive/Documents/dsa/graph-learning-platform-main/graph-learning-platform-main"
git init

# Add all files
git add .

# Commit
git commit -m "Add Vercel API and fix 404 error"

# Add remote (replace with your GitHub repo URL)
git remote add origin https://github.com/yourusername/graph-learning-platform.git

# Push
git push -u origin main
```

Then connect your GitHub repo to Vercel for automatic deployments.

### Troubleshooting

**Still getting 404?**
1. Check Vercel deployment logs
2. Verify the `api` folder was uploaded
3. Check that environment variables are set
4. Try accessing `/api/health` directly

**Can't find the api folder?**
- Make sure you're uploading the entire project, not just individual files
- The folder structure should be:
  ```
  your-project/
  ├── api/
  │   ├── index.py
  │   └── requirements.txt
  ├── backend/
  ├── src/
  ├── dashboard.html
  └── vercel.json
  ```

**Environment variables not working?**
- Make sure to redeploy after adding environment variables
- Check that variable names match exactly (case-sensitive)
