import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def scrape_topic(topic: str, depth: int = 1) -> str:
    """
    Scrapes information about a topic using requests and BeautifulSoup.
    """
    logger.info(f"Scraping topic: {topic}")
    
    try:
        # Example: Search Wikipedia
        search_url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
        response = requests.get(search_url)
        
        if response.status_code != 200:
            logger.warning(f"Failed to fetch {search_url}: {response.status_code}")
            return ""
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract paragraphs from the main content area
        content_div = soup.find(id="bodyContent")
        if not content_div:
            content_div = soup
            
        paragraphs = content_div.find_all('p')
        text = "\n".join([p.get_text() for p in paragraphs])
        
        return text[:10000] # Return first 10k chars
        
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        return ""
