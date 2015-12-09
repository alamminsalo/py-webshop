
# Database operations

from dbobjects import *
import mysql.connector
import decimal

config = {
    'user':'shop',
    'password':'pass',
    'host':'localhost',
    'database':'webshop'
}

# Setup connection to mysqlserver



# Query options for fetching products
def getProductQueryOptions(sortBy = 'name', minPrice = None, maxPrice = None, offset = None, limit = None):
    # Some input checking, add more sorting columns here if needed
    if sortBy not in set(['name','price']):
        sortBy = 'name'

    return {
        'minPrice':         minPrice,
        'maxPrice':         maxPrice,
        'sortBy':           sortBy,
        'offset':           offset,
        'limit':            limit
    }

# Get products, with query options
def getProducts(options = getProductQueryOptions()):
    products = []

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(buffered=True)

        query = "SELECT product_id, code, name, price, in_stock FROM products WHERE TRUE"

        #Add given parameters to query
        if options.get('minPrice') != None:
            print("min",options.get('minPrice'))
            query += " AND price >= %d"

        if options.get('maxPrice') != None:
            print("max",options.get('maxPrice'))
            query += " AND price <= %d"
        
        if options.get('sortBy') != None:
            print("sortBy",options.get('sortBy'))
            query += " ORDER BY %s ASC"

        if options.get('offset') != None:
            print("offset",options.get('offset'))
            query += " OFFSET %d"

        if options.get('limit') != None:
            print("limit",options.get('limit'))
            query += " LIMIT %d"

        #Create array of params which were used
        params = []
        for value in options.values():
            if value != None:
                params.append(value)

        #Exec query
        cursor.execute(query,params)

        #Add queried products to array
        for (product_id, code, name, price, in_stock) in cursor:
            products.append(ProductDO(product_id, code, name, price, in_stock))

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

    #Validate product before adding
    if (product == None
        or not isinstance(product, ProductDO) 
        or not product.validate()):
        return

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        query, params = "", ()

        if product.productId <= 0:
            print("adding new product")
            query = "INSERT INTO products(code,name,price,in_stock) VALUES(%s, %s, %s, %s)"
            params = (product.code, product.name, product.price, product.in_stock)

        else:
            query = "UPDATE products SET code = %s, name = %s, price = %s, in_stock = %s WHERE product_id = %s"
            params = (product.code, product.name, product.price, product.in_stock, product.productId)

        print(query % params)
        cursor.execute(query, params)

        conn.commit()

    except mysql.connector.Error as e:
          print("Error in product update: {}".format(e))

    finally:
        if conn:
            conn.close()
        if cursor:
            cursor.close()
            
    return



#Insert test entry
updateProduct(ProductDO(code="TESTCODE",name="Test entry",price=99.99,in_stock=999))

#Test querying
options = getProductQueryOptions(sortBy='ce')
for p in getProducts(options):
    print(p.productId, p.code, p.name, p.price, p.in_stock)

    #Test updating
    p.price += decimal.Decimal(1.09)
    updateProduct(p)



