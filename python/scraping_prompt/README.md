# Web Crawler API - Scraping Prompt Example

This example demonstrates how to use the Web Crawler API to scrape web content using a custom prompt. The example shows how to extract structured data from a webpage using natural language instructions.

## Prerequisites

- Python 3.6 or higher
- A Web Crawler API key (get one at [webcrawlerapi.com](https://webcrawlerapi.com))

## Setup

1. Install the required dependencies:
```bash
pip install python-dotenv webcrawlerapi
```

2. Create a `.env` file in the same directory with your API key:
```
WEBCRAWLERAPI_API_KEY=your_api_key_here
```

## Usage

The example script demonstrates how to:
1. Initialize the Web Crawler API client
2. Send a scraping request with a custom prompt
3. Handle the response and extract structured data

To run the example:
```bash
python scrape_prompt.py
```

## Code Explanation

The example uses the `scrape` method with a custom prompt to extract content from a webpage. The prompt instructs the API to:
- Extract the main content of the page
- Return the data in JSON format with an 'output' property

The response is then processed to either:
- Print the extracted content if successful
- Display any error messages if the request fails

## Customization

You can modify the example by:
- Changing the target URL
- Adjusting the prompt to extract different types of information
- Adding additional error handling or data processing

## Error Handling

The example includes basic error handling that displays:
- Error codes
- Error messages

## License

This example is provided under the MIT License.
