from typing import Any, Dict, List, Optional, Union

from .http import HttpClient


class InfoAPI:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    def rocket_sim(self, rocket: Optional[Union[int, str]] = None) -> Dict[str, Any]:
        """
        获取火箭的仿真信息
        对应：GET /rocket_sim?rocketIdOrName=xxx
        """
        params: Dict[str, Any] = {}
        if rocket is not None:
            params["rocketIdOrName"] = str(rocket)
        return self.http.get_json("/rocket_sim", params)

    def rocket_save(self, rocket: Optional[Union[int, str]] = None) -> Dict[str, Any]:
        """
        获取单个火箭的保存信息（RocketSave）
        对应：GET /rocket?rocketIdOrName=xxx
        """
        params: Dict[str, Any] = {}
        if rocket is not None:
            params["rocketIdOrName"] = str(rocket)
        return self.http.get_json("/rocket", params)

    def rockets(self) -> List[Dict[str, Any]]:
        """
        获取当前场景中所有火箭的保存信息列表
        对应：GET /rockets
        """
        data = self.http.get_json("/rockets")
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "rockets" in data and isinstance(data["rockets"], list):
            return data["rockets"]
        return [data]

    def planet(self, codename: Optional[str] = None) -> Dict[str, Any]:
        """
        获取当前或指定星球的信息
        对应：GET /planet?codename=xxx
        """
        params: Dict[str, Any] = {}
        if codename:
            params["codename"] = codename
        return self.http.get_json("/planet", params)

    def planets(self) -> List[Dict[str, Any]]:
        """
        获取所有星球的信息列表
        对应：GET /planets
        """
        data = self.http.get_json("/planets")
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "planets" in data and isinstance(data["planets"], list):
            return data["planets"]
        return [data]

    def other(self, rocket: Optional[Union[int, str]] = None) -> Dict[str, Any]:
        """
        获取其它杂项信息
        对应：GET /other?rocketIdOrName=xxx
        """
        params: Dict[str, Any] = {}
        if rocket is not None:
            params["rocketIdOrName"] = str(rocket)
        return self.http.get_json("/other", params)

    def mission(self) -> Dict[str, Any]:
        """
        获取任务/挑战相关信息
        对应：GET /mission
        """
        return self.http.get_json("/mission")

    def debug_log(self) -> Dict[str, Any]:
        """
        获取游戏中的调试日志
        对应：GET /debuglog
        """
        return self.http.get_json("/debuglog")

    def version(self) -> Dict[str, Any]:
        """
        获取 SFSControl 版本信息
        对应：GET /version
        """
        return self.http.get_json("/version")

    def parts_info(self, rocket: Optional[Union[int, str]] = None) -> Dict[str, Any]:
        """
        获取火箭的部件信息
        对应：GET /rocket_sim?rocketIdOrName=xxx 中的parts字段
        """
        data = self.rocket_sim(rocket)
        if isinstance(data, dict) and "parts" in data:
            return data["parts"]
        return {}

    def parts_list(self, rocket: Optional[Union[int, str]] = None) -> List[Dict[str, Any]]:
        """
        获取火箭的部件列表，包含ID和名称
        返回格式：[{"id": int, "name": str, ...}, ...]
        """
        parts_info = self.parts_info(rocket)
        if isinstance(parts_info, list):
            return parts_info
        return []