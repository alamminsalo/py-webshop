
class Product:
    def __init__(self, productId = 0, code = None, name = None, price = None, in_stock = None):
        self.productId = productId
        self.code = code
        self.name = name
        self.price = price
        self.in_stock = in_stock

    #Validation 
    def validate(self):
        if self.productId is None:
            raise Exception("Validation error in productId")
        if self.code is None:
            raise Exception("Validation error in code")
        if self.name is None:
            raise Exception("Validation error in name")
        if self.price is None:
            raise Exception("Validation error in price")
        if self.in_stock is None:
            raise Exception("Validation error in in_stock")


class Cart:
    def __init__(self, userId = 0):
        #UserId this shopcart belongs to
        self.userId = userId
        #List of products by id this shopcart holds
        self.products = {}

    def addProduct(self, productId):
        #In set key is productId and value is amount of products
        if self.products.get(productId) is None:
            self.products[productId] = 0

        self.products[productId] += 1

    #Validation 
    def validate(self):
        if self.userId is None or self.userId <= 0:
            raise Exception("Validation error in userId")
        if self.products is None:
            raise Exception("Validation error in products")

