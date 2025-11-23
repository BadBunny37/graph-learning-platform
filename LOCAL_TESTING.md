# Local Testing Guide

## Prerequisites

1. Python 3.9+ installed
2. Node.js installed
3. Supabase account with project set up
4. Google Gemini API key

## Setup

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Install Node Dependencies

```bash
npm install
```

### 3. Create .env File

Create a `.env` file in the root directory:

```env
SUPABASE_URL=https://ohhdqlciitoihqzyxqcn.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9oaGRxbGNpaXRvaWhxenl4cWNuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM4NTcyNjUsImV4cCI6MjA3OTQzMzI2NX0.s1mTR-UFVULzbh1d_Z_LMNqFxbYH04OfFzPIBDHa-mM
GEMINI_API_KEY=your_gemini_api_key_here
```

## Running Locally

### Option 1: Run Backend and Frontend Separately

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
npm run dev
```

Then open `http://localhost:5173` in your browser.

### Option 2: Test API Directly

```bash
# Start the backend
cd backend
uvicorn main:app --reload --port 8000

# Test health endpoint
curl http://localhost:8000/health

# Test with a document ID (replace with actual ID)
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"document_id": "your-document-id-here"}'
```

## Testing the Full Flow

1. **Start both servers** (backend and frontend)
2. **Open browser** to `http://localhost:5173`
3. **Sign up/Login** with your credentials
4. **Upload a PDF** document
5. **Click "Generate Graph"**
6. **Monitor backend logs** to see processing status
7. **Wait for graph** to render (may take 30-60 seconds)

## Troubleshooting

### Backend Issues

**Error: Module not found**
```bash
pip install -r backend/requirements.txt
```

**Error: Supabase connection failed**
- Check `.env` file has correct credentials
- Verify Supabase project is active

**Error: Gemini API failed**
- Check API key is valid
- Verify you have API quota remaining

### Frontend Issues

**Error: Cannot connect to backend**
- Ensure backend is running on port 8000
- Check CORS settings in `backend/main.py`

**Error: Supabase auth failed**
- Check credentials in `src/js/supabase.js`
- Verify Supabase project is active

## API Endpoints

### GET /health
Health check endpoint

**Response:**
```json
{
  "status": "ok"
}
```

### POST /process
Process a document and generate knowledge graph

**Request:**
```json
{
  "document_id": "uuid-here"
}
```

**Response:**
```json
{
  "message": "Processing completed",
  "document_id": "uuid-here"
}
```

### POST /scrape
Scrape additional information for a node

**Request:**
```json
{
  "document_id": "uuid-here",
  "node_id": "node-id-here",
  "topic": "Topic Name"
}
```

**Response:**
```json
{
  "message": "Scraping and update completed",
  "new_nodes": 5
}
```

## Database Schema

### documents table

```sql
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  title TEXT,
  file_path TEXT,
  status TEXT DEFAULT 'uploaded',
  study_mode TEXT,
  graph_data JSONB,
  created_at TIMESTAMPTZ DEFAULT timezone('utc', now())
);
```

### Graph Data Format

```json
{
  "nodes": [
    {
      "id": "concept_1",
      "label": "Concept Name",
      "description": "Brief description",
      "level": 1
    }
  ],
  "edges": [
    {
      "source": "concept_1",
      "target": "concept_2",
      "relation": "related_to"
    }
  ]
}
```

## Performance Tips

1. **PDF Size**: Keep PDFs under 10MB for faster processing
2. **Text Content**: PDFs with clear text extract better than scanned images
3. **API Quota**: Monitor your Gemini API usage
4. **Database**: Index frequently queried fields

## Next Steps

1. Test locally to ensure everything works
2. Deploy to Vercel
3. Monitor production logs
4. Optimize based on usage patterns
