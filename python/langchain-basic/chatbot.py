from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from webcrawlerapi_langchain import WebCrawlerAPILoader
import os
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

# Load environment variables
load_dotenv()
logger.debug("Environment variables loaded")


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


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
        
        # Generate filename with current date and time
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_filename = f"books-summary-{current_time}.txt"
        
        # Open output file for writing
        with open(output_filename, 'w', encoding='utf-8') as f:
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
                    
                    # Only process if it's a book page
                    if "Not a book detail page" not in result:
                        output = f"\n{'='*70}\n📚 Book Details\n{'='*70}\n{result}\n\n🔗 Link: {url}\n{'='*70}\n"
                        # Write to file
                        f.write(output)
                        # Print to console
                        print(output)
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