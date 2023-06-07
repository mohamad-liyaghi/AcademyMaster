import secrets
import random


def generate_unique_token(obj):
    # Generate a random token length between 4 and 32
    token_length = random.randint(4, 32)

    # Generate a random token using the secrets module
    token = secrets.token_hex(token_length)[:token_length]

    # Check if the generated token is unique
    klass = obj.__class__
    if klass.objects.filter(token=token).exists():
        generate_unique_token(obj=obj)

    # Return the unique token
    return token
