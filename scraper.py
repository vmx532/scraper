import requests
from bs4 import BeautifulSoup
from site import Site

PARSER = "lxml"
MAIN_LINK_ATTRIBUTE = "href"


def scrape_by_rule(source: BeautifulSoup, selector: str, rule: str):
    def select_one():
        return source.select_one(selector).string

    def select_one_float_content():
        return float(source.select_one("selector")["content"])

    def select_all_ps():
        to_filter = [str(p.string).translate(str(p.string).maketrans("\n\t\r", "   ")).replace("   ", "") for p in
                     source.select(selector) if p.string is not None and p.string != ""]
        filter_obj = filter(lambda x: x != "", to_filter)
        return " ".join(list(filter_obj)).strip()

    def find_all_lis():
        return len(source.find("ul", class_=selector).find_all("li"))

    return {
        "select_one": select_one,
        "select_one_float_content": select_one_float_content,
        "select_all_ps": select_all_ps,
        "find_all_lis": find_all_lis,
    }.get(rule)()


def scrape_site(site: Site):
    response = requests.get(site.url)
    soup = BeautifulSoup(response.text, PARSER)
    site_links = soup.select(site.links_selector)

    stuff = []
    for link in site_links:
        url = f'{site.base_url}{link[MAIN_LINK_ATTRIBUTE]}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, PARSER)
        print(f"Checking {url}....")

        stuff_attributes = {}
        for attribute in site.attributes:
            stuff_attributes[attribute.name] = scrape_by_rule(soup, attribute.selector, attribute.rule)
        stuff.append(stuff_attributes)
    return stuff


def scrape_all_sites(sites: [Site]):
    if sites:
        sites_stuff = [scrape_site(site) for site in sites]
    else:
        raise Exception("Sites are empty.")
    return sites_stuff
