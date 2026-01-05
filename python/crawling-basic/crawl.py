import os
from dotenv import load_dotenv

from webcrawlerapi import WebCrawlerAPI

# Load environment variables from .env file
load_dotenv()

def main():
    api_key = os.getenv("WEBCRAWLERAPI_API_KEY")

    test_urls = [
        "https://shop.interface.com/US/en-US/carpet-tile/detours/7962C.html"
    ]

    webcrawler = WebCrawlerAPI(api_key=api_key)

    print("Testing webcrawler...")

    for url in test_urls:
        result = webcrawler.crawl(
            url=url,
            scrape_type="markdown",
            items_limit=3)

        print(result)

if __name__ == "__main__":
    main() 