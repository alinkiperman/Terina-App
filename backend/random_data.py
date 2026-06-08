import random
from datetime import date, timedelta


FIRST_NAMES = ["David", "Sarah", "Michael", "Rachel", "Daniel", "Maya", "Noa", "Yosef"]
LAST_NAMES = ["Cohen", "Levi", "Greenberg", "Shalev", "Azoulay", "Katz", "Friedman"]


def random_full_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def random_gender():
    return random.choice(["Male", "Female"])


def random_date_of_birth():
    start = date(1950, 1, 1)
    end = date(1990, 12, 31)
    delta_days = (end - start).days
    return start + timedelta(days=random.randint(0, delta_days))


def random_phone():
    return "05" + str(random.randint(10000000, 99999999))


def random_email(full_name):
    name = full_name.lower().replace(" ", ".")
    return f"{name}{random.randint(1, 999)}@gmail.com"


