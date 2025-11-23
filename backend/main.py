from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import get_document_metadata, update_document_status, save_graph_data, supabase
from ocr_engine import process_document
from ai_engine import extract_graph, process_scraped_data
from scraper import scrape_topic

app = FastAPI()
router = APIRouter()

# CORS Setup
origins = [
    "http://localhost:5173", # Vite default
    "http://127.0.0.1:5500", # Live Server default
    "*" # Allow all for development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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

@router.get("/health")
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
            return

        file_path = f"/tmp/temp_{doc_id}.pdf" # Use /tmp for Vercel
        try:
            # Download file from Supabase Storage
            # Assuming bucket name is 'documents' and path is stored in meta['file_path']
            with open(file_path, 'wb') as f:
                res = supabase.storage.from_("documents").download(meta['file_path'])
                f.write(res)
            print(f"Downloaded file to {file_path}")
        except Exception as e:
            print(f"Failed to download file: {e}")
            update_document_status(doc_id, "failed_download")
            return 
        
        # 2. OCR
        text_content = process_document(file_path)
        
        # 3. AI Extraction
        graph_data = extract_graph(text_content)
        
        # 4. Save
        save_graph_data(doc_id, graph_data)
        
        print(f"Finished processing for document {doc_id}")
        update_document_status(doc_id, "completed")
        
    except Exception as e:
        print(f"Error processing document {doc_id}: {e}")
        update_document_status(doc_id, "failed")

@router.post("/process")
async def process_document_endpoint(request: ProcessRequest):
    # Verify document exists
    meta = get_document_metadata(request.document_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Run synchronously for Vercel Serverless
    await background_processing(request.document_id)
    
    return {"message": "Processing completed", "document_id": request.document_id}

@router.post("/scrape")
async def scrape_endpoint(request: ScrapeRequest):
    try:
        # 1. Scrape
        print(f"Scraping topic: {request.topic}")
        scraped_text = scrape_topic(request.topic)
        
        # 2. Process with AI
        print("Processing scraped data...")
        new_graph_data = process_scraped_data(scraped_text, request.node_id)
        
        # 3. Update Graph (Merge logic needed, for now just returning new data)
        # In a real app, we would fetch existing graph, merge, and save back.
        # For now, we'll append to the document's graph data in Supabase
        
        current_meta = get_document_metadata(request.document_id)
        current_graph = current_meta.get('graph_data', {'nodes': [], 'edges': []})
        
        # Simple merge
        current_graph['nodes'].extend(new_graph_data.get('nodes', []))
        current_graph['edges'].extend(new_graph_data.get('edges', []))
        
        save_graph_data(request.document_id, current_graph)
        
        return {"message": "Scraping and update completed", "new_nodes": len(new_graph_data.get('nodes', []))}
        
    except Exception as e:
        print(f"Scraping failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Include router for both root and /api paths to handle Vercel rewrites and localhost
app.include_router(router)
app.include_router(router, prefix="/api")
