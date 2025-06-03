import requests
from bs4 import BeautifulSoup
import csv

# Step 1: Get all product URLs from the Science category page
base_url = "http://books.toscrape.com/"
category_url = "http://books.toscrape.com/catalogue/category/books/science_22/index.html"
response = requests.get(category_url)
soup = BeautifulSoup(response.text, "html.parser")

# Collect all book URLs from this page
book_links = soup.select("h3 a")
book_urls = [base_url + "catalogue/" + link["href"].replace("../", "") for link in book_links]

# Prepare the CSV file
with open("science_books.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["URL", "Title", "UPC", "Price (incl. tax)", "Price (excl. tax)", "Availability", "Description", "Category", "Rating", "Image URL"])

    # Step 2: Visit each product page and scrape the info
    for url in book_urls:
        book_response = requests.get(url)
        book_soup = BeautifulSoup(book_response.text, "html.parser")

        title = book_soup.h1.text

        table = book_soup.find("table", class_="table table-striped")
        rows = table.find_all("tr")
        book_info = {}
        for row in rows:
            header = row.th.text
            value = row.td.text
            book_info[header] = value

        # Description
        description_tag = book_soup.find("meta", attrs={"name": "description"})
        description = description_tag["content"].strip() if description_tag else "No description"

        # Category
        category = book_soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()

        # Rating
        rating_tag = book_soup.find("p", class_="star-rating")
        rating = rating_tag["class"][1]

        # Image URL
        image_tag = book_soup.find("img")
        image_url = base_url + image_tag["src"].replace("../", "")

        # Write row to CSV
        writer.writerow([
            url,
            title,
            book_info.get("UPC", ""),
            book_info.get("Price (incl. tax)", ""),
            book_info.get("Price (excl. tax)", ""),
            book_info.get("Availability", ""),
            description,
            category,
            rating,
            image_url
        ])

print("Science books scraped and saved to science_books.csv")
