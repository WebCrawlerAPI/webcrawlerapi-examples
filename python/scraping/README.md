# Web Crawler API Python Example

[WebcrawlerAPI](https://webcrawlerapi.com) helps to convert website and pages into LLM and AI ready data.
This example demonstrates basic usage of the WebCrawlerAPI to scrape webpage content in markdown format.

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

The example script (`scrape.py`) demonstrates how to:
- Initialize the Web Crawler API client
- Scrape a single webpage
- Get the content in markdown format

To run the example:
```bash
python scrape.py
```

## Example Output

The script will output:
- The scraped content in markdown format if successful
- Error code and message if the scraping fails

## Error Handling

The script includes basic error handling and will display:
- Success status
- Error code and message if the scraping fails

## License

This example is provided under the MIT License.
