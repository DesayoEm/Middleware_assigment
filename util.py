from uuid import uuid4


def create_user_id():
    return str(uuid4()).replace('-', '')[:5]


print(create_user_id())
print(create_user_id())