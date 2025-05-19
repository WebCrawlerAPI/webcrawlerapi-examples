import os
from dotenv import load_dotenv

from webcrawlerapi import WebCrawlerAPI

# Load environment variables from .env file
load_dotenv()

def main():
    api_key = os.getenv("WEBCRAWLERAPI_API_KEY")

    crawler = WebCrawlerAPI(api_key=api_key)
    job = crawler.crawl(
        url="https://books.toscrape.com/",  # Replace with your target website
        scrape_type="markdown",
        items_limit=10,
    )

    print(f"\nJob completed with status: {job.status}")
    print(f"Crawled URL: {job.url}")
    print(f"Created at: {job.created_at}")
    print(f"Number of items: {len(job.job_items)}")

    # Print the crawled content
    for item in job.job_items:
        print(f"\nPage: {item.title}")
        print(f"URL: {item.original_url}")
        print(f"Item status: {item.status}")
        print(f"Error code: {item.error_code}")

        content = item.content
        if content:
            print(f"Content preview: {content[:100]}")
        else:
            print("Content not available or item not done")

if __name__ == "__main__":
    main() 