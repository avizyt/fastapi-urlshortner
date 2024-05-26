# URL Shortener Project using FastAPI

A fully functional API to shorten URLs.

## Features

* Shorten URLs
* Get the administration info of a shortened URL
* Delete a shortened URL by its secret key
* Get the number of clicks of a shortened URL

## Usage

### Shorten a URL

POST /url

### Get the administration info of a shortened URL

GET /admin/{secret_key}

### Delete a shortened URL by its secret key

DELETE /admin/{secret_key}

### Get the number of clicks of a shortened URL

GET /{url_key}
