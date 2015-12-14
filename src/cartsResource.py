
import falcon
import restUtils
import json

#Business logic imports
import businesslogic as bl
from objects import Cart


#Shopping cart interface
class ShopCartResource:

    """If user credentials implemented, get caller account and use that information instead of pathparam"""

    def on_get(self, req, resp, userId):
        try:
            userId = int(userId)

            #Fetch cart info
            cart  = bl.getShoppingCart(userId)

            #Result dict
            result = {'myCart':cart}

            resp.body = json.dumps(result, sort_keys=True, default=Cart.serialize)
            resp.status = falcon.HTTP_200

        except:
            #Return 500 - internal error
            resp.status = falcon.HTTP_500

    def on_put(self, req, resp, userId):
        try:
            userId = int(userId)

            """Skip the validations because we dont have yet way of adding user
            accounts to the system.."""
            
            doc = req.context['doc']
            newCart = Cart.from_json(doc)

            if newCart.userId is None:
                newCart.userId = userId

            elif newCart.userId != userId:
                resp.status = falcon.HTTP_403
                return

            #update product
            bl.setShoppingCart(newCart)

            resp.status = falcon.HTTP_200 #Status Ok

        except:
            #Return 500 - internal error
            resp.status = falcon.HTTP_500



#Resource for querying products on one's shopping cart
class ShopCartProductsResource:

    """If user credentials implemented, get caller account and use that information instead of pathparam"""

    def on_get(self, req, resp, userId):
        try:
            name, code, sortBy, minPrice, maxPrice, offset, limit, productIds = restUtils.getQueryParams(req)
            userId = int(userId)

            #Fetch products using queryparams and pathparam userId
            productsInCart = bl.getShoppingCartProducts(name=name, code=code, sortBy=sortBy, minPrice=minPrice, maxPrice=maxPrice, offset=offset, limit=limit, productIds=productIds, userId=userId)

            result = {'products':productsInCart}
            resp.body = json.dumps(result, sort_keys=True)
            resp.status = falcon.HTTP_200

        except:
            #Return 500 - internal error
            resp.status = falcon.HTTP_500



