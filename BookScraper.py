import requests
from bs4 import BeautifulSoup
import csv
import os

base_url = "http://books.toscrape.com/"
home_url = base_url

# Make sure the images folder exists
if not os.path.exists("images"):
    os.makedirs("images")

# Get all categories
response = requests.get(home_url)
soup = BeautifulSoup(response.text, "html.parser")

category_links = soup.select("div.side_categories ul li ul li a")
categories = {
    link.text.strip(): base_url + link["href"]
    for link in category_links
}

# Loop through categories
for category_name, category_url in categories.items():
    print(f"Scraping category: {category_name}")

    # Format category filename
    filename = f"{category_name.lower().replace(' ', '_')}_books.csv"

    # Open CSV for this category
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Title", "UPC", "Price (incl. tax)", "Price (excl. tax)",
                         "Availability", "Description", "Category", "Rating", "Image URL", "Image Filename"])

        current_url = category_url

        while current_url:
            category_response = requests.get(current_url)
            category_soup = BeautifulSoup(category_response.text, "html.parser")

            # Collect book URLs from the page
            book_links = category_soup.select("h3 a")
            book_urls = []
            for link in book_links:
                partial_url = link["href"].replace("../../../", "").replace("../../", "")
                full_url = base_url + "catalogue/" + partial_url
                book_urls.append(full_url)

            # Visit each book page
            for url in book_urls:
                book_response = requests.get(url)
                book_soup = BeautifulSoup(book_response.text, "html.parser")

                title = book_soup.h1.text

                # Extract book info from the table
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

                # Category and rating
                category = book_soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
                rating_tag = book_soup.find("p", class_="star-rating")
                rating = rating_tag["class"][1] if rating_tag else "None"

                # Image handling
                image_tag = book_soup.find("img")
                image_url = base_url + image_tag["src"].replace("../", "")

                # Make filename safe and unique
                upc = book_info.get("UPC", "")
                safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)
                short_title = safe_title[:40]  # limit to first 40 characters
                image_filename = f"images/{short_title}_{upc}.jpg"

                # Download and save image
                try:
                    img_data = requests.get(image_url).content
                    with open(image_filename, "wb") as img_file:
                        img_file.write(img_data)
                except Exception as e:
                    print(f"Failed to download image for '{title}': {e}")
                    image_filename = "Download failed"

                # Write book info to CSV
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
                    image_url,
                    image_filename
                ])

            # Handle pagination
            next_button = category_soup.select_one("li.next a")
            if next_button:
                next_page_url = next_button["href"]
                current_url = "/".join(current_url.split("/")[:-1]) + "/" + next_page_url
            else:
                current_url = None

print("All categories scraped and saved to individual CSV files.")
