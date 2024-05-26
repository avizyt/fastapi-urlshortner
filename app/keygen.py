import secrets
import string
from sqlalchemy.orm import Session

from . import crud


def generate_random_key(
    length: int = 5,
    chars: str = string.ascii_uppercase + string.ascii_lowercase + string.digits,
) -> str:
    """
    Generate a random key.

    The key is a sequence of random characters of a given length.

    By default, the key is 5 characters long and is composed of a mix of
    uppercase letters, lowercase letters and digits.

    Args:
        length (int): The length of the key.
        chars (str): The characters to use.

    Returns:
        str: The random key.
    """
    return "".join(secrets.choice(chars) for _ in range(length))


def create_unique_random_key(db: Session) -> str:
    """
    Create a unique random key.

    Create a random key and check if it already exists in the database.
    If it does, create a new one.

    Args:
        db (Session): The database session to use.

    Returns:
        str: The unique random key.
    """
    key = generate_random_key()
    while crud.get_db_url_by_key(db, key):
        key = generate_random_key()
    return key
