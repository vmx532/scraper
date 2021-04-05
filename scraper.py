import requests
from bs4 import BeautifulSoup
from site_ import WebSite

PARSER = "lxml"
MAIN_LINK_ATTRIBUTE = "href"


def scrape_by_rule(source: BeautifulSoup, selector: str, rule: str):
    # Vladislav Minin 21:50 05.04.2021
    """
    Функция поиска атрибута по заданному правилу по селектору
    :param source: HTML код BS4
    :param selector: Селектор поиска
    :param rule: Правило поиска
    :return:
    """
    def select_one():
        # Vladislav Minin 21:50 05.04.2021
        """
        Поиск первого
        :return: Значение без лишних отступов
        """
        return str(source.select_one(selector).string).strip()

    def select_one_float_content():
        # Vladislav Minin 21:50 05.04.2021
        """
        Поиск первого со значением из свойства content
        :return: Значение с вещественным типом данных
        """
        return float(source.select_one(selector)["content"])

    def select_all_ps():
        # Vladislav Minin 21:50 05.04.2021
        """
        Поиск содержимого всех параграфов
        :return: Значение со всех параграфов
        """
        to_filter = [str(p.string).translate(str(p.string).maketrans("\n\t\r", "   ")).replace("   ", "") for p in
                     source.select(selector) if p.string is not None and p.string != ""]
        filter_obj = filter(lambda x: x != "", to_filter)
        return " ".join(list(filter_obj)).strip()

    def find_all_lis():
        # Vladislav Minin 21:50 05.04.2021
        """
        Поиск рейтинга по "звездам"
        :return: Значение рейтинга по кол-ву звезд 0..5
        """
        return len(source.find("ul", class_=selector).find_all("li"))

    def select_one_div_only_nums():
        # Vladislav Minin 21:50 05.04.2021
        """
        Поиск содержимого первого блока по селектору
        :return: Содержимое блока если найдено, Not found - не обнаружено
        """
        try:
            return "".join(digit_letter for digit_letter in str(source.select_one(selector)) if digit_letter.isdigit())
        except AttributeError:
            return "Not found"

    return {
        "select_one": select_one,
        "select_one_float_content": select_one_float_content,
        "select_all_ps": select_all_ps,
        "find_all_lis": find_all_lis,
        "select_one_div_only_nums": select_one_div_only_nums,
    }.get(rule)()


def scrape_site(site: WebSite):
    # Vladislav Minin 21:50 05.04.2021
    """
    Скрейпинг страницы
    :param site: Веб-сайт
    :return: Объект-поиска
    """
    response = requests.get(site.url, params=site.params)
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
