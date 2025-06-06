import os
from dotenv import load_dotenv

from webcrawlerapi import WebCrawlerAPI

# Load environment variables from .env file
load_dotenv()

def main():
    api_key = os.getenv("WEBCRAWLERAPI_API_KEY")

    crawler = WebCrawlerAPI(api_key=api_key)
    response = crawler.scrape(
        url="https://webcrawlerapi.com",
        prompt="Extract the main content of the page and return it in JSON 'output' property" 
    )
    if response.success:
        print(response.structured_data["output"])
    else:
        print(f"Code: {response.error_code} Error: {response.error_message}")

if __name__ == "__main__":
    main() 