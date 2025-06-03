import requests
from bs4 import BeautifulSoup
import csv

# Get the webpage
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, "html.parser")

# Find book information
title = soup.h1.text

table = soup.find("table", class_="table table-striped")
rows = table.find_all("tr")

# Make a dictionary with the books UPC, Prices, Availability
book_info = {}
for row in rows:
    header = row.th.text
    value = row.td.text
    book_info[header] = value

# Description
description_tag = soup.find("meta", attrs={"name": "description"})
if description_tag:
    description = description_tag["content"].strip()
else:
    description = "No description"

# Category
category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()

# Rating
rating_tag = soup.find("p", class_="star-rating")
rating = rating_tag["class"][1]

# Image URL
image_tag = soup.find("img")
image_url = "http://books.toscrape.com/" + image_tag["src"].replace("../", "")

# Step 3: Save the data to CSV
with open("one_book.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["URL","Title", "UPC", "Price (incl. tax)", "Price (excl. tax)", "Availability", "Description", "Category", "Rating", "Image URL"])
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

print("Book info saved to one_book.csv")
