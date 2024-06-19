import random
import string


def GeneratePassword(length):
    return ''.join([random.choices(string.ascii_letters + string.digits, string.punctuation) for n in range(length)])
