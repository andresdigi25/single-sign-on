import random
import string


def is_empty_string(value):
    return value is None or value.strip() == ''


def get_random_password():
    lower = random.sample(string.ascii_lowercase, 3)
    upper = random.sample(string.ascii_uppercase, 2)
    num = random.sample(string.digits, 2)
    symbols = random.sample(string.punctuation, 1)

    password = lower + upper + num + symbols
    random.shuffle(password)

    return ''.join(password)