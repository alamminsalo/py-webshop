
# Restfull api using falcon framework

from wsgiref import simple_server
import falcon
import json

#Resource endpoints import
from cartsResource import *
from productsResource import *


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
    RequireJSON(),
    JSONBuilder()
])


#Add api endpoints
products = ProductsResource()
api.add_route('/api/products', products)

product = ProductResource()
api.add_route('/api/products/{productId}', product)

shopcart = ShopCartResource()
api.add_route('/api/shopcarts/{userId}', shopcart)

shopcartProducts = ShopCartProductsResource()
api.add_route('/api/shopcarts/{userId}/products', shopcartProducts)

#Start the server 
if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    httpd.serve_forever()

