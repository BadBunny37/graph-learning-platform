import google.generativeai as genai
import json
import logging
from config import GEMINI_API_KEY

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

logger = logging.getLogger(__name__)

def extract_graph(text_content: str) -> dict:
    """
    Extracts a knowledge graph from the provided text using Gemini.
    Returns a JSON object with nodes and edges.
    """
    if not GEMINI_API_KEY:
        logger.error("Gemini API Key is missing.")
        return {"error": "API Key missing"}

    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are an expert knowledge graph extractor. Analyze the following text and extract key concepts and their relationships.
    
    Output the result strictly in the following JSON format:
    {{
        "nodes": [
            {{ "id": "concept_1", "label": "Concept Name", "description": "Brief description", "level": 1 }}
        ],
        "edges": [
            {{ "source": "concept_1", "target": "concept_2", "relation": "related_to" }}
        ]
    }}
    
    Ensure the JSON is valid and parseable. Do not include markdown formatting like ```json.
    
    Text content:
    {text_content[:30000]}  # Truncate to avoid token limits if necessary
    """
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean up potential markdown formatting
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        graph_data = json.loads(response_text)
        return graph_data
    except Exception as e:
        logger.error(f"AI Extraction failed: {e}")
        return {"nodes": [], "edges": [], "error": str(e)}

def process_scraped_data(text_content: str, parent_node_id: str) -> dict:
    """
    Analyzes scraped text to extend the graph from a parent node.
    """
    if not GEMINI_API_KEY:
        logger.error("Gemini API Key is missing.")
        return {"error": "API Key missing"}

    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are an expert knowledge graph expander. I have a parent node with ID "{parent_node_id}".
    Analyze the following text (scraped from a source related to this node) and identify sub-concepts, details, and related topics to expand the graph.
    
    Output the result strictly in the following JSON format:
    {{
        "nodes": [
            {{ "id": "unique_id", "label": "Concept Name", "description": "Brief description", "level": 2 }}
        ],
        "edges": [
            {{ "source": "{parent_node_id}", "target": "unique_id", "relation": "related_to" }},
            {{ "source": "unique_id_1", "target": "unique_id_2", "relation": "related_to" }}
        ]
    }}
    
    Ensure the JSON is valid and parseable. Do not include markdown formatting.
    
    Text content:
    {text_content[:30000]}
    """
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        graph_data = json.loads(response_text)
        return graph_data
    except Exception as e:
        logger.error(f"AI Scraped Data Processing failed: {e}")
        return {"nodes": [], "edges": [], "error": str(e)}
