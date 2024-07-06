import requests
from bs4 import BeautifulSoup
import csv
import time

def fetch_page(url):
    """
    Fetch the content of the URL and return the response object.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_page(response):
    """
    Parse the response content and extract book titles, prices, and availability.
    """
    soup = BeautifulSoup(response.content, 'html.parser')
    books = []

    for book in soup.find_all('article', class_='product_pod'):
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').get_text(strip=True)
        availability = book.find('p', class_='instock availability').get_text(strip=True)
        books.append({'title': title, 'price': price, 'availability': availability})

    return books

def save_to_csv(books, filename='books.csv'):
    """
    Save the list of books to a CSV file.
    """
    keys = books[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(books)

def scrape_books(url, pages=1):
    """
    Scrape books from the given URL and handle pagination if necessary.
    """
    all_books = []

    for page in range(1, pages + 1):
        page_url = f"{url}catalogue/page-{page}.html" 
        response = fetch_page(page_url)

        if response:
            books = parse_page(response)
            all_books.extend(books)
            time.sleep(1) 

    return all_books

if __name__ == "__main__":
    base_url = 'http://books.toscrape.com/'
    num_pages = 5 
    # Scrape books
    books = scrape_books(base_url, num_pages)

    # Check if books were found
    if books:
        # Save books to CSV
        save_to_csv(books)
        print(f"Scraped and saved {len(books)} books.")
    else:
        print("No books found.")
