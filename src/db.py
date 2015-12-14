
# Database operations

import mysql.connector 
from objects import Cart
from objects import Product

config = {
    'user':'shop',
    'password':'pass',
    'host':'localhost',
    'database':'webshop'
}

#Assign decimal precision
import decimal
decimal.getcontext().prec = 3

# Get products, with query options
# If userId is given, inner join is made between products and shopcarts
def getProducts(name = None, sortBy = None, minPrice = None, maxPrice = None, offset = None, limit = None, productIds = None, code = None, userId = None):

    products = []

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(buffered=True)

        params = []
        query = "SELECT product_id, code, name, price, in_stock FROM products"

        if userId is not None and userId > 0:
            query += " JOIN shopcarts sc USING(product_id)"
        
        query += " WHERE TRUE"

        #Form rest of the query according to given parameters
        if productIds is not None and len(productIds) > 0:
            query += " AND product_id IN ("
            for i in range(0,len(productIds)):
                if i > 0:
                    query += ","
                query += "%s"
                params.append(productIds[i])
            query += ")"

        if userId is not None and userId > 0:
            query += " AND sc.user_id = %s"
            params.append(userId)

        if code is not None:
            query += " AND code = %s"
            params.append(code)

        if name is not None:
            query += " AND name LIKE %s"
            name += "%%"
            params.append(name)

        if minPrice is not None:
            query += " AND price >= %s"
            params.append(minPrice)

        if maxPrice is not None:
            query += " AND price <= %s"
            params.append(maxPrice)
        
        if sortBy is not None:
            if sortBy == 'name':
                query += " ORDER BY name ASC"
            elif sortBy == 'price':
                query += " ORDER BY price ASC"

        if limit is not None:
            query += " LIMIT %s"
            params.append(limit)
            
            #No offset without limit
            if offset is not None:
                query += " OFFSET %s"
                params.append(offset)

        #Exec query
        print(query)
        cursor.execute(query,params)

        #Add resulted products to array
        for (product_id, code, name, price, in_stock) in cursor:
            products.append(Product(product_id, str(code), str(name), decimal.Decimal(price), in_stock))
            #print(product_id, code, name, price, in_stock)

    except mysql.connector.Error as e:
          print("Error in products query: {}".format(e))

    finally:
        if conn:
            conn.close()
        if cursor:
            cursor.close()

    return products


# Add new or update existing product
def updateProduct(product):
    if product is not None:

        #Validate insertable object
        product.validate()

        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            query, params = "", ()

            if product.productId is None or product.productId <= 0:
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

# Delete product from database
def removeProduct(productId):
        if productId == None:
            return
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            query = "DELETE FROM products WHERE product_id = %s"

            cursor.execute(query, [productId])

            conn.commit()

        except mysql.connector.Error as e:
              print("Error in product deletion: {}".format(e))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

# Get shopping cart of user
def getShoppingCart(userId):
    result = None

    if userId is not None:
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            query = "SELECT product_id, count FROM shopcarts WHERE user_id = %s"

            cursor.execute(query, [userId])

            #Build Cart object from results
            for (product_id, count) in cursor:
                if result is None:
                    result = Cart(userId)
                result.products[product_id] = count


        except mysql.connector.Error as e:
              print("Error in product update: {}".format(e))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return result


def updateShoppingCart(cart):
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
            for productId, count in cart.products.items():

                if len(query) > 0:
                    query += ","

                query += "(%s, %s, %s)"

                # Add userId, productId, productsCount to  queryParams
                params.append(cart.userId) 
                params.append(productId)
                params.append(count)

            #Check if data is to be added to db
            if len(query) > 0:
                query = ("INSERT INTO shopcarts (user_id, product_id, count) VALUES " + query)

                ##print(query, params)
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

