import requests
import json
import logging
from config import OPENROUTER_API_KEY

logger = logging.getLogger(__name__)

# OpenRouter API endpoint
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Free model options on OpenRouter
FREE_MODEL = "meta-llama/llama-3.2-3b-instruct:free"  # Free Llama model

def extract_graph(text_content: str) -> dict:
    """
    Extracts a knowledge graph from the provided text using OpenRouter API.
    Returns a JSON object with nodes and edges.
    """
    if not OPENROUTER_API_KEY:
        logger.error("OpenRouter API Key is missing.")
        return {"error": "API Key missing"}

    prompt = f"""You are an expert knowledge graph extractor. Analyze the following text and extract key concepts and their relationships.

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
{text_content[:30000]}"""

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://graph-learning-platform.vercel.app",  # Optional
            "X-Title": "Graph Learning Platform"  # Optional
        }
        
        payload = {
            "model": FREE_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 4000
        }
        
        logger.info(f"Calling OpenRouter API with model: {FREE_MODEL}")
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        response_text = result['choices'][0]['message']['content'].strip()
        
        # Clean up potential markdown formatting
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        logger.info(f"OpenRouter response received, parsing JSON...")
        graph_data = json.loads(response_text)
        
        # Validate structure
        if 'nodes' not in graph_data or 'edges' not in graph_data:
            logger.error("Invalid graph structure returned")
            return {"nodes": [], "edges": [], "error": "Invalid graph structure"}
        
        logger.info(f"Successfully extracted {len(graph_data['nodes'])} nodes and {len(graph_data['edges'])} edges")
        return graph_data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"OpenRouter API request failed: {e}")
        return {"nodes": [], "edges": [], "error": f"API request failed: {str(e)}"}
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response: {e}")
        logger.error(f"Response text: {response_text[:500]}")
        return {"nodes": [], "edges": [], "error": f"JSON parse error: {str(e)}"}
    except Exception as e:
        logger.error(f"AI Extraction failed: {e}")
        return {"nodes": [], "edges": [], "error": str(e)}

def process_scraped_data(text_content: str, parent_node_id: str) -> dict:
    """
    Analyzes scraped text to extend the graph from a parent node.
    """
    if not OPENROUTER_API_KEY:
        logger.error("OpenRouter API Key is missing.")
        return {"error": "API Key missing"}

    prompt = f"""You are an expert knowledge graph expander. I have a parent node with ID "{parent_node_id}".
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
{text_content[:30000]}"""

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://graph-learning-platform.vercel.app",
            "X-Title": "Graph Learning Platform"
        }
        
        payload = {
            "model": FREE_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 4000
        }
        
        logger.info(f"Calling OpenRouter API for scraped data with model: {FREE_MODEL}")
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        response_text = result['choices'][0]['message']['content'].strip()
        
        # Clean up potential markdown formatting
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        graph_data = json.loads(response_text)
        
        logger.info(f"Successfully processed scraped data: {len(graph_data.get('nodes', []))} new nodes")
        return graph_data
        
    except Exception as e:
        logger.error(f"AI Scraped Data Processing failed: {e}")
        return {"nodes": [], "edges": [], "error": str(e)}
