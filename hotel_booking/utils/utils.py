import string
import random


def generate_id(length=20):
    characters = string.ascii_letters + string.digits
    id = ''.join(random.choice(characters) for _ in range(length))
    return id