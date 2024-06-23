# FastAPI Scraper Project

This project is a FastAPI-based web scraping tool designed to scrape product information from a target website and store it locally. The tool includes optional settings for limiting the number of pages to scrape and using a proxy.

## Features

- Scrapes product name, price, and image from the target website.
- Supports limiting the number of pages to scrape.
- Supports using a proxy for scraping.
- Stores scraped data in a local JSON file.
- Notifies the number of scraped products at the end of the scraping cycle.
- Simple token-based authentication for the API.
- Caching mechanism to avoid updating unchanged product prices.

## Setup Instructions

### Prerequisites

- Python 3.8 or later (Used 3.9 for development)
- pip (Python package installer)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/sdshone/fastapi-scraper.git
   cd fastapi-scraper
   ```
2. **Create and activate a virtual environment**

   ```bash
   python3.9 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install the required packages**

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the FastAPI server**

    ```bash
    uvicorn main:app --reload
    ```

2. **Access the API documentation**


    ```bash
    Open your browser and go to http://127.0.0.1:8000/docs to view the interactive API documentation.
    ```

### Testing the Scrape API

1. **Send a POST request to the /scrape endpoint**

    You can use tools like curl, httpie, or Postman to send a request. Here's an example using curl:

    ```bash
    curl -X POST "http://127.0.0.1:8000/scrape" \
     -H "Content-Type: application/json" \
     -H "x-token: secret-token" \
     -d '{"pages": 5, "proxy": "http://yourproxy.com"}'

    ```
    The body of the request should include the following JSON:

    ```json
    {
    "pages": 5,
    "proxy": "http://yourproxy.com"
    }
    ```
    If you do not need to use a proxy, you can omit the proxy field:

    ```json
    {
    "pages": 5
    }
    ```

