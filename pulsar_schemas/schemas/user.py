from pulsar.schema import *


class User(Record):
    first_name = String()
    last_name = String()
    email = String()
    status = Boolean()
    phone = String()
    address = String()



