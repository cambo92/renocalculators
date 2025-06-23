class Product:
    name = ""
    price = 0
    url = ""

    def __init__(self, name, price, url):
        self.name = name
        self.price = price
        self.url = url

class PaintProduct(Product):
    size = 0.5

    def __init__(self, name, price, url, size):
        super().__init__(name, price, url)
        self.size = size