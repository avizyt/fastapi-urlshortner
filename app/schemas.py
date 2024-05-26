from pydantic import BaseModel


class URLBase(BaseModel):
    """
    Base model for the URL.

    Attributes:
        target_url (str): The target URL.
    """

    target_url: str


class URL(URLBase):
    """
    Model for the URL.

    Attributes:
        is_active (bool): Whether the URL is active.
        clicks (int): The number of clicks.
    """

    is_active: bool
    clicks: int

    class Config:
        from_attributes = True


class URLInfo(URL):
    """
    Model for the URL info.

    Attributes:
        url (str): The URL.
        admin_url (str): The admin URL.
    """

    url: str
    admin_url: str
