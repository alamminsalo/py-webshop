

class ProductDO:
#Constructor
    def __init__(self, productId = 0, code = None, name = None, price = None, in_stock = None):
        self.productId = productId
        self.code = code
        self.name = name
        self.price = price
        self.in_stock = in_stock

    #Validation 
    def validate(self):
        return (
            self.code != None 
            and self.name != None
            and self.price != None
            and self.in_stock != None
        )





