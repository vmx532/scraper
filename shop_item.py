class ShopItem:
    def __init__(self, name, price: float, rank=0, review=0, about="", discount=0):
        self.name = name
        self.price = price
        self.rank = rank
        self.review = review
        self.about = about
        self.discount = discount

    def get_info(self):
        return f"Name: {self.name} / Price: {self.price} / Rank: [{self.rank}/5] / Review: {self.review} / " \
               f"About: {self.about} / Discount: {self.discount}%\n\n"

    def print(self):
        print(self.get_info())
