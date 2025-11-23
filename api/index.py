from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Add parent directory to path to import backend modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.database import get_document_metadata, update_document_status, save_graph_data, supabase
from backend.ocr_engine import process_document
from backend.ai_engine import extract_graph, process_scraped_data
from backend.scraper import scrape_topic

app = FastAPI()

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProcessRequest(BaseModel):
    document_id: str

class ScrapeRequest(BaseModel):
    document_id: str
    node_id: str
    topic: str

@app.get("/")
@app.get("/api")
def root():
    return {"status": "ok", "message": "Graph Learning Platform API"}

@app.get("/health")
@app.get("/api/health")
def health_check():
    return {"status": "ok"}

async def background_processing(doc_id: str):
    print(f"Starting processing for document {doc_id}")
    try:
        update_document_status(doc_id, "processing")
        
        # 1. Fetch document path from Supabase
        meta = get_document_metadata(doc_id)
        if not meta:
            print(f"Document {doc_id} not found")
            update_document_status(doc_id, "failed")
            return

        file_path = f"/tmp/temp_{doc_id}.pdf"
        try:
            # Download file from Supabase Storage
            print(f"Downloading file from storage: {meta['file_path']}")
            res = supabase.storage.from_("documents").download(meta['file_path'])
            with open(file_path, 'wb') as f:
                f.write(res)
            print(f"Downloaded file to {file_path}")
        except Exception as e:
            print(f"Failed to download file: {e}")
            update_document_status(doc_id, "failed")
            return 
        
        # 2. OCR
        print("Extracting text from document...")
        text_content = process_document(file_path)
        
        if not text_content or len(text_content.strip()) < 50:
            print("Insufficient text extracted from document")
            update_document_status(doc_id, "failed")
            return
        
        # 3. AI Extraction
        print("Generating knowledge graph with AI...")
        graph_data = extract_graph(text_content)
        
        if not graph_data or "error" in graph_data:
            print(f"AI extraction failed: {graph_data.get('error', 'Unknown error')}")
            update_document_status(doc_id, "failed")
            return
        
        # 4. Save
        print("Saving graph data...")
        save_graph_data(doc_id, graph_data)
        
        print(f"Finished processing for document {doc_id}")
        update_document_status(doc_id, "completed")
        
    except Exception as e:
        print(f"Error processing document {doc_id}: {e}")
        import traceback
        traceback.print_exc()
        update_document_status(doc_id, "failed")

@app.post("/process")
@app.post("/api/process")
async def process_document_endpoint(request: ProcessRequest):
    # Verify document exists
    meta = get_document_metadata(request.document_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Run synchronously for Vercel Serverless
    await background_processing(request.document_id)
    
    return {"message": "Processing completed", "document_id": request.document_id}

@app.post("/scrape")
@app.post("/api/scrape")
async def scrape_endpoint(request: ScrapeRequest):
    try:
        # 1. Scrape
        print(f"Scraping topic: {request.topic}")
        scraped_text = scrape_topic(request.topic)
        
        if not scraped_text:
            raise HTTPException(status_code=500, detail="Failed to scrape content")
        
        # 2. Process with AI
        print("Processing scraped data...")
        new_graph_data = process_scraped_data(scraped_text, request.node_id)
        
        # 3. Update Graph (Merge logic)
        current_meta = get_document_metadata(request.document_id)
        current_graph = current_meta.get('graph_data', {'nodes': [], 'edges': []})
        
        # Simple merge
        current_graph['nodes'].extend(new_graph_data.get('nodes', []))
        current_graph['edges'].extend(new_graph_data.get('edges', []))
        
        save_graph_data(request.document_id, current_graph)
        
        return {"message": "Scraping and update completed", "new_nodes": len(new_graph_data.get('nodes', []))}
        
    except Exception as e:
        print(f"Scraping failed: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# This is required for Vercel
handler = app
