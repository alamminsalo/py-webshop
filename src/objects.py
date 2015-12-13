
from decimal import Decimal

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
        if self.price is None or type(self.price) is not Decimal:
            print(type(self.price))
            raise Exception("Validation error in price")
        if self.in_stock is None:
            raise Exception("Validation error in in_stock")

    def serialize(self):
        return {
            'id':self.productId,
            'code':self.code,
            'name':self.name,
            'price':str(self.price),
            'inStock':self.in_stock
        }

    def from_json(self):
        #todo from json logic
        return


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

    def from_json(self):
        #todo from json logic
        return


