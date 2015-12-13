
# Restfull api using falcon framework

from wsgiref import simple_server
import falcon
import simplejson as json

# Local businesslogic
import businesslogic as bl


 
#Products interface
class ProductsResource:

    #GET handler
    def on_get(self, req, resp):
        print("Products GET")

        try:
            resp.body = json.dumps(bl.getProducts())
            resp.status = falcon.HTTP_200 #Status Ok

        except:
            #Return 500 - internal error
            resp.status = falcon.HTTP_500

#Single product resource
class ProductResource:
    #GET handler
    def on_get(self, req, resp, productId):
        print("Products GET")

        try:
            resp.body = json.dumps(bl.getProduct(productId))
            resp.status = falcon.HTTP_200 #Status Ok

        except:
            #Return 500 - internal error
            resp.status = falcon.HTTP_500


#Shopping cart interface
class ShopCartResource:

    def on_get(self, req, resp, userId):

        try:
            resp.body = json.dumps(bl.getShopCart(userId))
            resp.status = falcon.HTTP_200

        except:
            #Return 500 - internal error
            resp.status = falcon.HTTP_500

    def on_put(self, req, resp):
        try:
            #todo update logic
            resp.status = falcon.HTTP_200

        except:
            #Return 500 - internal error
            resp.status = falcon.HTTP_500


# Check that client has application/json in Accept header
# and Content-Type, if request has body
class RequireJSON(object):

    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.',
                href='http://docs.examples.com/api/json')

        if req.method in ('POST', 'PUT'):
            if 'application/json' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType(
                    'This API only supports requests encoded as JSON.',
                    href='http://docs.examples.com/api/json')

#JSON builder func for both incoming and outgoing messages 
class JSONBuilder(object):

    def process_request(self, req, resp):
            if req.content_length in (None, 0):
                # Nothing to do
                return

            body = req.stream.read()
            if not body:
                raise falcon.HTTPBadRequest('Empty request body',
                                            'A valid JSON document is required.')

            try:
                req.context['doc'] = json.loads(body.decode('utf-8'))

            except (ValueError, UnicodeDecodeError):
                raise falcon.HTTPError(falcon.HTTP_753,
                                       'Malformed JSON',
                                       'Could not decode the request body. The '
                                       'JSON was incorrect or not encoded as '
                                       'UTF-8.')

    def process_response(self, req, resp, resource):
        if 'result' not in req.context:
            return

        resp.body = json.dumps(req.context['result'])



api = falcon.API(middleware=[ 
        RequireJSON()
])


#Add api endpoints
products = ProductsResource()
api.add_route('/api/products', products)

product = ProductResource()
api.add_route('/api/products/{productId}', product)

shopcart = ShopCartResource()
api.add_route('/api/shopcart/{userId}', shopcart)

#Start the server 
if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    httpd.serve_forever()

