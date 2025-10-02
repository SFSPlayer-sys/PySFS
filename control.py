from typing import Any, Dict, List, Optional, Union, Callable

from .http import HttpClient


class ControlAPI:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    def control(self, method: str, *args: Any) -> Union[str, Dict[str, Any]]:
        payload = {"method": method, "args": list(args)}
        result = self.http.post_json("/control", payload)
        if isinstance(result, dict) and "result" in result and len(result) == 1:
            return result["result"]
        if isinstance(result, str):
            return result
        return result
    # 自定义操作：指定方法名与参数列表（按顺序传递）。
    # 等价于 /control {"method": method, "args": [...]}。
    def call(self, method: str, args: Optional[List[Any]] = None) -> Union[str, Dict[str, Any]]:
        return self.control(method, *(args or []))

    def custom(self, method: str, *args: Any) -> Union[str, Dict[str, Any]]:
        return self.control(method, *args)

    # 动态分发：兼容大小写、下划线、驼峰
    def __getattr__(self, name: str) -> Callable[..., Union[str, Dict[str, Any]]]:
        def candidates(n: str) -> List[str]:
            opts: List[str] = [n]
            if n:
                opts.append(n[:1].upper() + n[1:])
            if "_" in n:
                parts = [p for p in n.split("_") if p]
                opts.append("".join(p.capitalize() for p in parts))
                opts.append(parts[0].lower() + "".join(p.capitalize() for p in parts[1:]))
            opts.append(n.lower())
            opts.append(n.upper())
            if n.lower() != n:
                ln = n.lower()
                opts.append(ln[:1].upper() + ln[1:])
                if "_" in ln:
                    parts = [p for p in ln.split("_") if p]
                    opts.append("".join(p.capitalize() for p in parts))
            seen = set()
            out: List[str] = []
            for s in opts:
                if s not in seen:
                    seen.add(s)
                    out.append(s)
            return out

        cand = candidates(name)

        def caller(*args: Any) -> Union[str, Dict[str, Any]]:
            last: Union[str, Dict[str, Any]] = "Error: Unknown method"
            for m in cand:
                res = self.control(m, *args)
                if isinstance(res, str) and "Unknown method" in res:
                    last = res
                    continue
                return res
            return last

        return caller

    #设置节流阀
    def set_throttle(self, value: float, rocket: Optional[Union[int, str]] = None) -> Union[str, Dict[str, Any]]:
        return self.control("SetThrottle", float(value), None if rocket is None else str(rocket))
    #设置RCS
    def set_rcs(self, on: bool, rocket: Optional[Union[int, str]] = None) -> Union[str, Dict[str, Any]]:
        return self.control("SetRCS", bool(on), None if rocket is None else str(rocket))
    #分级
    def stage(self, rocket: Optional[Union[int, str]] = None) -> Union[str, Dict[str, Any]]:
        return self.control("Stage", None if rocket is None else str(rocket))
    #旋转
    def rotate(self, mode_or_angle: Union[str, float, int], offset: float = 0.0, rocket: Optional[Union[int, str]] = None) -> Union[str, Dict[str, Any]]:
        return self.control("Rotate", mode_or_angle, float(offset), None if rocket is None else str(rocket))
    #停止旋转
    def stop_rotate(self, rocket: Optional[Union[int, str]] = None, stop_coroutine: bool = True) -> Union[str, Dict[str, Any]]:
        return self.control("StopRotate", None if rocket is None else str(rocket), bool(stop_coroutine))
    #设置旋转角度
    def set_rotation(self, angle: float, rocket: Optional[Union[int, str]] = None) -> Union[str, Dict[str, Any]]:
        return self.control("SetRotation", float(angle), None if rocket is None else str(rocket))
    #RCS推
    def rcs_thrust(self, direction: str, seconds: float, rocket: Optional[Union[int, str]] = None) -> Union[str, Dict[str, Any]]:
        return self.control("RcsThrust", direction, float(seconds), None if rocket is None else str(rocket))
    #主引擎开关
    def set_main_engine_on(self, on: bool, rocket: Optional[Union[int, str]] = None) -> Union[str, Dict[str, Any]]:
        return self.control("SetMainEngineOn", bool(on), None if rocket is None else str(rocket))
    #使用部件
    def use_part(self, part_id: int, rocket: Optional[Union[int, str]] = None) -> Union[str, Dict[str, Any]]:
        return self.control("UsePart", int(part_id), None if rocket is None else str(rocket))
    #发射
    def launch(self) -> Union[str, Dict[str, Any]]:
        return self.control("Launch")
    #切换火箭
    def switch_rocket(self, id_or_name: Union[int, str]) -> Union[str, Dict[str, Any]]:
        return self.control("SwitchRocket", id_or_name)
    #重命名火箭
    def rename_rocket(self, id_or_name: Union[int, str], new_name: str) -> Union[str, Dict[str, Any]]:
        return self.control("RenameRocket", id_or_name, new_name)
    #设置目标
    def set_target(self, name_or_index: Union[int, str]) -> Union[str, Dict[str, Any]]:
        return self.control("SetTarget", name_or_index)
    #清除目标
    def clear_target(self) -> Union[str, Dict[str, Any]]:
        return self.control("ClearTarget")
    #建造
    def build(self, blueprint_info: str) -> Union[str, Dict[str, Any]]:
        return self.control("Build", blueprint_info)
    #清除蓝图
    def clear_blueprint(self) -> Union[str, Dict[str, Any]]:
        return self.control("ClearBlueprint")
    #切换到建造场景
    def switch_to_build(self) -> Union[str, Dict[str, Any]]:
        return self.control("SwitchToBuild")
    #清除垃圾
    def clear_debris(self) -> Union[str, Dict[str, Any]]:
        return self.control("ClearDebris")
    #添加分级
    def add_stage(self, index: int, part_ids: List[int], rocket: Optional[Union[int, str]] = None) -> Union[str, Dict[str, Any]]:
        return self.control("AddStage", int(index), list(map(int, part_ids)), None if rocket is None else str(rocket))
    #移除分级
    def remove_stage(self, index: int, rocket: Optional[Union[int, str]] = None) -> Union[str, Dict[str, Any]]:
        return self.control("RemoveStage", int(index), None if rocket is None else str(rocket))
    #设置轨道
    def set_orbit(self, radius: float, eccentricity: Optional[float] = None, true_anomaly: Optional[float] = None,
                  counterclockwise: Optional[bool] = None, planet_code: Optional[str] = None,
                  rocket: Optional[Union[int, str]] = None) -> Union[str, Dict[str, Any]]:
        return self.control("SetOrbit", float(radius), None if eccentricity is None else float(eccentricity),
                            None if true_anomaly is None else float(true_anomaly),
                            None if counterclockwise is None else bool(counterclockwise),
                            planet_code, None if rocket is None else str(rocket))
    #设置状态
    def set_state(self, x: Optional[float] = None, y: Optional[float] = None, vx: Optional[float] = None, vy: Optional[float] = None,
                  angular_velocity: Optional[float] = None, blueprint_json: Optional[str] = None,
                  rocket: Optional[Union[int, str]] = None) -> Union[str, Dict[str, Any]]:
        return self.control("SetState", None if x is None else float(x), None if y is None else float(y),
                            None if vx is None else float(vx), None if vy is None else float(vy),
                            None if angular_velocity is None else float(angular_velocity), blueprint_json,
                            None if rocket is None else str(rocket))
    #删除火箭
    def delete_rocket(self, id_or_name: Optional[Union[int, str]] = None) -> Union[str, Dict[str, Any]]:
        return self.control("DeleteRocket", None if id_or_name is None else id_or_name)
    #创建火箭
    def create_rocket(self, planet_code: str, blueprint_json: str, rocket_name: Optional[str] = None,
                      x: Optional[float] = None, y: Optional[float] = None,
                      vx: Optional[float] = None, vy: Optional[float] = None,
                      vr: Optional[float] = None) -> Union[str, Dict[str, Any]]:
        return self.control("CreateRocket", planet_code, blueprint_json, rocket_name,
                            None if x is None else float(x), None if y is None else float(y),
                            None if vx is None else float(vx), None if vy is None else float(vy),
                            None if vr is None else float(vr))
    #转移燃料
    def transfer_fuel(self, from_tank_id: int, to_tank_id: int, rocket: Optional[Union[int, str]] = None) -> Union[str, Dict[str, Any]]:
        return self.control("TransferFuel", int(from_tank_id), int(to_tank_id), None if rocket is None else str(rocket))
    #停止转移燃料
    def stop_fuel_transfer(self, rocket: Optional[Union[int, str]] = None) -> Union[str, Dict[str, Any]]:
        return self.control("StopFuelTransfer", None if rocket is None else str(rocket))
    #车轮控制
    def wheel_control(self, enable: Optional[bool] = None, turn_axis: Optional[float] = None,
                      rocket: Optional[Union[int, str]] = None) -> Union[str, Dict[str, Any]]:
        return self.control("WheelControl", None if enable is None else bool(enable),
                            None if turn_axis is None else float(turn_axis), None if rocket is None else str(rocket))

    # 时间与地图
    def set_timewarp(self, speed: float, realtime_physics: Optional[bool] = None, show_message: Optional[bool] = None) -> Union[str, Dict[str, Any]]:
        return self.control("SetTimewarp", float(speed),
                            None if realtime_physics is None else bool(realtime_physics),
                            None if show_message is None else bool(show_message))
    #时间加速
    def timewarp_plus(self) -> Union[str, Dict[str, Any]]:
        return self.control("TimewarpPlus")
    #时间减速
    def timewarp_minus(self) -> Union[str, Dict[str, Any]]:
        return self.control("TimewarpMinus")
    #切换地图视图
    def switch_map_view(self, on: Optional[bool] = None) -> Union[str, Dict[str, Any]]:
        return self.control("SwitchMapView", None if on is None else bool(on))
    #跟踪
    def track(self, name_or_index: Union[int, str]) -> Union[str, Dict[str, Any]]:
        return self.control("Track", name_or_index)
    #取消跟踪
    def unfocus(self) -> Union[str, Dict[str, Any]]:
        return self.control("Unfocus")
    #作弊
    def set_cheat(self, cheat_name: str, value: bool) -> Union[str, Dict[str, Any]]:
        return self.control("SetCheat", cheat_name, bool(value))
    #回退
    def revert(self, revert_type: str) -> Union[str, Dict[str, Any]]:
        return self.control("Revert", revert_type)
    #完成挑战
    def complete_challenge(self, challenge_id: str) -> Union[str, Dict[str, Any]]:
        return self.control("CompleteChallenge", challenge_id)
    #等待窗口
    def wait_for_window(self, mode: Optional[str] = None, parameter: Optional[float] = None) -> Union[str, Dict[str, Any]]:
        return self.control("WaitForWindow", mode, None if parameter is None else float(parameter))
    #显示提示
    def show_toast(self, toast: str) -> Union[str, Dict[str, Any]]:
        return self.control("ShowToast", toast)
    #日志
    def log_message(self, msg_type: str, message: str) -> Union[str, Dict[str, Any]]:
        return self.control("LogMessage", msg_type, message)
    #存档管理
    def quicksave_manager(self, operation: Optional[str] = None, name: Optional[str] = None) -> Union[str, Dict[str, Any]]:
        return self.control("QuicksaveManager", operation, name)
    #设置地图图标颜色
    def set_map_icon_color(self, rgba_value: str, rocket: Optional[Union[int, str]] = None) -> Union[str, Dict[str, Any]]:
        return self.control("SetMapIconColor", rgba_value, None if rocket is None else str(rocket))
    #获取火箭信息
    def get_rocket_info(self, rocket: Optional[Union[int, str]] = None) -> Union[str, Dict[str, Any]]:
        return self.control("GetRocketInfo", None if rocket is None else str(rocket))
    #获取火箭列表
    def get_rocket_list(self) -> Union[str, Dict[str, Any]]:
        return self.control("GetRocketList")
    #获取世界信息
    def get_world_info(self) -> Union[str, Dict[str, Any]]:
        return self.control("GetWorldInfo")