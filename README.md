# WebScraper Project

## Overview
The **TenderScraper** project is a robust solution designed to automate the extraction and management of tender data from the BHEL website. It incorporates web scraping using Selenium, database interaction for storing and updating tenders, and a Streamlit-based user interface for data visualization and downloads.

--------------------------------------------------------------------------------------------------------------------------

## Project Structure
```plaintext
WebScraper/
│
├── database/
│   ├── connection.py           # Database connection and query functions
│   ├── crud_operations.py      # Insert, update, fetch operations for SQL
│
├── scraper/
│   ├── web_scraper.py          # Web scraping logic using Selenium
│   ├── captcha_generator.py    # CAPTCHA generation utility
│
├── main.py                     # Entry point for the application
├── requirements.txt            # Python dependencies
└── .env                        # Environment variables
```

--------------------------------------------------------------------------------------------------------------------------

## Features
1. **Web Scraping:**
   - Automated data extraction from the BHEL website using Selenium.
   - Captures tender details, including bid submission closing dates, tender titles, reference numbers, tender IDs, and publication dates.

2. **Database Integration:**
   - Uses a SQL Server database to store and manage tenders.
   - Implements `insert`, `update`, and `fetch` operations to maintain data consistency.

3. **Streamlit UI:**
   - Interactive dashboard for scraping initiation and data visualization.
   - Enables downloading tender data in CSV format for further use.

--------------------------------------------------------------------------------------------------------------------------

## Installation
### Prerequisites
- Python 3.8 or later
- Selenium WebDriver
- SQL Server
- Streamlit
- Google Chrome (with Chromedriver)

### Steps
1. Clone the repository:
   ```bash
   git clone "https://github.com/your-repo/webscraper.git"
   cd webscraper
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the `.env` file with the following keys:
   ```plaintext
   DB_SERVER=<your_database_server>
   DB_NAME=<your_database_name>
   DB_DRIVER={ODBC Driver 17 for SQL Server}
   DB_TRUSTED_CONNECTION=Yes
   CHROMEDRIVER_PATH=<path_to_chromedriver>
   BHEL_URL="https://eprocurebhel.co.in/nicgep/app?page=FrontEndLatestActiveTenders&service=page"
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run main.py
   ```

--------------------------------------------------------------------------------------------------------------------------

## Code Explanation
### Database Module
#### `connection.py`
Establishes a connection to the SQL Server database using credentials from the `.env` file.
```python
# SQL Server Connection Setup
server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
driver = os.getenv("DB_DRIVER")
trusted_connection = os.getenv("DB_TRUSTED_CONNECTION")
connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection};"

# Create connection
def get_sql_connection():
    return pyodbc.connect(connection_string)
```

#### `crud_operations.py`
Handles `insert`, `update`, and `fetch` operations to ensure data integrity.
- Updates tenders if new data is more recent than the existing records.
- Fetches all stored tenders for visualization.

### Scraper Module
#### `web_scraper.py`
Automates the extraction of tender data from the BHEL website.
- Uses Selenium for navigating and extracting table data.
- Captures and processes CAPTCHA inputs programmatically.
- Provides options for exporting data to CSV.

--------------------------------------------------------------------------------------------------------------------------

## Key Functions
### Database Functions
1. `get_sql_connection()`: Establishes a database connection.
2. `insert_or_update_data_to_sql(data)`: Inserts or updates tenders in the database.
3. `fetch_all_data_from_sql()`: Retrieves all tenders from the database.

### Web Scraper Functions
1. `start_scraping()`: Automates the scraping process, captures data, and integrates it with the database.
2. `display_and_download_data(data, title, file_name)`: Displays data in Streamlit and provides a CSV download option.

--------------------------------------------------------------------------------------------------------------------------

## Usage
1. Launch the Streamlit app.
2. Click on **Start Scraping** to begin extracting data.
3. View newly inserted or updated tenders in the UI.
4. Download the data as CSV for offline use.

--------------------------------------------------------------------------------------------------------------------------

## Future Enhancements
- Add support for more tender websites.
- Implement advanced CAPTCHA-solving mechanisms.
- Enhance UI for a better user experience.

--------------------------------------------------------------------------------------------------------------------------

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For any issues or feature requests, please contact
[Shreya Joshi](mailto:shreyajoshi071003@gmail.com) / [Devanshi Dhabalia](mailto:dhabaliadevanshi@gmail.com).

--------------------------------------------------------------------------------------------------------------------------