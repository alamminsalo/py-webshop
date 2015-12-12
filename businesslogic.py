
import db

#Creating or updating product
def updateProducts(products):
    for p in products:
        db.updateProduct(p)

#Query products with parameters
def getProducts(name = None, sortBy = 'name', minPrice = None, maxPrice = None, offset = None, limit = 100, productIds = None):
    return db.getProducts(name,sortby,minPrice,maxPrice,offset,limit,productIds)

#Update shopping cart of user
def updateShoppingCart(cart):
    #Check that to-be-updated products are all found in database
    if len(cart.products) > 0:
        products = getProducts(productIds = cart.products.keys())

        #Compare lists
        if not cart.products.keys().issubset(products.keys()):
            raise Exception("Exception: Some elements not found")

    db.updateCart(cart)

#Get shopping cart of user
def getShoppingCart(userId):
    return db.getCart(userId)

