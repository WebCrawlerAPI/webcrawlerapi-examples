# WebCrawlerAPI Java Examples

This directory contains examples demonstrating how to use the WebCrawlerAPI Standalone Java SDK.

## Prerequisites

- Java 17 or newer
- WebCrawlerAPI API key ([get one here](https://webcrawlerapi.com))

## Available Examples

### 1. Basic Example (`Example.java`)

Comprehensive example demonstrating all main SDK features:
- **Crawling**: Crawl multiple pages from a website with markdown extraction
- **Synchronous Scraping**: Scrape a single page and wait for results
- **Asynchronous Scraping**: Start a scrape job and poll for completion manually

### 2. Quick Test (`QuickTest.java`)

A simple test to verify the SDK compiles and basic functionality works:
- Constructor validation
- Data class instantiation
- Helper method testing

## Running the Examples

### Method 1: Using the Compilation Script

The easiest way to run the examples:

```bash
# Basic example with production API
API_KEY=your-api-key ./compile-and-run.sh

# Test with local development server
API_KEY=test-api-key API_BASE_URL=http://localhost:8080 ./compile-and-run.sh
```

### Method 2: Manual Compilation

If you prefer to compile and run manually:

```bash
# Create bin directory
mkdir -p bin

# Copy the SDK file to the current directory
cp ../../java/standalone-sdk/WebCrawlerAPI.java .

# Compile all Java files
javac *.java -d bin

# Run the basic example
API_KEY=your-api-key java -cp bin Example

# Or run the quick test
java -cp bin QuickTest
```

## Example Output

### Basic Example

```
=== WebCrawlerAPI Standalone Example ===

Example 1: Crawling a website
------------------------------
URL: https://books.toscrape.com
Scrape Type: markdown
Items Limit: 5

Starting crawl...
Crawl completed!
Job ID: 123e4567-e89b-12d3-a456-426614174000
Status: done
Items found: 5

Item 1:
  URL: https://books.toscrape.com/
  Status: done
  Content URL: https://api.webcrawlerapi.com/storage/...

... and 4 more items
```

### Quick Test

```
WebCrawlerAPI Standalone SDK - Quick Test
==========================================

Test 1: Creating client with API key...
✓ Client created successfully

Test 2: Creating client with custom base URL...
✓ Client created with custom URL

Test 3: Testing null API key validation...
✓ Correctly rejected null API key

...

All tests passed! ✓
```

## Environment Variables

- `API_KEY` (required): Your WebCrawlerAPI key
- `API_BASE_URL` (optional): Override the base URL for local testing (default: `https://api.webcrawlerapi.com`)

## SDK Features Demonstrated

### Crawling

```java
WebCrawlerAPI client = new WebCrawlerAPI(apiKey);
CrawlResult result = client.crawl("https://example.com", "markdown", 10);

System.out.println("Found " + result.items.size() + " items");
for (CrawlItem item : result.items) {
    System.out.println("URL: " + item.url);
    System.out.println("Content: " + item.getContentUrl("markdown"));
}
```

### Synchronous Scraping

```java
ScrapeResult result = client.scrape("https://example.com", "markdown");
System.out.println("Content: " + result.content);
```

### Asynchronous Scraping

```java
// Start the job
String scrapeId = client.scrapeAsync("https://example.com", "html");

// Poll for completion
ScrapeResult result;
do {
    result = client.getScrape(scrapeId);
    Thread.sleep(2000);
} while (!"done".equals(result.status) && !"error".equals(result.status));

System.out.println("HTML: " + result.html);
```

## Scrape Types

The SDK supports three content extraction types:

- `"html"`: Raw HTML content
- `"cleaned"`: Cleaned text content
- `"markdown"`: Markdown-formatted content

## Error Handling

All API methods throw `WebCrawlerAPIException`:

```java
try {
    CrawlResult result = client.crawl("https://example.com", "markdown", 5);
} catch (WebCrawlerAPI.WebCrawlerAPIException e) {
    System.err.println("Error code: " + e.getErrorCode());
    System.err.println("Error message: " + e.getMessage());
}
```

## Learn More

- [WebCrawlerAPI Documentation](https://docs.webcrawlerapi.com)
- [Java Standalone SDK](../../java/standalone-sdk)
- [Get API Key](https://webcrawlerapi.com)
