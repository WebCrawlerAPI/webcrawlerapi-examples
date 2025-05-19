# Web Crawler API Python Example

[WebcrawlerAPI](https://webcrawlerapi.com) helps to convert website into LLM and AI ready data.
This example demonstrates basic usage of the WebCrawlerAPI to crawl websites and extract content in markdown format.

## Prerequisites

- Python 3.6 or higher
- A Web Crawler API key

Get your [API key](https://webcrawlerapi.com/docs/access-key) first.

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the project directory
2. Add your Web Crawler API key:
```
WEBCRAWLERAPI_API_KEY=your_api_key_here
```

## Usage

The example script (`crawl.py`) demonstrates how to:
- Initialize the Web Crawler API client
- Start a crawling job
- Process and display the results

To run the example:
```bash
python crawl.py
```

## Example Output

The script will output:
- Job status
- Crawled URL
- Creation timestamp
- Number of items crawled
- For each crawled page:
  - Page title
  - Original URL
  - Item status
  - Error code (if any)
  - Content preview

## Customization

You can modify the following parameters in `crawl.py`:
- `url`: The target website to crawl
- `scrape_type`: The format of the extracted content (e.g., "markdown")
- `items_limit`: Maximum number of pages to crawl

## Error Handling

The script includes basic error handling and will display:
- Job status
- Individual item status
- Error codes for failed items

## License

This example is provided under the MIT License.
