
#DB unit tests
import db
from objects import Cart
from objects import Product

#Insert test entry
#updateProduct(Product(code="TESTCODE",name="Test entry",price=99.99,in_stock=999))

#Test querying
#options = getProductQueryOptions(sortBy='ce')
#for p in getProducts(options):
#    print(p.productId, p.code, p.name, p.price, p.in_stock)
#
#    #Test updating
#    p.price += decimal.Decimal(1.09)
#    #updateProduct(p)

#Test adding cart and some products to it
def test_cart_add():
    cart = Cart(79)
    cart.addProduct(1)
    cart.addProduct(1)
    db.updateCart(cart)

    cart2 = db.getCart


