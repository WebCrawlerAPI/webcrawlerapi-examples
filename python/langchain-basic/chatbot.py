from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('chatbot.log')
    ]
)
logger = logging.getLogger(__name__)

# Add the local webcrawlerapi-langchain package to Python path
REPO_ROOT = Path("/Users/andrey/Projects/own/supcop/sdk/python")
sys.path.append(str(REPO_ROOT / "webcrawlerapi-langchain"))

logger.info(f"Added webcrawlerapi-langchain to Python path")

from webcrawlerapi_langchain import WebCrawlerAPILoader
from langchain_core.documents import Document

# Load environment variables
load_dotenv()
logger.debug("Environment variables loaded")

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def load_local_data():
    """Load data from local file"""
    logger.debug("Attempting to load local data from data/bubble_io_data.json")
    file_path = "data/bubble_io_data.json"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.debug(f"Successfully loaded {len(data)} items from local data")
            return [Document(
                page_content=item["page_content"],
                metadata=item["metadata"]
            ) for item in data]
    except FileNotFoundError:
        logger.info("Local data file not found. Will crawl for new data.")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in {file_path}: {str(e)}. Deleting corrupted file.", exc_info=True)
        try:
            os.remove(file_path)
            logger.info(f"Deleted corrupted file: {file_path}")
        except OSError as remove_error:
            logger.error(f"Error deleting corrupted file {file_path}: {remove_error}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error loading local data from {file_path}: {str(e)}", exc_info=True)
        return None

# Test data
DATA = """
This is a test dataset about artificial intelligence.
AI is a broad field of computer science focused on creating intelligent machines.
Machine learning is a subset of AI that enables systems to learn from data.
Deep learning is a type of machine learning that uses neural networks with multiple layers.
Natural Language Processing (NLP) is another important area of AI that deals with understanding human language.
"""

def create_extraction_chain():
    """Create a chain for extracting book information"""
    logger.info("Creating extraction chain")
    try:
        model = ChatOpenAI(
            model="gpt-4o-mini", 
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        logger.info("ChatOpenAI model initialized")
        
        prompt = ChatPromptTemplate.from_template("""
        You are analyzing a page from books.toscrape.com. Extract book information ONLY if this is a single book's detail page.

        Page Metadata:
        URL: {url}
        Title: {title}
        Status Code: {status_code}

        Rules for identifying a book detail page:
        1. The page should contain detailed information about exactly ONE book
        2. Skip if it's a category page, catalog page, or any page listing multiple books
        3. The page should have specific details like price, availability, and product description
        4. The URL should contain '/catalogue/' and end with a specific book identifier
        
        If these criteria are met, extract:
        - Book Title (the main title of the single book)
        - Price (the current price, including currency symbol)
        - Description (the product description or synopsis of the book)
        
        If this is NOT a single book's detail page, respond ONLY with:
        "Not a book detail page"

        Content: {content}
        
        Format your response EXACTLY as:
        Title: <the exact book title>
        Price: <the exact price with currency>
        Description: <the book's description>

        OR just "Not a book detail page" if criteria not met.
        """)
        
        chain = prompt | model | StrOutputParser()
        logger.info("Extraction chain created")
        return chain
    except Exception as e:
        logger.error(f"Error creating extraction chain: {str(e)}", exc_info=True)
        raise

def process_documents():
    """Process documents using lazy loading"""
    logger.info("Starting document processing with lazy loading")
    try:
        loader = WebCrawlerAPILoader(
            url="https://books.toscrape.com",
            api_key=os.getenv("WEBCRAWLERAPI_API_KEY"),
            whitelist_regexp="/catalogue/.*",
            blacklist_regexp="/catalogue/category/.*",
            scrape_type="markdown",
            items_limit=20,
            allow_subdomains=True
        )
        logger.info("WebCrawlerAPILoader initialized")
        
        # Create extraction chain
        chain = create_extraction_chain()
        
        # Process documents as they are loaded
        for doc in loader.lazy_load():
            url = doc.metadata.get('url', 'Unknown URL')
            logger.info(f"Processing document: {url}")
            try:
                # Extract information using the chain with metadata
                result = chain.invoke({
                    "content": doc.page_content,
                    "url": doc.metadata.get('url', 'Unknown URL'),
                    "title": doc.metadata.get('title', 'No title'),
                    "status_code": doc.metadata.get('status_code', 'Unknown')
                })
                
                # Only display if it's a book page
                if "Not a book detail page" not in result:
                    print("\n" + "="*70)
                    print(f"📚 Book Details")
                    print("="*70)
                    print(result)
                    print(f"\n🔗 Link: {url}")
                    print("="*70)
                else:
                    logger.info(f"Skipping non-book page: {url}")
            except Exception as e:
                logger.error(f"Error processing document: {str(e)}", exc_info=True)
                continue
            
    except Exception as e:
        logger.error(f"Error in process_documents: {str(e)}", exc_info=True)
        raise

def main():
    logger.info("Starting Book Information Extractor")
    print("Welcome to the Book Information Extractor!")
    print("Processing book pages from books.toscrape.com...\n")
    
    try:
        process_documents()
    except Exception as e:
        logger.error(f"Error in main loop: {str(e)}", exc_info=True)
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main() 