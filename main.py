from scraper import ToysScraper
import pandas as pd

"""
    BS4 + Requests toys.ru lego
"""
ts = ToysScraper(page=2)
links = ts.get_all_links()
[ts.add_toy(ts.check_link(link)) for link in links]
[toy.print() for toy in ts.get_toys()]

# toys_objects = toys_scrape()
# [toy.print() for toy in toys_objects]
