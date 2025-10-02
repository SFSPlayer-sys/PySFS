import json
from typing import Any, Dict, Optional

import requests


class HttpClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 27772, *, timeout_seconds: float = 10.0, session: Optional[requests.Session] = None) -> None:
        self.host = host
        self.port = port
        self.timeout_seconds = timeout_seconds
        self._session = session or requests.Session()

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"

    def get_json(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        resp = self._session.get(url, params=params or {}, timeout=self.timeout_seconds)
        resp.raise_for_status()
        return resp.json()

    def post_json(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        resp = self._session.post(url, json=payload, timeout=self.timeout_seconds)
        resp.raise_for_status()
        if resp.headers.get("Content-Type", "").startswith("application/json"):
            return resp.json()
        text = resp.text
        try:
            return json.loads(text)
        except Exception:
            return {"result": text}

    def screenshot(self) -> bytes:
        url = f"{self.base_url}/screenshot"
        resp = self._session.get(url, timeout=self.timeout_seconds)
        resp.raise_for_status()
        return resp.content