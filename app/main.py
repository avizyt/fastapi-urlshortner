import validators
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from . import schemas, models, crud
from .database import SessionLocal, engine
from .config import get_settings
from starlette.datastructures import URL

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    """
    Get a database session.

    Yields a database session.

    The session is automatically closed when the generator is exited.
    """
    db = SessionLocal()
    try:
        # Yield the database session.
        yield db
    finally:
        # Close the database session when we are done.
        db.close()


@app.get("/")
def read_root():
    return "Welcome to the URL shortener API :)"


def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


# @app.post("/url", response_model=schemas.URLInfo)
# def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
#     if not validators.url(url.target_url):
#         raise raise_bad_request(message="Your provider URL is not valid")

#     db_url = crud.create_db_url(db=db, url=url)

#     db_url.url = db_url.key
#     db_url.admin_url = db_url.secret_key
#     return db_url


@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    """
    Create a new shortened URL.

    Args:
        url (schemas.URLBase): The URL data.

    Returns:
        schemas.URLInfo: The shortened URL.

    Raises:
        HTTPException: If the provider URL is not valid.
    """
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provider URL is not valid")

    db_url = crud.create_db_url(db=db, url=url)
    return get_admin_info(db_url)


@app.get("/{url_key}")
def forward_to_target_url(
    url_key: str, request: Request, db: Session = Depends(get_db)
):
    """
    Forward to the target URL of a shortened URL.

    Args:
        url_key (str): The key of the shortened URL.
        request (Request): The request object.
        db (Session): The database session to use.

    Returns:
        RedirectResponse: A redirect response to the target URL.

    Raises:
        HTTPException: If the shortened URL is not found.
    """
    # := is assignment expression
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        # Update the number of clicks of the shortened URL.
        crud.update_db_clicks(db=db, db_url=db_url)
        # Redirect to the target URL.
        return RedirectResponse(db_url.target_url)
    else:
        # Raise an HTTPException if the shortened URL is not found.
        raise_not_found(request=request)


@app.get(
    "/admin/{secret_key}", name="administration info", response_model=schemas.URLInfo
)
def get_url_info(secret_key: str, request: Request, db: Session = Depends(get_db)):
    """
    Get the administration info of a shortened URL.

    Args:
        secret_key (str): The secret key of the shortened URL.
        request (Request): The request object.
        db (Session): The database session to use.

    Returns:
        schemas.URLInfo: The administration info of the shortened URL.

    Raises:
        HTTPException: If the shortened URL is not found.
    """
    if db_url := crud.get_db_url_by_secret_key(db=db, secret_key=secret_key):
        # Get the administration info of the shortened URL.
        return get_admin_info(db_url)
    else:
        # Raise an HTTPException if the shortened URL is not found.
        raise_not_found(request=request)


def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    """
    Get the administration info of a shortened URL.

    Args:
        db_url (models.URL): The URL to get the administration info of.

    Returns:
        schemas.URLInfo: The administration info of the shortened URL.
    """
    # Get the base URL from the configuration.
    base_url = URL(get_settings().base_url)

    # Get the administration info endpoint URL.
    admin_endpoint = app.url_path_for(
        "administration info",
        secret_key=db_url.secret_key,
    )

    # Set the URL and administration URL of the shortened URL.
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))

    # Return the shortened URL with the administration info.
    return db_url


@app.delete("/admin/{secret_key}")
def delete_url_info(secret_key: str, request: Request, db: Session = Depends(get_db)):
    """
    Delete a shortened URL by its secret key.

    Args:
        secret_key (str): The secret key of the shortened URL.
        request (Request): The request object.
        db (Session): The database session to use.

    Returns:
        dict[str, str]: A dictionary with the detail of the deletion.
    """
    if db_url := crud.deactivate_db_url_by_secret_key(db, secret_key=secret_key):
        # Return a dictionary with the detail of the deletion.
        return {
            "detail": f"Successfully deleted shortened URL for '{db_url.target_url}'"
        }
    else:
        # Raise an HTTPException if the shortened URL is not found.
        raise_not_found(request)
