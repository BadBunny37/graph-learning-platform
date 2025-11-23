# Deployment Checklist for Vercel

## ✅ Fixed Issues

### 1. **404 Error - Missing API Directory**
- **Problem**: Vercel was looking for `/api/index.py` but it didn't exist
- **Solution**: Created `api/index.py` as the serverless function entry point
- **Files Created**:
  - `api/index.py` - Main API handler for Vercel
  - `api/requirements.txt` - Python dependencies

### 2. **Vercel Configuration**
- **Problem**: `vercel.json` was using rewrites instead of builds/routes
- **Solution**: Updated `vercel.json` to properly configure Python serverless functions
- **Changes**:
  ```json
  {
    "builds": [
      {
        "src": "api/index.py",
        "use": "@vercel/python"
      }
    ],
    "routes": [...]
  }
  ```

### 3. **Security Issue - RLS Disabled**
- **Problem**: Row Level Security was disabled on `documents` table
- **Solution**: Enabled RLS and created proper policies
- **Migration Applied**: `enable_rls_on_documents`

## 🔧 Required Actions Before Deployment

### 1. **Set Environment Variables in Vercel**

Go to your Vercel project settings and add these environment variables:

```
SUPABASE_URL=https://ohhdqlciitoihqzyxqcn.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9oaGRxbGNpaXRvaWhxenl4cWNuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM4NTcyNjUsImV4cCI6MjA3OTQzMzI2NX0.s1mTR-UFVULzbh1d_Z_LMNqFxbYH04OfFzPIBDHa-mM
GEMINI_API_KEY=<your_gemini_api_key_here>
```

**Important**: Replace `<your_gemini_api_key_here>` with your actual Google Gemini API key.

### 2. **Push Changes to GitHub**

```bash
git add .
git commit -m "Fix: Add Vercel serverless function and enable RLS"
git push origin main
```

### 3. **Redeploy on Vercel**

After pushing to GitHub, Vercel will automatically redeploy. If not, manually trigger a deployment.

## 📋 Verification Steps

After deployment, verify:

1. ✅ Visit your Vercel URL
2. ✅ Sign up/Login works
3. ✅ Upload a PDF document
4. ✅ Click "Generate Graph" - should NOT get 404 error
5. ✅ Check Vercel function logs for processing status
6. ✅ Verify document status changes from "uploaded" to "processing" to "completed"
7. ✅ Graph should render after processing completes

## 🐛 Debugging

### Check Vercel Function Logs

1. Go to Vercel Dashboard
2. Select your project
3. Click on "Functions" tab
4. View logs for `/api/index.py`

### Common Issues

**Issue**: Still getting 404
- **Solution**: Ensure environment variables are set in Vercel
- **Solution**: Check that `api/index.py` exists in the deployed code

**Issue**: Processing fails
- **Solution**: Check Gemini API key is valid
- **Solution**: Verify Supabase credentials are correct
- **Solution**: Check function logs for specific errors

**Issue**: Documents stuck in "uploaded" status
- **Solution**: Check Vercel function logs
- **Solution**: Verify the backend can download files from Supabase storage
- **Solution**: Ensure Gemini API has sufficient quota

## 📊 Database Status

Current state of documents table:
- **Total documents**: 10
- **Status**: All currently "uploaded" (need reprocessing)
- **RLS**: ✅ Now enabled with proper policies

## 🔐 Security Improvements

1. ✅ Enabled RLS on `documents` table
2. ✅ Created user-specific access policies
3. ⚠️ Consider enabling leaked password protection in Supabase Auth settings

## 📝 Next Steps

1. Set environment variables in Vercel
2. Push code to GitHub
3. Wait for deployment
4. Test the application
5. Monitor function logs
6. (Optional) Reprocess existing documents by clicking "Generate Graph" again

## 🆘 Support

If issues persist:
1. Check Vercel function logs
2. Check browser console for errors
3. Verify Supabase connection
4. Ensure all environment variables are set correctly
