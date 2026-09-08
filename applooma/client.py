"""HTTP client for the AppLooma RTC control-plane API."""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Optional


class AppApiError(Exception):
    """Raised when the AppLooma RTC API returns an error response."""

    def __init__(self, status: int, message: str, code: Optional[str] = None):
        super().__init__(message)
        self.status = status
        self.code = code


class AppServerClient:
    """Server-side client. Never use your API secret in client apps."""

    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.applooma.dev/v1"):
        if not api_key or not api_secret:
            raise ValueError("AppServerClient: api_key and api_secret are required")
        self._api_key = api_key
        self._api_secret = api_secret
        self._base_url = base_url.rstrip("/")

    def create_token(
        self,
        room_name: str,
        identity: str,
        role: str = "host",
        metadata: Optional[dict] = None,
    ) -> dict:
        """Issue a join token for one participant.

        Returns: {"token", "wsUrl", "roomName", "expiresAt"}
        """
        body: dict[str, Any] = {"roomName": room_name, "identity": identity, "role": role}
        if metadata is not None:
            body["metadata"] = metadata
        return self._request("POST", "/token", body)

    def list_rooms(self) -> list:
        """List your app's live rooms."""
        return self._request("GET", "/rooms").get("rooms", [])

    def list_participants(self, room_name: str) -> list:
        """List participants currently in a room."""
        path = f"/rooms/{urllib.parse.quote(room_name, safe='')}/participants"
        return self._request("GET", path).get("participants", [])

    def _request(self, method: str, path: str, body: Optional[dict] = None) -> dict:
        req = urllib.request.Request(
            self._base_url + path,
            method=method,
            data=json.dumps(body).encode() if body is not None else None,
            headers={
                "content-type": "application/json",
                "x-applooma-key": self._api_key,
                "x-applooma-secret": self._api_secret,
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as res:
                return json.loads(res.read().decode() or "{}")
        except urllib.error.HTTPError as e:
            try:
                data = json.loads(e.read().decode() or "{}")
            except json.JSONDecodeError:
                data = {}
            raise AppApiError(e.code, data.get("error", f"Request failed ({e.code})"), data.get("code")) from None
