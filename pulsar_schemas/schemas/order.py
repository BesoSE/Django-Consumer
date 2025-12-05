from pulsar.schema import *


class Order(Record):
    shipping_address = String()
    email = String()
    product = String()
    total_amount = Double()
    status = String()
    created_at = String()



