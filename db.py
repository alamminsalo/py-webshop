
# Database operations

import mysql.connector
import decimal
from objects import *

config = {
    'user':'shop',
    'password':'pass',
    'host':'localhost',
    'database':'webshop'
}


# Get products, with query options
def getProducts(name = None, sortBy = 'name', minPrice = None, maxPrice = None, offset = None, limit = 100, productIds = None):

    products = {}

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(buffered=True)

        query = "SELECT product_id, code, name, price, in_stock FROM products WHERE TRUE"
        params = []

        #Add given parameters to query
        if productIds != None and len(productIds) > 0:
            query += " AND product_id IN ("
            for i in range(0,len(productIds)):
                if i > 0:
                    query += ","
                query += "%s"
                params.append(productIds[i])
            query += ")"

        if name != None:
            query += " AND name LIKE %s"
            name += "%%"
            params.append(name)

        if minPrice != None:
            query += " AND price >= %s"
            params.append(minPrice)

        if maxPrice != None:
            query += " AND price <= %s"
            params.append(maxPrice)
        
        if sortBy != None:
            query += " ORDER BY %s ASC"
            params.append(sortBy)

        if offset != None:
            query += " OFFSET %s"
            params.append(offset)

        if limit != None:
            query += " LIMIT %s"
            params.append(limit)

        print(query)
        #Exec query
        cursor.execute(query,params)

        #Add resulted products to array
        for (product_id, code, name, price, in_stock) in cursor:
            products[product_id] = Product(product_id, code, name, price, in_stock)
            print(product_id, code, name, price, in_stock)

    except mysql.connector.Error as e:
          print("Error in products query: {}".format(e))

    finally:
        if conn:
            conn.close()
        if cursor:
            cursor.close()

    return products

#Get single product information, if exists
def getProduct(pId):
    products = getProducts(productIds = [pId]).values()
    if len(products) > 0:
        return products[0]
    else:
        return None

# Add new or update existing product
def updateProduct(product):
    if product != None:

        #Validate insertable object
        product.validate()

        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            query, params = "", ()

            if product.productId == None or product.productId <= 0:
                query = "INSERT INTO products(code,name,price,in_stock) VALUES(%s, %s, %s, %s)"
                params = (product.code, product.name, product.price, product.in_stock)

            else:
                query = "UPDATE products SET code = %s, name = %s, price = %s, in_stock = %s WHERE product_id = %s"
                params = (product.code, product.name, product.price, product.in_stock, product.productId)

            cursor.execute(query, params)

            conn.commit()

        except mysql.connector.Error as e:
              print("Error in product update: {}".format(e))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            
    return

def updateCart(cart):
    if cart != None:

        #Validate insertable/updateable object
        cart.validate()

        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            query, params = "", []

            #Delete earlier products in cart by userId
            #cart can also be effectively cleared with no products in cart object
            query = "DELETE FROM shopcarts WHERE user_id = %s"

            cursor.execute(query, [cart.userId])
            conn.commit()

            #Form a querystring of values from products in cart
            query = ""
            productsQuery = ""
            for productId, count in cart.products.items():

                if len(query) > 0:
                    query += ","

                query += "(%s, %s, %s)"

                # Add userId, productId, productsCount to  queryParams
                params.append(cart.userId) 
                params.append(productId)
                params.append(count)

                # Add to productsQuery, which we'll use later
                if len(productsQuery) > 0:
                    productsQuery += ","

                productsQuery += "%s"


            #Check if data is to be added to db
            if len(query) > 0:
                query = "INSERT INTO shopcarts(user_id, product_id, count) VALUES" + query

                print(query)
                cursor.execute(query, params)
                conn.commit()



        except mysql.connector.Error as e:
              print("Error in cart update: {}".format(e))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            
    return


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

testCart = Cart(79)
testCart.addProduct(1)
testCart.addProduct(1)
updateCart(testCart)

