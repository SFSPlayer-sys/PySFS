import json
from typing import Any, Dict, List, Optional, Union, Callable

import requests

from .http import HttpClient
from .control import ControlAPI
from .info import InfoAPI
from .values import ValuesAPI
from .calc import CalcAPI
from .draw import DrawAPI


class SFSClient:
    """
    客户端：组合 HTTP、控制、信息与数值提取四个模块。
    - http: 基础 HTTP 能力（GET/POST、screenshot）
    - control_api: 控制接口（/control, /rcall + 动态分发）
    - info_api: 信息端点（/rocket, /planet 等）
    - values_api: 小函数，仅返回单一关键字段（如高度）

    说明：为避免重复，本类仅提供必要属性/入口，并将实际功能委托给子模块；
    未知方法将动态转发到 control_api，保持 sfs.UsePart(0) 等便捷写法。
    """

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 27772,
        *,
        timeout_seconds: float = 10.0,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.http = HttpClient(host=host, port=port, timeout_seconds=timeout_seconds, session=session)
        self.control_api = ControlAPI(self.http)
        self.info_api = InfoAPI(self.http)
        self.values_api = ValuesAPI(self.info_api)
        self.calc_api = CalcAPI(self.info_api)
        self.draw_api = DrawAPI(self.http)
        # 预热一次版本（不强制，首次调用时也会检查）
        try:
            _ = self.info_api.version()
        except Exception:
            pass

    @property
    def host(self) -> str:
        return self.http.host

    @host.setter
    def host(self, value: str) -> None:
        self.http.host = value

    @property
    def port(self) -> int:
        return self.http.port

    @port.setter
    def port(self, value: int) -> None:
        self.http.port = value


    def __getattr__(self, name: str) -> Callable[..., Union[str, Dict[str, Any]]]:
        return getattr(self.control_api, name)


    def screenshot(self) -> bytes:
        return self.http.screenshot()

