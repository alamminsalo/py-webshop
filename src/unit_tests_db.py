
import db
import businesslogic as bl
import simplejson as json
from decimal import Decimal
from objects import Cart
from objects import Product
import random


#DB section
#Insert test entry 
def test_product_add():
    print("Testing product insert..")

    db.updateProduct(Product(code="POOLBL",name="PoolBall",price=Decimal(9.80),in_stock=999))
    t = bl.getProduct(code="POOLBL")
    assert(t is not None)



#Test querying
def test_products_get():
    print("Testing product get..")

    for p in db.getProducts():
        print(p.productId, p.code, p.name, p.price, p.in_stock)

#Test adding cart and some products to it
def test_cart_add():
    print("Testing cart add..")

    cart = Cart(79)

    cart.addProduct(1)
    cart.addProduct(1)
    db.updateShoppingCart(cart)

    cart2 = db.getShoppingCart(79)
    assert(cart2 is not None)

test_product_add()
test_products_get()
test_cart_add()


#BL section

def bl_getProductsJSON():
    print("Testing json..")

    a = bl.getProducts()
    b = json.dumps(a, default = Product.serialize, sort_keys = True)

bl_getProductsJSON()

def bl_getShopCartProducts():
    print("Testing fetching products in shopcart..")

    a = bl.getProducts(userId=79)
    assert(a is not None)
    print(a)

bl_getShopCartProducts()


