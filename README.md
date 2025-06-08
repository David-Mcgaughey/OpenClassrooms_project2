# Book Scraper Project

## Overview

This Python script scrapes book data from [http://books.toscrape.com/](http://books.toscrape.com/), extracts relevant details for each book, and saves the information into separate CSV files by category. It also downloads the cover image for each book and saves them locally.

This script functions as a basic **ETL (Extract, Transform, Load) pipeline**:

* **Extract**: Scrapes book data and images from the website.
* **Transform**: Cleans and organizes the data.
* **Load**: Stores the data into categorized CSV files and images into a local folder.

## How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/book-scraper.git
cd book-scraper
```

### 2. Set Up a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate      # On macOS/Linux
venv\Scripts\activate         # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Script

```bash
python scraper.py
```

### 5. Output

* CSV files will be created in the same directory, one for each book category.
* Images will be saved to the `images/` folder.

## Requirements

The project depends on the following Python packages:

```
requests
beautifulsoup4
```

These are listed in `requirements.txt`.

## .gitignore

Ensure that your `.gitignore` file contains the following to exclude the virtual environment:

```
venv/
__pycache__/
*.pyc
```

## Contact

For questions, please contact: [your-email@example.com](mailto:your-email@example.com)
