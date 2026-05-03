TABLE_CREATORS = []

def register(fn):
    TABLE_CREATORS.append(fn)
    return fn