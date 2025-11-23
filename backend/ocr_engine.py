import logging
import pypdf

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_document(file_path: str) -> str:
    """
    Process a document (PDF) to extract text using pypdf.
    Returns the extracted text content.
    """
    try:
        logger.info(f"Attempting to process {file_path} with pypdf...")
        reader = pypdf.PdfReader(file_path)
        text_content = ""
        
        for page in reader.pages:
            text_content += page.extract_text() + "\n"
            
        if not text_content or len(text_content.strip()) < 50:
            logger.warning("pypdf extracted insufficient text.")
            # Fallback or just return what we have
            
        logger.info("pypdf processing successful.")
        return text_content

    except Exception as e:
        logger.error(f"pypdf failed: {e}")
        return ""
