"""Lio Live Server SDK for Python — © AppLooma LLC

    from liolive import LioServerClient

    lio = LioServerClient(api_key="...", api_secret="...")
    res = lio.create_token(room_name="room1", identity="user1", role="host")
    # res["token"], res["wsUrl"]
"""

from .client import LioApiError, LioServerClient

__all__ = ["LioServerClient", "LioApiError"]
__version__ = "0.1.0"
