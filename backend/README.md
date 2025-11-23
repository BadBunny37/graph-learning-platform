# Graph Learning Platform - Backend

This directory contains the Python backend for the Graph Learning Platform.

## Prerequisites

- Python 3.9+
- Pip
- Supabase Project
- Gemini API Key

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: You may need to install system dependencies for `paddlepaddle` and `playwright`.*
    ```bash
    playwright install
    ```

2.  **Environment Variables**:
    Create a `.env` file in this directory (or ensure `config.py` can read them) with:
    ```
    SUPABASE_URL=your_supabase_url
    SUPABASE_KEY=your_supabase_key
    GEMINI_API_KEY=your_gemini_key
    ```

## Running the Server

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The server will run at `http://127.0.0.1:8000`.

## API Endpoints

-   `POST /process`: Trigger document processing.
    -   Body: `{"document_id": "your_doc_id"}`
-   `GET /health`: Health check.

## Modules

-   `main.py`: Entry point and API routes.
-   `ocr_engine.py`: Handles PDF processing using Docling and PaddleOCR.
-   `ai_engine.py`: Interact with Gemini for graph extraction.
-   `scraper.py`: Web scraping using Playwright.
-   `database.py`: Supabase interactions.
