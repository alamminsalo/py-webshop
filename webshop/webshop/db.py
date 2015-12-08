
# Database operations

import mysql.connector

config = {
    'user':'shop',
    'password':'pass',
    'host':'localhost',
    'database':'webshop'
}

# Setup connection to mysqlserver
conn = mysql.connector.connect(**config)

def get_products(name, pricemin, pricemax, sort_by, offset, limit):
    print name, pricemin, pricemax, offset, limit

    return

get_products("A", 1, 10)


#def add_product(product):
#    return
#
#def get_user_shopcart(userId):
#    return
#
#

conn.close()

