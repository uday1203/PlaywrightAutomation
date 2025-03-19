# Playwright Product Catalog Scraper

## Overview
This Playwright script automates data extraction from a product catalog. It efficiently manages sessions, navigates hidden menus, extracts product data, and exports the data to a structured JSON file for analysis.

## Features
- **Session Management:** Logs in if necessary and maintains an active session.
- **Automated Navigation:** Clicks through UI elements to reach the product catalog.
- **Data Extraction:** Scrapes product details from a dynamically loaded table.
- **Scroll Handling:** Automatically scrolls until all products are loaded.
- **Export to JSON:** Saves extracted data in a structured JSON format.

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/uday1203/PlaywrightAutomation.git
   cd PlaywrightAutomation
   ```
2. Install dependencies:
   ```sh
   pip install playwright tqdm
   playwright install
   ```

## Usage
1. Run the script:
   ```sh
   python script.py
   ```
2. Extracted data will be saved as `Data.json`.

## Configuration
- Update authentication credentials in the `credentials` dictionary inside `script.py`.
- Modify navigation selectors in `script.py` if needed.


