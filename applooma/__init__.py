"""AppLooma RTC Server SDK for Python — © AppLooma LLC

    from applooma import AppServerClient

    applooma = AppServerClient(api_key="...", api_secret="...")
    res = applooma.create_token(room_name="room1", identity="user1", role="host")
    # res["token"], res["wsUrl"]
"""

from .client import AppApiError, AppServerClient

__all__ = ["AppServerClient", "AppApiError"]
__version__ = "0.1.0"
