import requests
from bs4 import BeautifulSoup
from shop_item import ShopItem


class ToysScraper:
    def __init__(self, toy_name="lego", page=1):
        self.toys = []
        self.base_url = "https://www.toy.ru"
        params = {
            "PAGEN_7": page,
        }
        response = requests.get(f"{self.base_url}/search/index.php?q={toy_name}", params=params)
        self.soup = BeautifulSoup(response.text, "lxml")

    def get_all_links(self):
        links = self.soup.select("a.product-name")
        return links

    def check_link(self, link):
        url = f'{self.base_url}{link["href"]}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        print(f"Checking {url}...")

        # elements searching
        name = soup.select_one("h1.detail-name").string
        price = float(soup.select_one("span.price")["content"])
        about = [str(p.string).translate(str(p.string).maketrans("\n\t\r", "   ")).replace("   ", "") for p in
                 soup.select(".collapse p") if p.string is not None and p.string != ""]
        filter_obj = filter(lambda x: x != "", about)
        about = " ".join(list(filter_obj)).strip()
        stars = len(soup.find("ul", class_="stars").find_all("li"))

        return ShopItem(name, price, rank=stars, about=about)

    def add_toy(self, toy: ShopItem):
        self.toys.append(toy)

    def get_toys(self):
        return self.toys
