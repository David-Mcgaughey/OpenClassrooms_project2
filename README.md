# Book Scraper Project

## What This Project Does

This Python project goes to a website called [Books to Scrape](http://books.toscrape.com/) and collects information about books in different categories. It saves the information into CSV files (like spreadsheets) and also downloads the book cover images into a folder on your computer.

This is a simple example of an **ETL process**:

* **Extract**: Get the data from the website.
* **Transform**: Organize and clean up the data.
* **Load**: Save the data into CSV files and download images.

---

## How to Use This Project

### Step 1: Clone the Repository

Open your terminal or command prompt and type:

```bash
git clone https://github.com/David-Mcgaughey/OpenClassrooms_project2.git
cd OpenClassrooms_project2
```

### Step 2: (Optional) Set Up a Virtual Environment

This keeps your Python packages organized:

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
# OR
source venv/bin/activate   # On Mac/Linux
```

### Step 3: Install the Required Packages

```bash
pip install -r requirements.txt
```

### Step 4: Run the Script

```bash
python scraper.py
```

### What Happens:

* You'll get one `.csv` file per book category.
* You'll also get an `images/` folder with all the book covers.

---

## What's in `requirements.txt`

These are the packages your code needs:

```
requests
beautifulsoup4
```

---

##  Keep Your Repo Clean

Create a `.gitignore` file (if you don't have one yet) and add this:

```
venv/
__pycache__/
*.pyc
*.csv
images/
```

That way, your extracted data and environment won't be uploaded to GitHub.

---


