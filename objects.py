
class Product:
    def __init__(self, productId = 0, code = None, name = None, price = None, in_stock = None):
        self.productId = productId
        self.code = code
        self.name = name
        self.price = price
        self.in_stock = in_stock

    #Validation 
    def validate(self):
        if self.productId == None:
            raise Exception("Validation error in productId")
        if self.code == None:
            raise Exception("Validation error in code")
        if self.name == None:
            raise Exception("Validation error in name")
        if self.price == None:
            raise Exception("Validation error in price")
        if self.in_stock == None:
            raise Exception("Validation error in in_stock")


class Cart:
    def __init__(self, userId = 0):
        #UserId this shopcart belongs to
        self.userId = userId
        #List of products by id this shopcart holds
        self.products = {}

    def addProduct(self, productId):
        #Add products as dict, where
        #key is productId and value is amount of products
        if self.products.get(productId) == None:
            self.products[productId] = 0

        self.products[productId] += 1

    def validate(self):
        if self.userId == None or self.userId == 0:
            raise Exception("Validation error in userId")
        if self.products == None:
            raise Exception("Validation error in products")


