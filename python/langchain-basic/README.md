# Book Information Extractor with LangChain and WebcrawlerAPI

This example demonstrates a web scraping application built with LangChain that extracts detailed book information from [books.toscrape.com](https://books.toscrape.com). The application showcases how to combine web crawling, LLM-based information extraction, and structured data processing.

## Features

- Web crawling with selective URL filtering (whitelist/blacklist patterns)
- Intelligent book information extraction using `gpt-4o-mini`
- Lazy loading of documents for efficient memory usage
- Structured logging with both console and file output
- Error handling and corrupt data management
- Environment variable configuration

## What it Does

The application:
1. Crawls the books.toscrape.com website, focusing on individual book pages
2. Uses LangChain and GPT-4 to extract specific information from each book page:
   - Book Title
   - Price
   - Description
3. Filters out non-book pages (like category listings)
4. Provides formatted output of the extracted information

## Requirements

```
langchain-core
langchain-openai
python-dotenv
webcrawlerapi-langchain
```

## How to Run

1. Clone the repository and navigate to the project directory:
```bash
cd python/langchain-basic
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project directory and add your API keys:
```bash
OPENAI_API_KEY=your_openai_api_key
WEBCRAWLERAPI_API_KEY=your_webcrawlerapi_key
```

5. Run the script:
```bash
python chatbot.py
```

## Output

The script outputs formatted book information to the console and maintains a detailed log file (`chatbot.log`) for debugging and monitoring.

Example output format:
```
======================================================================
📚 Book Details
======================================================================
Title: [Book Title]
Price: [Price with currency]
Description: [Book description]

🔗 Link: [Book URL]
======================================================================
```

## Error Handling

The application includes robust error handling for:
- JSON data corruption
- API failures
- Network issues
- Invalid document processing

All errors are logged with appropriate detail levels for debugging.