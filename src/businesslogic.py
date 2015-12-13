
#Business Logic layer between interface and database levels

import db

#Creating or updating products
def setProducts(products):

    """ here admin caller validation """

    for p in products:
        db.updateProduct(p)

#Get single product information by id or product code
def getProduct(pId = None, code = None):
    pIds = None
    if pId is not None:
        pIds = [pId]

    products = db.getProducts(productIds = pIds, code = code, limit=1)

    if len(products) > 0:
        return products[0]

    else:
        return None


#Query products with parameters
def getProducts(name = None, sortBy = 'name', minPrice = None, maxPrice = None, offset = None, limit = 100, productIds = None, code=None, userId=None):
    print("GET products")
    return {'products':db.getProducts(name=name, sortBy=sortBy, minPrice=minPrice, maxPrice=maxPrice, offset=offset, limit=limit, productIds=productIds, code=code, userId=userId)}

#Update shopping cart of user
def setShoppingCart(cart):

    """here user caller validation"""

    #Check that to-be-updated products are all found in database
    if len(cart.products) > 0:
        products = getProducts(productIds = cart.products.keys())

        #Compare lists
        if not set(cart.products.keys()).issubset(set(products.keys())):
            raise Exception("Exception: Some elements not found")

    db.updateShoppingCart(cart)

#Get shopping cart of user
def getShoppingCart(userId):

    """here user caller validation"""
    
    return { mycart: db.getShoppingCart(userId) }



