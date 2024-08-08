from bs4 import BeautifulSoup
import requests

class WebScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def fetch_page(self, path: str) -> str:
        response = requests.get(self.base_url + path)
        response.raise_for_status()
        return response.text

    def parse_html(self, html_content: str) -> BeautifulSoup:
        return BeautifulSoup(html_content, 'html.parser')

    def scrape(self, path: str = '') -> list:
        html_content = self.fetch_page(path)
        soup = self.parse_html(html_content)
        return get_data(soup)

def get_data(soup: BeautifulSoup) -> list:
    products = []
    product_cards = soup.find_all('div', class_='card thumbnail')
    for card in product_cards:
        title = card.find('a', class_='title').text.strip()
        price = card.find('h4', class_='price').text.strip()
        description = card.find('p', class_='description').text.strip()
        review_count = card.find('p', class_='review-count').text.strip()
        products.append({
            'title': title,
            'price': price,
            'description': description,
            'review_count': review_count
        })
    return products

def main():
    base_url = 'https://webscraper.io'
    path = '/test-sites/e-commerce/scroll'
    scraper = WebScraper(base_url)
    data = scraper.scrape(path)
    print(data)

if __name__ == '__main__':
    main()