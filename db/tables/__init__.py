TABLE_CREATORS = []


def register(creator):
    TABLE_CREATORS.append(creator)
    return creator
