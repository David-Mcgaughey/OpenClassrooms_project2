import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin


def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def extract_book_data(book_url):
    soup = get_soup(book_url)

    title = soup.h1.text
    table = soup.find("table", class_="table table-striped")
    rows = {row.th.text: row.td.text for row in table.find_all("tr")}

    description_tag = soup.find("meta", attrs={"name": "description"})
    description = description_tag["content"].strip() if description_tag else "No description"

    category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
    rating = soup.find("p", class_="star-rating")["class"][1]

    image_url = urljoin(book_url, soup.find("div", class_="item active").img["src"])

    return {
        "product_page_url": book_url,
        "universal_ product_code (upc)": rows.get("UPC", ""),
        "book_title": title,
        "price_including_tax": rows.get("Price (incl. tax)", ""),
        "price_excluding_tax": rows.get("Price (excl. tax)", ""),
        "quantity_available": rows.get("Availability", ""),
        "product_description": description,
        "category": category,
        "review_rating": rating,
        "image_url": image_url
    }


def write_to_csv(data, filename="one_book.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow(data)
    print(f"Data written to {filename}")


def main():

    book_url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

    print("Scraping one book...")
    book_data = extract_book_data(book_url)
    write_to_csv(book_data)


if __name__ == "__main__":
    main()
