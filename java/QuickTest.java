/**
 * Quick test to verify WebCrawlerAPI compilation and basic functionality
 */
public class QuickTest {
    public static void main(String[] args) {
        System.out.println("WebCrawlerAPI Standalone SDK - Quick Test");
        System.out.println("==========================================\n");

        // Test 1: Constructor
        System.out.println("Test 1: Creating client with API key...");
        try {
            WebCrawlerAPI client = new WebCrawlerAPI("test-key");
            System.out.println("✓ Client created successfully\n");
        } catch (Exception e) {
            System.err.println("✗ Failed: " + e.getMessage());
            System.exit(1);
        }

        // Test 2: Constructor with custom URL
        System.out.println("Test 2: Creating client with custom base URL...");
        try {
            WebCrawlerAPI client = new WebCrawlerAPI("test-key", "http://localhost:8080");
            System.out.println("✓ Client created with custom URL\n");
        } catch (Exception e) {
            System.err.println("✗ Failed: " + e.getMessage());
            System.exit(1);
        }

        // Test 3: Constructor with null API key (should fail)
        System.out.println("Test 3: Testing null API key validation...");
        try {
            WebCrawlerAPI client = new WebCrawlerAPI(null);
            System.err.println("✗ Should have thrown IllegalArgumentException");
            System.exit(1);
        } catch (IllegalArgumentException e) {
            System.out.println("✓ Correctly rejected null API key\n");
        } catch (Exception e) {
            System.err.println("✗ Unexpected exception: " + e.getMessage());
            System.exit(1);
        }

        // Test 4: Constructor with empty API key (should fail)
        System.out.println("Test 4: Testing empty API key validation...");
        try {
            WebCrawlerAPI client = new WebCrawlerAPI("");
            System.err.println("✗ Should have thrown IllegalArgumentException");
            System.exit(1);
        } catch (IllegalArgumentException e) {
            System.out.println("✓ Correctly rejected empty API key\n");
        } catch (Exception e) {
            System.err.println("✗ Unexpected exception: " + e.getMessage());
            System.exit(1);
        }

        // Test 5: Data classes instantiation
        System.out.println("Test 5: Testing data classes...");
        try {
            WebCrawlerAPI.CrawlResult crawlResult = new WebCrawlerAPI.CrawlResult();
            crawlResult.id = "test-id";
            crawlResult.status = "done";
            System.out.println("✓ CrawlResult: " + crawlResult);

            WebCrawlerAPI.CrawlItem crawlItem = new WebCrawlerAPI.CrawlItem();
            crawlItem.url = "https://books.toscrape.com";
            crawlItem.status = "done";
            System.out.println("✓ CrawlItem: " + crawlItem);

            WebCrawlerAPI.ScrapeResult scrapeResult = new WebCrawlerAPI.ScrapeResult();
            scrapeResult.status = "done";
            scrapeResult.url = "https://books.toscrape.com";
            System.out.println("✓ ScrapeResult: " + scrapeResult);

            WebCrawlerAPI.WebCrawlerAPIException exception =
                new WebCrawlerAPI.WebCrawlerAPIException("test_error", "Test message");
            System.out.println("✓ WebCrawlerAPIException: " + exception);

            System.out.println("✓ All data classes work correctly\n");
        } catch (Exception e) {
            System.err.println("✗ Failed: " + e.getMessage());
            System.exit(1);
        }

        // Test 6: CrawlItem helper method
        System.out.println("Test 6: Testing CrawlItem.getContentUrl()...");
        try {
            WebCrawlerAPI.CrawlItem item = new WebCrawlerAPI.CrawlItem();
            item.rawContentUrl = "http://example.com/raw";
            item.cleanedContentUrl = "http://example.com/cleaned";
            item.markdownContentUrl = "http://example.com/markdown";

            String htmlUrl = item.getContentUrl("html");
            String cleanedUrl = item.getContentUrl("cleaned");
            String markdownUrl = item.getContentUrl("markdown");

            if (!"http://example.com/raw".equals(htmlUrl)) {
                throw new Exception("HTML URL mismatch");
            }
            if (!"http://example.com/cleaned".equals(cleanedUrl)) {
                throw new Exception("Cleaned URL mismatch");
            }
            if (!"http://example.com/markdown".equals(markdownUrl)) {
                throw new Exception("Markdown URL mismatch");
            }

            System.out.println("✓ getContentUrl() works correctly\n");
        } catch (Exception e) {
            System.err.println("✗ Failed: " + e.getMessage());
            System.exit(1);
        }

        System.out.println("==========================================");
        System.out.println("All tests passed! ✓");
        System.out.println("\nThe SDK is ready to use.");
        System.out.println("\nTo test with the API, run:");
        System.out.println("  API_KEY=your-key java -cp bin Example");
    }
}
