# Conference Hunter

Conference Hunter is an advanced, multi-threaded intelligence gathering tool engineered to extract, process, and visualize highly targeted biographical and professional data from over 100 distinct life sciences and biotechnology conference domains.

## Architecture and Core Engine

The application revolves around a centralized execution engine (`core/engine.py`) that handles job dispatching and spider routing.

- **Concurrent Execution Engine:** The engine utilizes a `ThreadPoolExecutor` to process multiple conference domains simultaneously, defaulting to 20 concurrent threads to maximize scraping throughput.
- **Dynamic Routing:** The system maps over 100 specific domains to specialized spider classes (e.g., `HansonWadeSpider`, `CHISpider`, `InformaSpider`, `ImmunoOncologySpider`). 
- **Archive Fallback Mechanism:** For domains that have been deprecated, taken offline, or present strict anti-bot mechanisms, the engine dynamically overrides the default spider and routes the request to a dedicated `ArchiveSpider` to extract historical data.
- **Incremental Data Persistence:** To prevent data loss during massive scraping operations, the engine flushes scraped results to an exporter incrementally as each thread completes.

## Spider Capabilities and Web Scraping Logic

The specialized spiders, such as the `HansonWadeSpider`, are built on top of Playwright and BeautifulSoup4, enabling deep DOM interaction and JavaScript execution.

- **Dynamic Link Discovery:** If explicit speaker directory URLs are unavailable, spiders traverse the DOM of the homepage, matching anchor tags against heuristic keywords to locate the speaker rosters.
- **Heuristic Text Extraction:** Spiders parse raw text blocks to heuristically identify event dates and locations, searching for specific date patterns and removing extraneous text.
- **Deep Profile Scraping:** The spiders navigate to individual speaker profiles to extract deep data points, including presentation titles, profile images, and extensive biographical summaries.
- **Data Cleansing:** The scraping logic incorporates a cleansing algorithm that strips out generic website boilerplate, cookie notices, and privacy policy text from the extracted biographies to maintain data integrity.
- **Intelligent Email Extraction:** Spiders employ a two-pass email discovery system. First, they scan the DOM for `mailto:` links and execute regular expressions over the raw text. Second, they run a proprietary validation algorithm (`is_valid_email`) that correlates extracted email prefixes and domains against the speaker's first name, last name, and company name to eliminate generic contact emails (e.g., info@, sales@) and output only highly probable direct contacts.

## Dashboard and Visualization

The extracted intelligence is presented through a Streamlit web application (`app.py`) designed with a strict, minimalist dark mode aesthetic.

- **Metric Tracking:** Real-time visibility into the volume of processed intelligence, including Total Speakers, Unique Companies, and Topics Covered.
- **Interactive Filtering:** Users can filter the underlying dataset by specific life-science topics or specific speaker companies.
- **Data Visualization:** Integrated with Plotly to render dynamic, interactive charts illustrating the distribution of the top represented companies.
- **Export Capabilities:** The dashboard allows users to export either the entire intelligence database or the currently filtered subset directly into standard Excel format using Pandas and OpenPyXL.

## Technical Specifications

- **Language:** Python 3
- **Browser Automation:** Playwright (Headless Chromium)
- **Data Structuring:** Pandas, OpenPyXL
- **Frontend Framework:** Streamlit
- **Visualization:** Plotly Express

## Installation and Execution

1. Clone the repository to the local environment.
2. Initialize a virtual environment and install the required packages:
   `pip install -r requirements.txt`
3. Install the required Playwright browser binaries:
   `playwright install`
4. Execute the scraping engine directly to rebuild the database:
   `python main.py`
5. Launch the analytical dashboard:
   `streamlit run app.py`

Programmed by Steve Zhelyazkov.
