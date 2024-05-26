from sqlalchemy.orm import Session
from . import keygen, models, schemas


def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    """
    Create a new URL in the database.

    The URL is created with a unique key and a secret key. The key
    is used to redirect to the target URL.

    Args:
        db (Session): The database session to use.
        url (schemas.URLBase): The URL data.

    Returns:
        models.URL: The created URL.
    """
    key = keygen.create_unique_random_key(db)
    secret_key = f"{key}_{keygen.generate_random_key(8)}"
    db_url = models.URL(
        target_url=url.target_url,
        key=key,
        secret_key=secret_key,
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_db_url_by_key(db: Session, url_key: str) -> models.URL:
    """
    Get a URL by its key.

    Args:
        db (Session): The database session to use.
        url_key (str): The key of the URL.

    Returns:
        models.URL: The URL.
    """
    return (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )


def get_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    """
    Get a URL by its secret key.

    Args:
        db (Session): The database session to use.
        secret_key (str): The secret key of the URL.

    Returns:
        models.URL: The URL.
    """
    return (
        db.query(models.URL)
        .filter(models.URL.secret_key == secret_key, models.URL.is_active)
        .first()
    )


def update_db_clicks(db: Session, db_url: schemas.URL) -> None:
    """
    Update the number of clicks of a URL in the database.

    Args:
        db (Session): The database session to use.
        db_url (schemas.URL): The URL whose number of clicks to update.

    Returns:
        None
    """
    # Increment the number of clicks.
    db_url.clicks += 1
    # Commit the changes.
    db.commit()
    # Refresh the URL object from the database.
    db.refresh(db_url)


def deactivate_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    """
    Deactivate a URL by its secret key.

    Args:
        db (Session): The database session to use.
        secret_key (str): The secret key of the URL.

    Returns:
        models.URL: The URL.
    """
    # Get the URL by its secret key.
    db_url = get_db_url_by_secret_key(db, secret_key)
    if db_url:
        # Deactivate the URL.
        # db_url.is_active = False
        db.query(models.URL).filter(models.URL.secret_key == secret_key).update(
            {"is_active": False}
        )
        # Commit the changes.
        db.commit()
        # Refresh the URL object from the database.
        db.refresh(db_url)
    return db_url
