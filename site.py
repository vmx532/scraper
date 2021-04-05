from urllib.parse import urlparse


class Attribute:
    def __init__(self, name, selector, rule):
        self.name = name
        self.selector = selector
        self.rule = rule


class Site:
    def __init__(self, url, title, links_selector):
        self.url = url
        self.base_url = urlparse(url).netloc
        self.title = title
        self.links_selector = links_selector
        self.attributes = []

    def add_attribute(self, attribute: Attribute):
        self.attributes.append(attribute)
