
#DB unit tests
import db
from objects import Cart
from objects import Product

#Insert test entry
def test_product_add():
    db.updateProduct(Product(code="TESTCODE",name="Test product",price=99.99,in_stock=999))
    t = db.getProduct(code="TESTCODE")
    assert(t is not None)

#Test querying
def test_products_get():
    for p in db.getProducts().values():
        print(p.productId, p.code, p.name, p.price, p.in_stock)

#Test adding cart and some products to it
def test_cart_add():
    cart = Cart(79)
    cart.addProduct(1)
    cart.addProduct(1)
    db.updateShoppingCart(cart)

    cart2 = db.getShoppingCart

test_product_add()
test_products_get()
test_cart_add()

