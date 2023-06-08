from random import randint
from accounts.models import Account


def generate_unique_verification_code(account: Account) -> str:
    verification_code = randint(11111, 99999)
    if account.verification_codes.filter(code=verification_code):
        generate_unique_verification_code(account=account)

    return verification_code
