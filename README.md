# Graph Learning Platform

A 3D knowledge graph visualization platform that transforms documents into interactive, explorable graphs using AI.

## Features

- 📄 Upload PDF documents and convert them to knowledge graphs
- 🎯 Multiple study modes: Research, General, Exam Prep
- 🌐 3D interactive graph visualization
- 🔍 Expand nodes by scraping related information
- 🔐 User authentication with Supabase
- 🤖 AI-powered graph extraction using Google Gemini

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript, Three.js, 3D Force Graph
- **Backend**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **Storage**: Supabase Storage
- **AI**: Google Gemini API
- **Deployment**: Vercel

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd graph-learning-platform
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
GEMINI_API_KEY=your_google_gemini_api_key
```

### 4. Supabase Setup

Ensure your Supabase project has:

1. **Storage Bucket**: Create a public bucket named `documents`
2. **Database Tables**: 
   - `profiles` (for user profiles)
   - `documents` (for storing document metadata and graph data)
   - `user_projects` (optional, for project management)

### 5. Vercel Deployment

1. Push your code to GitHub
2. Import the project in Vercel
3. Add environment variables in Vercel:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `GEMINI_API_KEY`
4. Deploy!

**Important**: Make sure to add the environment variables in Vercel's project settings before deploying.

## Local Development

```bash
# Start frontend
npm run dev

# Start backend (in a separate terminal)
cd backend
uvicorn main:app --reload --port 8000
```

## Project Structure

```
graph-learning-platform/
├── api/                    # Vercel serverless functions
│   ├── index.py           # API entry point
│   └── requirements.txt   # Python dependencies
├── backend/               # Backend logic
│   ├── ai_engine.py      # AI graph extraction
│   ├── database.py       # Supabase database operations
│   ├── ocr_engine.py     # PDF text extraction
│   ├── scraper.py        # Web scraping for node expansion
│   └── main.py           # FastAPI application
├── src/                   # Frontend source
│   ├── css/              # Stylesheets
│   └── js/               # JavaScript modules
├── dashboard.html        # Main dashboard
├── index.html           # Landing page
├── login.html           # Login page
├── signup.html          # Signup page
└── vercel.json          # Vercel configuration
```

## Usage

1. **Sign up/Login**: Create an account or log in
2. **Upload Document**: Drag and drop a PDF file
3. **Select Study Mode**: Choose Research, General, or Exam Prep
4. **Generate Graph**: Click "Generate Graph" to process the document
5. **Explore**: Interact with the 3D graph, click nodes to expand them

## Troubleshooting

### 404 Error on Vercel

If you get a 404 error when clicking "Generate Graph":
- Ensure environment variables are set in Vercel
- Check that the `api` directory exists with `index.py`
- Verify `vercel.json` is properly configured

### Documents Stuck in "uploaded" Status

- Check Vercel function logs for errors
- Verify Gemini API key is valid
- Ensure Supabase storage bucket is accessible

## License

MIT
