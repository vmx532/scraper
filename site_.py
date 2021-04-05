from urllib.parse import urlparse


class Attribute:
    """
    Характеристика сайта и правила ее нахождения
    """
    def __init__(self, name, selector, rule):
        # Vladislav Minin 21:50 05.04.2021
        """
        Инициализация характеристики сайта
        :param name: Наименование характеристики
        :param selector: Селектор поиска характеристики
        :param rule: Правила поиска с использованием селектора
        """
        self.name = name
        self.selector = selector
        self.rule = rule


class WebSite:
    """
    Веб-страница
    """
    def __init__(self, url, title, links_selector, params):
        # Vladislav Minin 21:50 05.04.2021
        """
        Инициализация данных веб-страницы
        :param url: Ссылка
        :param title: Название (метка)
        :param links_selector: Селектор списка ссылок поиска (товаров)
        :param params: Дополнительные параметры GET запроса
        """
        self.url = url
        parsed_url = urlparse(url)
        self.base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        self.title = title
        self.links_selector = links_selector
        self.params = params
        self.attributes = []

    def add_attribute(self, attribute: Attribute):
        # Vladislav Minin 21:50 05.04.2021
        """
        Функция добавления атрибута на сайте
        :param attribute: Атрибут, который будет добавлен
        """
        self.attributes.append(attribute)
