from random import randint
from accounts.models import Account


def generate_unique_verification_code(user: Account) -> str:
    verification_code = randint(11111, 99999)
    if user.verification_codes.filter(code=verification_code):
        generate_unique_verification_code(user=user)

    return verification_code
