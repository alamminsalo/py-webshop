
#Business Logic layer between interface and database levels

import db
from objects import Product
from objects import Cart


#Creating or updating products
def setProduct(product):

    """ here admin caller validation """

    db.updateProduct(product)

#Get single product information by id or product code 
def getProduct(pId = None, code = None):
    products = db.getProducts(productIds = [pId] if pId is not None else None, code = code)

    if len(products) > 0:
        return products[0]

    else:
        return None


#Query products with parameters
def getProducts(name = None, sortBy = None, minPrice = None, maxPrice = None, offset = None, limit = None, productIds = None, code=None, userId=None):

    if not sortBy in (None,'name', 'price'): raise Exception("Invalid parameter: sortBy; Values in 'name' or 'price' expected")

    return db.getProducts(name,sortBy,minPrice,maxPrice,offset,limit,productIds,code,userId)

#Update shopping cart of user
def setShoppingCart(cart):

    """here caller validation"""

    #Check that to-be-updated products are all found in database
    if len(cart.products) > 0:
        productIds = []
        for k in cart.products.keys():
            productIds.append(k)

        products = getProducts(productIds = productIds)

        #Compare lists
        for k in cart.products.keys():

            found = False

            for p in products:
                if k == p.productId:
                    found = True

            if found == False:
                raise Exception("Exception: Some elements not found")

    db.updateShoppingCart(cart)

#Get user's shopping cart
def getShoppingCart(userId):

    """here caller validation"""

    if userId == None or userId <= 0:
        raise Exception("Error in arguments while getting user's cart")

    return db.getShoppingCart(userId)

#Get products of shopping cart of user
def getShoppingCartProducts(name = None, sortBy = None, minPrice = None, maxPrice = None, offset = None, limit = None, productIds = None, code=None, userId=None):

    """here caller validation"""

    if userId == None:
        raise Exception("Error in shopping cart get; userId not given")

    products = db.getProducts(name, sortBy, minPrice, maxPrice, offset, limit, productIds, code, userId)

    cart = db.getShoppingCart(userId)

    results = []
    #Assemble products with cart information
    for p in products:
        print(p)
        """Swap 'count' entry in product with count in shopping cart of customer"""
        obj = Product.serialize(p)

        """Delete 'inStock'-entry from obj since we dont need it here"""
        del obj['inStock']

        """Add 'inCart'-entry, which tells us how many products of each type our cart has"""
        obj['inCart'] = cart.products[p.productId]

        results.append(obj)

    print(results)
    
    return results



