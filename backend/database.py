from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_document_metadata(doc_id: str):
    response = supabase.table("documents").select("*").eq("id", doc_id).execute()
    if response.data:
        return response.data[0]
    return None

def update_document_status(doc_id: str, status: str):
    supabase.table("documents").update({"status": status}).eq("id", doc_id).execute()

def save_graph_data(doc_id: str, graph_data: dict):
    # Assuming a 'graphs' table or storing in 'documents'
    # For now, let's assume we update the document with the graph data
    supabase.table("documents").update({"graph_data": graph_data, "status": "processed"}).eq("id", doc_id).execute()
