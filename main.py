from site import Site, Attribute
from scraper import scrape_all_sites
import pandas as pd

DATA_FILE = "data.xlsx"

urls_data_df = pd.read_excel(DATA_FILE, sheet_name="urls")

sites = []

for index, row in urls_data_df.iterrows():
    site = Site(row.URL, row.Title, row.StuffSelector)
    site_data_df = pd.read_excel(DATA_FILE, sheet_name=site.title)
    for inner_index, inner_row in site_data_df.iterrows():
        attribute = Attribute(inner_row.LookingFor, inner_row.Selector, inner_row.Rule)
        site.add_attribute(attribute)
    sites.append(site)

excel_sites_stuff = scrape_all_sites(sites)
print(excel_sites_stuff)
