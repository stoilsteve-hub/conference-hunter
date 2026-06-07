# Conference Hunter

Conference Hunter is a data extraction tool designed to collect biographical and professional data from life sciences and biotechnology conference websites.

## Architecture and Extraction Engine

The application uses `google-genai` (Gemini 2.5 Flash) to parse raw DOM text and extract structured speaker data in JSON format.

- **LLM Integration:** Sends extracted website text to Gemini 2.5 Flash with a JSON schema to identify speaker names, titles, companies, and biographies.
- **Retry Mechanism:** Uses a 6-strike exponential backoff system to handle 503 Service Unavailable errors and API rate limits.
- **Concurrent Execution:** Uses `ThreadPoolExecutor` to process multiple conference URLs concurrently.

## Scraping Capabilities

The system includes specific spiders for different website structures:

- **JS-Aware Scraping:** Uses Playwright with a `networkidle` state and a 2.5-second timeout to allow JavaScript frameworks (React/Angular) to render dynamic content before extraction.
- **Archive Scraping (Wayback Machine):** Uses the `archive.org/wayback/available` API to retrieve historical snapshots for URLs that return 404 errors or have deleted speaker data.
- **Data Pruning:** Removes non-speaker entries such as "Coffee Break" or "Registration" using AI text classification.

## Data Validation

Data integrity is maintained through programmatic and AI checks:

- **Column Validation:** Scans the dataset for structural errors (e.g., biographies placed in the company column) and re-sorts the data into the correct schema.
- **Cell-by-Cell Audit:** Feeds the extracted rows back into the Gemini LLM to verify that each cell contains the correct type of data according to the schema.

## Dashboard and Visualization

The data is presented using a Streamlit web application (`app.py`).

- **Metrics:** Displays total speakers, unique companies, and topics.
- **Filtering:** Allows filtering by specific topics or companies.
- **Visualization:** Uses Plotly to render charts showing company distribution.
- **Exporting:** Allows exporting the dataset to an Excel file using Pandas.

## Technical Specifications

- **Language:** Python 3
- **LLM API:** Google Gemini 2.5 Flash API (`google-genai`)
- **Browser Automation:** Playwright (Headless Chromium)
- **Data Handling:** Pandas, OpenPyXL
- **Frontend:** Streamlit
- **Visualization:** Plotly Express

## Installation and Usage

1. Clone the repository.
2. Create a virtual environment and install dependencies:
   `pip install -r requirements.txt`
3. Install Playwright browser binaries:
   `playwright install`
4. Set your Google Gemini API Key:
   `export GEMINI_API_KEY="your_api_key_here"`
5. Run the scraping engine:
   `python main.py`
6. Run the dashboard:
   `streamlit run app.py`

Programmed by Steve Zhelyazkov.
