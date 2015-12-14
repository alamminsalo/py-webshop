
# Shared function collection for rest interfaces

def getQueryParams(req):
    #Queryparams assembler
    name =      req.params.get('name')
    code =      req.params.get('code')
    sortBy =    req.params.get('sortby')
    minPrice =  req.params.get('min') 
    maxPrice =  req.params.get('max') 
    offset =    req.params.get('offset')
    limit =     req.params.get('limit') or 100
    productIds =req.params.get('id')

    print("Query params:")
    print("name %s" % name)
    print("code %s" % code)
    print("sortBy %s" % sortBy)
    print("minPrice %s" % minPrice)
    print("maxPrice %s" % maxPrice)
    print("offset %s" % offset)
    print("limit %s" % limit)
    print("productIds %s" % productIds)

    if minPrice is not None:
        minPrice = int(minPrice)

    if maxPrice is not None:
        maxPrice = int(maxPrice)

    if offset is not None:
        offset = int(offset)

    if limit is not None:
        limit = int(limit)

    return name, code, sortBy, minPrice, maxPrice, offset, limit, productIds


