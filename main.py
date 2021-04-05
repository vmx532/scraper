from site_ import WebSite, Attribute
from scraper import scrape_site
import pandas as pd
import math
import json

DATA_FILE = "data.xlsx"


# Vladislav Minin 21:50 05.04.2021
"""
Инициализация веб-сайтов из xlsx документа
Чтение атрибутов веб-сайтов из xlsx документа
"""
urls_data_df = pd.read_excel(DATA_FILE, sheet_name="urls")
sites = []
for index, row in urls_data_df.iterrows():
    if row.Active == "no":
        continue

    if not isinstance(row.Params, str) and not math.isnan(row.Params):
        json_acceptable_params = row.Params.replace("'", "\"")
        params = json.loads(json_acceptable_params)
    else:
        params = None

    site = WebSite(row.URL, row.Title, row.StuffSelector, params)
    site_data_df = pd.read_excel(DATA_FILE, sheet_name=site.title)
    for inner_index, inner_row in site_data_df.iterrows():
        attribute = Attribute(inner_row.LookingFor, inner_row.Selector, inner_row.Rule)
        site.add_attribute(attribute)
    sites.append(site)


# Vladislav Minin 21:50 05.04.2021
"""
Формирование файла результатов
"""
excel_sites_stuff = [scrape_site(site) for site in sites]
excel_sites_stuff_df = pd.concat([pd.DataFrame(excel_site_stuff) for excel_site_stuff in excel_sites_stuff])
excel_sites_stuff_df.to_csv("results.csv")
