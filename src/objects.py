
from decimal import Decimal

class Product:
    def __init__(self, productId = None, code = None, name = None, price = None, in_stock = None):
        self.productId = productId
        self.code = code
        self.name = name
        self.price = price
        self.in_stock = in_stock

    def printData(self):
        print("Product:")
        print("productId: %s" % self.productId)
        print("name: %s" % self.name)
        print("code: %s" % self.code)
        print("price: %s" % self.price)
        print("in_stock: %s" % self.in_stock)

    #Validation 
    def validate(self):
        if self.productId is not None and self.productId <= 0:
            raise Exception("Validation error in productId")
        if self.code is None:
            raise Exception("Validation error in code")
        if self.name is None:
            raise Exception("Validation error in name")
        if self.price is None or type(self.price) is not Decimal:
            raise Exception("Validation error in price")
        if self.in_stock is None:
            raise Exception("Validation error in in_stock")

    @staticmethod
    def serialize(obj):

        if type(obj) != Product:
            raise Exception("Error in serialization: Wrong type")

        obj.validate()
        return {
            'id':obj.productId,
            'code':obj.code,
            'name':obj.name,
            'price':str(obj.price),
            'inStock':obj.in_stock
        }

    @staticmethod
    def from_json(data):
        productId = data.get('id')
        code = data.get('code')
        name = data.get('name')
        price = Decimal(data.get('price'))
        in_stock = int(data.get('inStock'))

        product = Product(productId = productId, code = code, name = name, price = price, in_stock = in_stock)

        #product.printData()

        product.validate()

        return product


class Cart:
    def __init__(self, userId = 0):
        self.userId = userId
        self.products = {}

    def addProduct(self, productId):
        #Set of products, where products[id] = count
        if self.products.get(productId) is None:
            self.products[productId] = 0

        self.products[productId] += 1

    #Validation 
    def validate(self):
        if self.userId is None or self.userId <= 0:
            raise Exception("Validation error in userId")
        if self.products is None:
            raise Exception("Validation error in products")

    #Serialize object to json-friendly format
    @staticmethod
    def serialize(obj):
        if type(obj) != Cart:
            raise Exception("Error in serialization: Wrong type")

        obj.validate()

        products = []
        for pId, count in obj.products.items():
            products.append({ 'productId':pId, 'inCart':count })

        return {
            'userId':obj.userId,
            'products':products
        }

    #deserializer
    @staticmethod
    def from_json(data):
        cart = Cart()
        
        #Assemble products
        if data.get('products') is not None:
            for product in data.get('products'):
                pId = product.get('productId')
                count = product.get('inCart')
                cart.products[int(pId)] = int(count)

        #Set userId
        if data.get('userId') is not None:
            cart.userId = int(data.get('userId'))

        cart.validate()

        return cart


