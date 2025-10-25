import json
from typing import Any, Dict, Optional

import requests


class HttpClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 27772, *, timeout_seconds: float = 10.0, session: Optional[requests.Session] = None) -> None:
        self.host = host
        self.port = port
        self.timeout_seconds = timeout_seconds
        self._session = session or requests.Session()
        self._version_checked: bool = False
        self._supported: bool = False
        self._version_text: str = ""

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"

    def get_json(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # 版本兼容：除 /version 外，其它请求在不支持时直接返回统一提示
        if path != "/version":
            self._ensure_version()
            if not self._supported:
                return {"result": "PySFS only supports SFSControl v1.2 and above"}
        url = f"{self.base_url}{path}"
        resp = self._session.get(url, params=params or {}, timeout=self.timeout_seconds)
        resp.raise_for_status()
        return resp.json()

    def post_json(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        # 版本兼容：所有控制/POST接口在不支持时直接返回统一提示
        if path != "/version":
            self._ensure_version()
            if not self._supported:
                return {"result": "PySFS only supports SFSControl v1.2 and above"}
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

    # 内部：获取并缓存服务端版本，设置是否受支持
    def _ensure_version(self) -> None:
        if self._version_checked:
            return
        self._version_checked = True
        try:
            data = self.get_json("/version")
            ver = str(data.get("version", ""))
            self._version_text = ver
            self._supported = self._is_version_supported(ver)
        except Exception:
            self._supported = False

    @staticmethod
    def _is_version_supported(ver: str) -> bool:
        # 解析 x.y[.z]，x.y >= 1.2 视为支持
        try:
            parts = [int(p) for p in str(ver).split(".") if p.isdigit() or (p and p[0].isdigit())]
            while len(parts) < 2:
                parts.append(0)
            major, minor = parts[0], parts[1]
            if major > 1:
                return True
            if major == 1 and minor >= 2:
                return True
            return False
        except Exception:
            return False