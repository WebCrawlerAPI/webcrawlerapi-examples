/**
 * Example usage of WebCrawlerAPI standalone client
 *
 * This example demonstrates how to use the WebCrawlerAPI class for:
 * 1. Crawling multiple pages from a website
 * 2. Scraping a single page (synchronous)
 * 3. Scraping a single page (asynchronous)
 */
public class Example {

    public static void main(String[] args) {
        // Get API key from environment variable or use a test key
        String apiKey = System.getenv("API_KEY");
        if (apiKey == null || apiKey.isEmpty()) {
            System.err.println("Error: API_KEY environment variable not set");
            System.err.println("Usage: API_KEY=your-api-key java Example");
            System.exit(1);
        }

        // Optional: override base URL for local testing
        String baseUrl = System.getenv("API_BASE_URL");
        WebCrawlerAPI client = baseUrl != null
            ? new WebCrawlerAPI(apiKey, baseUrl)
            : new WebCrawlerAPI(apiKey);

        try {
            System.out.println("=== WebCrawlerAPI Standalone Example ===\n");

            // Example 1: Crawl a website
            example1Crawl(client);

            printSeparator();

            // Example 2: Scrape a single page (synchronous)
            example2Scrape(client);

            printSeparator();

            // Example 3: Scrape asynchronously
            example3ScrapeAsync(client);

        } catch (WebCrawlerAPI.WebCrawlerAPIException e) {
            System.err.println("Error: " + e);
            System.exit(1);
        }
    }

    /**
     * Example 1: Crawl a website and extract markdown content
     */
    private static void example1Crawl(WebCrawlerAPI client) throws WebCrawlerAPI.WebCrawlerAPIException {
        System.out.println("Example 1: Crawling a website");
        System.out.println("------------------------------");

        String url = "https://books.toscrape.com";
        String scrapeType = "markdown";
        int itemsLimit = 5;

        System.out.println("URL: " + url);
        System.out.println("Scrape Type: " + scrapeType);
        System.out.println("Items Limit: " + itemsLimit);
        System.out.println("\nStarting crawl...");

        WebCrawlerAPI.CrawlResult result = client.crawl(url, scrapeType, itemsLimit);

        System.out.println("Crawl completed!");
        System.out.println("Job ID: " + result.id);
        System.out.println("Status: " + result.status);
        System.out.println("Items found: " + result.items.size());

        // Display first few items
        for (int i = 0; i < Math.min(3, result.items.size()); i++) {
            WebCrawlerAPI.CrawlItem item = result.items.get(i);
            System.out.println("\nItem " + (i + 1) + ":");
            System.out.println("  URL: " + item.url);
            System.out.println("  Status: " + item.status);
            System.out.println("  Content URL: " + item.getContentUrl(scrapeType));
        }

        if (result.items.size() > 3) {
            System.out.println("\n... and " + (result.items.size() - 3) + " more items");
        }
    }

    /**
     * Example 2: Scrape a single page synchronously
     */
    private static void example2Scrape(WebCrawlerAPI client) throws WebCrawlerAPI.WebCrawlerAPIException {
        System.out.println("Example 2: Scraping a single page (synchronous)");
        System.out.println("------------------------------------------------");

        String url = "https://books.toscrape.com";
        String scrapeType = "markdown";

        System.out.println("URL: " + url);
        System.out.println("Scrape Type: " + scrapeType);
        System.out.println("\nStarting scrape...");

        WebCrawlerAPI.ScrapeResult result = client.scrape(url, scrapeType);

        System.out.println("Scrape completed!");
        System.out.println("Status: " + result.status);
        System.out.println("URL: " + result.url);
        System.out.println("Page Status Code: " + result.pageStatusCode);

        // Display content preview
        if (result.content != null) {
            String preview = result.content.length() > 200
                ? result.content.substring(0, 200) + "..."
                : result.content;
            System.out.println("\nContent preview:");
            System.out.println(preview);
        }
    }

    /**
     * Example 3: Scrape a page asynchronously (start job and poll manually)
     */
    private static void example3ScrapeAsync(WebCrawlerAPI client) throws WebCrawlerAPI.WebCrawlerAPIException {
        System.out.println("Example 3: Scraping a page asynchronously");
        System.out.println("------------------------------------------");

        String url = "https://books.toscrape.com";
        String scrapeType = "html";

        System.out.println("URL: " + url);
        System.out.println("Scrape Type: " + scrapeType);
        System.out.println("\nStarting async scrape...");

        // Start the scrape job
        String scrapeId = client.scrapeAsync(url, scrapeType);
        System.out.println("Scrape started! ID: " + scrapeId);

        // Poll for completion (you could do other work here)
        System.out.println("Polling for completion...");
        WebCrawlerAPI.ScrapeResult result = null;
        int maxPolls = 20;

        for (int i = 0; i < maxPolls; i++) {
            result = client.getScrape(scrapeId);
            System.out.println("Poll " + (i + 1) + ": status = " + result.status);

            if ("done".equals(result.status) || "error".equals(result.status)) {
                break;
            }

            try {
                Thread.sleep(2000); // Wait 2 seconds between polls
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new WebCrawlerAPI.WebCrawlerAPIException("interrupted", "Polling interrupted");
            }
        }

        if (result != null && "done".equals(result.status)) {
            System.out.println("\nScrape completed!");
            System.out.println("Page Status Code: " + result.pageStatusCode);

            // Display HTML preview
            if (result.html != null) {
                String preview = result.html.length() > 200
                    ? result.html.substring(0, 200) + "..."
                    : result.html;
                System.out.println("\nHTML preview:");
                System.out.println(preview);
            }
        } else {
            System.out.println("Scrape did not complete within timeout");
        }
    }

    /**
     * Print a separator line (Java 17 compatible)
     */
    private static void printSeparator() {
        System.out.println();
        for (int i = 0; i < 50; i++) {
            System.out.print("=");
        }
        System.out.println("\n");
    }
}
