
import falcon
import restUtils
import json

#Business logic imports
import businesslogic as bl
from objects import Product
from objects import Cart


#Products interface
class ProductsResource:

    #GET handler
    def on_get(self, req, resp):

        try:
            name, code, sortBy, minPrice, maxPrice, offset, limit, productIds = restUtils.getQueryParams(req)

            products = bl.getProducts(
                    name = name,
                    code = code,
                    sortBy = sortBy,
                    minPrice = minPrice,
                    maxPrice = maxPrice,
                    offset = offset,
                    limit = limit,
                    productIds = productIds
            )

            result = {'products':products}

            print(result)

            resp.body = json.dumps(result, sort_keys=True, default=Product.serialize)
            resp.status = falcon.HTTP_200 #Status Ok

        except:
            #Return 500 - internal error
            resp.status = falcon.HTTP_500

    #POST handler
    def on_post(self, req, resp):
        try:
            doc = req.context['doc']
            product = Product.from_json(doc)
            bl.setProduct(product)

            resp.status = falcon.HTTP_200

        except:
            resp.status = falcon.HTTP_500

#Single product resource
class ProductResource:

    #GET handler

    def on_get(self, req, resp, productId):
        try:
            productId = int(productId)
            product = bl.getProduct(productId)

            if product is None:
                return falcon.HTTP_404

            result = {'product':product}

            resp.body = json.dumps(result, sort_keys=True, default=Product.serialize)
            resp.status = falcon.HTTP_200 #Status Ok

        except:
            #Return 500 - internal error
            resp.status = falcon.HTTP_500


    def on_put(self, req, resp, productId):
        try:
            productId = int(productId)
            product = bl.getProduct(productId)

            if product is None:
                return falcon.HTTP_404

            doc = req.context['doc']
            newProduct  = Product.from_json(doc)

            if newProduct.productId is None:
                newProduct.productId = product.productId

            #If updated object has id which doesn't match old one, return http forbidden-status
            elif newProduct.productId != productId:
                return falcon.HTTP_403

            #update product
            bl.setProduct(newProduct)

            resp.status = falcon.HTTP_200 #Status Ok
        except:
            #Return 500 - internal error
            resp.status = falcon.HTTP_500



