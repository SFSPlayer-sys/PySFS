from typing import Any, Dict, List, Optional, Union
import math

from .info import InfoAPI


def _as_float(x: Any) -> Optional[float]:
    try:
        return float(x)
    except Exception:
        return None


def _as_int(x: Any) -> Optional[int]:
    try:
        return int(x)
    except Exception:
        return None


def _as_bool(x: Any) -> Optional[bool]:
    try:
        return bool(x)
    except Exception:
        return None


class ValuesAPI:
    def __init__(self, info: InfoAPI) -> None:
        self.info = info
        self._version = None

    def _get_version(self) -> Optional[str]:
        """获取SFSControl版本号"""
        if self._version is None:
            version_data = self.info.version()
            if isinstance(version_data, dict) and "version" in version_data:
                self._version = str(version_data["version"])
            else:
                self._version = "0.0"
        return self._version

    def _check_version(self, required_version: str) -> bool:
        """检查版本是否满足要求"""
        current_version = self._get_version()
        if not current_version:
            return False
        
        try:
            current_parts = [int(x) for x in current_version.split('.')]
            required_parts = [int(x) for x in required_version.split('.')]
            
            # 补齐版本号长度
            while len(current_parts) < len(required_parts):
                current_parts.append(0)
            while len(required_parts) < len(current_parts):
                required_parts.append(0)
            
            return current_parts >= required_parts
        except:
            return False

    def rocket_name(self, rocket: Optional[Union[int, str]] = None) -> Optional[str]:
        data = self.info.rocket_sim(rocket)
        if isinstance(data, dict) and "name" in data and data["name"] is not None:
            return str(data["name"])
        data2 = self.info.rocket_save(rocket)
        if isinstance(data2, dict) and "rocketName" in data2 and data2["rocketName"] is not None:
            return str(data2["rocketName"])
        return None

    def rocket_id(self, rocket: Optional[Union[int, str]] = None) -> Optional[int]:
        data = self.info.rocket_sim(rocket)
        if isinstance(data, dict):
            return _as_int(data.get("id"))
        return None

    def rocket_altitude(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        data = self.info.rocket_sim(rocket)
        if isinstance(data, dict) and "height" in data:
            v = _as_float(data["height"])
            if v is not None:
                return v
        data2 = self.info.rocket_save(rocket)
        if isinstance(data2, dict) and "height" in data2:
            return _as_float(data2["height"])  # 若服务端包含该字段
        return None

    def rocket_position(self, rocket: Optional[Union[int, str]] = None) -> Optional[Dict[str, float]]:
        data = self.info.rocket_save(rocket)
        if isinstance(data, dict):
            location = data.get("location")
            if isinstance(location, dict):
                pos = location.get("position")
                if isinstance(pos, dict) and "x" in pos and "y" in pos:
                    return {"x": _as_float(pos["x"]) or 0.0, "y": _as_float(pos["y"]) or 0.0}
        return None

    def rocket_rotation(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        data = self.info.rocket_sim(rocket)
        if isinstance(data, dict) and "rotation" in data:
            v = _as_float(data["rotation"])
            if v is not None:
                return v
        data2 = self.info.rocket_save(rocket)
        if isinstance(data2, dict) and "rotation" in data2:
            return _as_float(data2["rotation"])
        return None

    def rocket_longitude(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        r = self.info.rocket_save(rocket)
        try:
            pos = r.get("location", {}).get("position", {}) if isinstance(r, dict) else {}
            if isinstance(pos, dict) and "AngleDegrees" in pos and pos["AngleDegrees"] is not None:
                # 规范化到 [0, 360)
                ang = float(pos["AngleDegrees"]) % 360.0
                if ang < 0:
                    ang += 360.0
                return ang
        except Exception as e:
            pass
        return None

    

    def rocket_angular_velocity(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        data = self.info.rocket_sim(rocket)
        if isinstance(data, dict):
            return _as_float(data.get("angularVelocity"))
        return None

    def rocket_throttle(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        data = self.info.rocket_sim(rocket)
        if isinstance(data, dict) and "throttle" in data:
            v = _as_float(data["throttle"])
            if v is not None:
                return v
        data2 = self.info.rocket_save(rocket)
        if isinstance(data2, dict) and "throttlePercent" in data2:
            return _as_float(data2["throttlePercent"])
        return None

    def rocket_rcs_on(self, rocket: Optional[Union[int, str]] = None) -> Optional[bool]:
        data = self.info.rocket_sim(rocket)
        if isinstance(data, dict) and "rcs" in data:
            return _as_bool(data["rcs"])
        data2 = self.info.rocket_save(rocket)
        if isinstance(data2, dict) and "RCS" in data2:
            return _as_bool(data2["RCS"])
        return None

    def rocket_orbit(self, rocket: Optional[Union[int, str]] = None) -> Optional[Dict[str, Any]]:
        data = self.info.rocket_sim(rocket)
        if isinstance(data, dict) and isinstance(data.get("orbit"), dict):
            return data["orbit"]
        return None

    def rocket_orbit_apoapsis(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        o = self.rocket_orbit(rocket)
        return _as_float(o.get("apoapsis")) if isinstance(o, dict) else None

    def rocket_orbit_periapsis(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        o = self.rocket_orbit(rocket)
        return _as_float(o.get("periapsis")) if isinstance(o, dict) else None

    def rocket_orbit_period(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        o = self.rocket_orbit(rocket)
        return _as_float(o.get("period")) if isinstance(o, dict) else None

    def rocket_orbit_true_anomaly(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        o = self.rocket_orbit(rocket)
        return _as_float(o.get("trueAnomaly")) if isinstance(o, dict) else None

    def rocket_parent_planet_code(self, rocket: Optional[Union[int, str]] = None) -> Optional[str]:
        data = self.info.rocket_sim(rocket)
        if isinstance(data, dict) and data.get("parentPlanetCode") is not None:
            return str(data["parentPlanetCode"])
        return None

    def other_target_angle(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        data = self.info.other(rocket)
        return _as_float(data.get("targetAngle")) if isinstance(data, dict) else None

    def other_quicksaves(self, rocket: Optional[Union[int, str]] = None) -> Optional[List[Any]]:
        data = self.info.other(rocket)
        return data.get("quicksaves") if isinstance(data, dict) else None

    def other_nav_target(self, rocket: Optional[Union[int, str]] = None) -> Any:
        data = self.info.other(rocket)
        return data.get("navTarget") if isinstance(data, dict) else None

    def other_timewarp_speed(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        data = self.info.other(rocket)
        return _as_float(data.get("timewarpSpeed")) if isinstance(data, dict) else None

    def other_world_time(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        data = self.info.other(rocket)
        return _as_float(data.get("worldTime")) if isinstance(data, dict) else None

    def other_scene_name(self, rocket: Optional[Union[int, str]] = None) -> Optional[str]:
        data = self.info.other(rocket)
        v = data.get("sceneName") if isinstance(data, dict) else None
        return str(v) if v is not None else None

    def other_transfer_window_delta_v(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        data = self.info.other(rocket)
        return _as_float(data.get("transferWindowDeltaV")) if isinstance(data, dict) else None

    def other_mission_status(self, rocket: Optional[Union[int, str]] = None) -> Any:
        data = self.info.other(rocket)
        return data.get("missionStatus") if isinstance(data, dict) else None

    def other_mass(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        data = self.info.other(rocket)
        return _as_float(data.get("mass")) if isinstance(data, dict) else None

    def other_thrust(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        data = self.info.other(rocket)
        return _as_float(data.get("thrust")) if isinstance(data, dict) else None

    def other_max_thrust(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        data = self.info.other(rocket)
        return _as_float(data.get("maxThrust")) if isinstance(data, dict) else None

    def other_twr(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        data = self.info.other(rocket)
        return _as_float(data.get("TWR")) if isinstance(data, dict) else None

    def other_dist_to_apoapsis(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        data = self.info.other(rocket)
        return _as_float(data.get("distToApoapsis")) if isinstance(data, dict) else None

    def other_dist_to_periapsis(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        data = self.info.other(rocket)
        return _as_float(data.get("distToPeriapsis")) if isinstance(data, dict) else None

    def other_time_to_apoapsis(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        data = self.info.other(rocket)
        return _as_float(data.get("timeToApoapsis")) if isinstance(data, dict) else None

    def other_time_to_periapsis(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        data = self.info.other(rocket)
        return _as_float(data.get("timeToPeriapsis")) if isinstance(data, dict) else None

    def other_inertia_info(self, rocket: Optional[Union[int, str]] = None) -> Optional[Dict[str, Any]]:
        data = self.info.other(rocket)
        return data.get("inertia") if isinstance(data, dict) else None
    
    def current_planet_code(self, rocket: Optional[Union[int, str]] = None) -> Optional[str]:
        data = self.info.rocket_sim(rocket)
        return data.get("planetCode") if isinstance(data, dict) else None

    def other_gravity_info(self, rocket: Optional[Union[int, str]] = None) -> Optional[Dict[str, float]]:
        """
        获取火箭当前受到的重力信息
        返回格式：{"gravityX": float, "gravityY": float, "gravityMagnitude": float}
        需要SFSControl版本 >= 1.3
        """
        if not self._check_version("1.3"):
            return None
        data = self.info.other(rocket)
        if isinstance(data, dict) and isinstance(data.get("gravity"), dict):
            gravity = data["gravity"]
            return {
                "gravityX": _as_float(gravity.get("gravityX")) or 0.0,
                "gravityY": _as_float(gravity.get("gravityY")) or 0.0,
                "gravityMagnitude": _as_float(gravity.get("gravityMagnitude")) or 0.0
            }
        return None

    def other_gravity_x(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        """获取火箭当前受到的X方向重力分量"""
        gravity_info = self.other_gravity_info(rocket)
        return gravity_info.get("gravityX") if gravity_info else None

    def other_gravity_y(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        """获取火箭当前受到的Y方向重力分量"""
        gravity_info = self.other_gravity_info(rocket)
        return gravity_info.get("gravityY") if gravity_info else None

    def other_gravity_magnitude(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        """获取火箭当前受到的总重力大小"""
        gravity_info = self.other_gravity_info(rocket)
        return gravity_info.get("gravityMagnitude") if gravity_info else None
    
    def other_landing_point(self, rocket: Optional[Union[int, str]] = None) -> Optional[Dict[str, Any]]:
        """
        获取火箭的落点预测信息（修正嵌套路径）
        返回包含落点坐标、角度、高度等信息的字典
        """
        if not self._check_version("1.3"):
             return None
        data = self.info.other(rocket)
        if isinstance(data, dict):
            # 解析到内层 landingPoint
            outer_landing = data.get("landingPoint", {})  # 外层 landingPoint
            if isinstance(outer_landing, dict):
                inner_landing = outer_landing.get("landingPoint", {})  # 内层 landingPoint
                if inner_landing:  # 确保内层数据存在
                    return inner_landing
        return None

    def other_landing_point_position(self, rocket: Optional[Union[int, str]] = None) -> Optional[Dict[str, float]]:
        """获取落点的2D坐标"""
        landing_point = self.other_landing_point(rocket)
        if isinstance(landing_point, dict) and "x" in landing_point and "y" in landing_point:
            return {
                "x": _as_float(landing_point.get("x")) or 0.0,
                "y": _as_float(landing_point.get("y")) or 0.0
            }
        return None

    def other_landing_point_angle(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        """获取落点相对于星球中心的角度（度数）"""
        landing_point = self.other_landing_point(rocket)
        return _as_float(landing_point.get("angle")) if isinstance(landing_point, dict) else None

    def other_landing_point_height(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        """获取落点距离星球表面的高度"""
        landing_point = self.other_landing_point(rocket)
        return _as_float(landing_point.get("height")) if isinstance(landing_point, dict) else None

    def other_landing_point_radius(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        """获取落点到星球中心的距离"""
        landing_point = self.other_landing_point(rocket)
        return _as_float(landing_point.get("radius")) if isinstance(landing_point, dict) else None

    def other_landing_point_planet(self, rocket: Optional[Union[int, str]] = None) -> Optional[str]:
        """获取落点所在的星球代码名"""
        landing_point = self.other_landing_point(rocket)
        if isinstance(landing_point, dict) and "planet" in landing_point:
            return str(landing_point["planet"])
        return None

    def other_landing_point_success(self, rocket: Optional[Union[int, str]] = None) -> Optional[bool]:
        """检查落点计算是否成功"""
        landing_point = self.other_landing_point(rocket)
        return _as_bool(landing_point.get("success")) if isinstance(landing_point, dict) else None

    def other_landing_point_steps(self, rocket: Optional[Union[int, str]] = None) -> Optional[int]:
        """获取落点计算使用的仿真步数"""
        landing_point = self.other_landing_point(rocket)
        return _as_int(landing_point.get("steps")) if isinstance(landing_point, dict) else None

    def other_fuel_bar_groups(self, rocket: Optional[Union[int, str]] = None) -> Optional[List[Dict[str, Any]]]:
        """
        获取燃料组信息
        返回格式：[{"type": str, "current": float, "max": float, "percent": float}, ...]
        """
        data = self.info.other(rocket)
        if isinstance(data, dict) and isinstance(data.get("fuelBarGroups"), list):
            return data["fuelBarGroups"]
        return None

    def other_mission_log(self, rocket: Optional[Union[int, str]] = None) -> Optional[List[Dict[str, Any]]]:
        """
        获取任务日志
        返回格式：[{"text": str, "reward": Any, "logId": str}, ...]
        """
        mission_data = self.info.mission()
        if isinstance(mission_data, dict) and isinstance(mission_data.get("missionLog"), list):
            return mission_data["missionLog"]
        return None

    def other_console_log(self, max_lines: int = 150) -> Optional[List[str]]:
        """
        获取游戏控制台日志
        参数：
        - max_lines: 最大行数，默认150
        返回：日志行列表
        """
        log_data = self.info.debug_log()
        if isinstance(log_data, dict) and isinstance(log_data.get("log"), list):
            return log_data["log"]
        return None

    def other_quicksave_names(self, rocket: Optional[Union[int, str]] = None) -> Optional[List[str]]:
        """
        获取快速保存名称列表
        返回：快速保存名称列表
        """
        quicksaves = self.other_quicksaves(rocket)
        if isinstance(quicksaves, list):
            names = []
            for qs in quicksaves:
                if isinstance(qs, dict) and "name" in qs:
                    names.append(str(qs["name"]))
            return names
        return None

    def other_quicksave_times(self, rocket: Optional[Union[int, str]] = None) -> Optional[List[str]]:
        """
        获取快速保存时间列表
        返回：快速保存时间列表（ISO格式字符串）
        """
        quicksaves = self.other_quicksaves(rocket)
        if isinstance(quicksaves, list):
            times = []
            for qs in quicksaves:
                if isinstance(qs, dict) and "time" in qs:
                    times.append(str(qs["time"]))
            return times
        return None

    def other_nav_target_type(self, rocket: Optional[Union[int, str]] = None) -> Optional[str]:
        """
        获取导航目标类型
        返回：目标类型（"planet"或"rocket"）
        """
        nav_target = self.other_nav_target(rocket)
        if isinstance(nav_target, dict) and "type" in nav_target:
            return str(nav_target["type"])
        return None

    def other_nav_target_name(self, rocket: Optional[Union[int, str]] = None) -> Optional[str]:
        """
        获取导航目标名称
        返回：目标名称
        """
        nav_target = self.other_nav_target(rocket)
        if isinstance(nav_target, dict) and "name" in nav_target:
            return str(nav_target["name"])
        return None

    def other_nav_target_code_name(self, rocket: Optional[Union[int, str]] = None) -> Optional[str]:
        """
        获取导航目标代码名
        返回：目标代码名
        """
        nav_target = self.other_nav_target(rocket)
        if isinstance(nav_target, dict) and "codeName" in nav_target:
            return str(nav_target["codeName"])
        return None

    def other_nav_target_id(self, rocket: Optional[Union[int, str]] = None) -> Optional[int]:
        """
        获取导航目标ID（如果是火箭）
        返回：目标ID
        """
        nav_target = self.other_nav_target(rocket)
        if isinstance(nav_target, dict) and "id" in nav_target:
            return _as_int(nav_target["id"])
        return None

    def other_nav_target_soi_planet(self, rocket: Optional[Union[int, str]] = None) -> Optional[str]:
        """
        获取导航目标所在的星球（如果是火箭）
        返回：星球名称
        """
        nav_target = self.other_nav_target(rocket)
        if isinstance(nav_target, dict) and "soiPlanet" in nav_target:
            return str(nav_target["soiPlanet"])
        return None

    def planet_radius(self, codename: Optional[str] = None) -> Optional[float]:
        data = self.info.planet(codename)
        return _as_float(data.get("radius")) if isinstance(data, dict) else None

    def planet_gravity(self, codename: Optional[str] = None) -> Optional[float]:
        data = self.info.planet(codename)
        return _as_float(data.get("gravity")) if isinstance(data, dict) else None

    def planet_soi(self, codename: Optional[str] = None) -> Optional[float]:
        data = self.info.planet(codename)
        return _as_float(data.get("SOI")) if isinstance(data, dict) else None

    def planet_has_atmosphere(self, codename: Optional[str] = None) -> Optional[bool]:
        data = self.info.planet(codename)
        return _as_bool(data.get("hasAtmosphere")) if isinstance(data, dict) else None

    def planet_atmosphere_height(self, codename: Optional[str] = None) -> Optional[float]:
        data = self.info.planet(codename)
        return _as_float(data.get("atmosphereHeight")) if isinstance(data, dict) else None

    def planet_parent(self, codename: Optional[str] = None) -> Optional[str]:
        data = self.info.planet(codename)
        v = data.get("parent") if isinstance(data, dict) else None
        return str(v) if v is not None else None

    def planet_orbit(self, codename: Optional[str] = None) -> Optional[Dict[str, Any]]:
        data = self.info.planet(codename)
        return data.get("orbit") if isinstance(data, dict) else None

    def planet_orbit_eccentricity(self, codename: Optional[str] = None) -> Optional[float]:
        o = self.planet_orbit(codename)
        return _as_float(o.get("eccentricity")) if isinstance(o, dict) else None

    def planet_orbit_semi_major_axis(self, codename: Optional[str] = None) -> Optional[float]:
        o = self.planet_orbit(codename)
        return _as_float(o.get("semiMajorAxis")) if isinstance(o, dict) else None

    def planet_orbit_argument_of_periapsis(self, codename: Optional[str] = None) -> Optional[float]:
        o = self.planet_orbit(codename)
        return _as_float(o.get("argumentOfPeriapsis")) if isinstance(o, dict) else None

    def planet_orbit_current_true_anomaly(self, codename: Optional[str] = None) -> Optional[float]:
        o = self.planet_orbit(codename)
        return _as_float(o.get("currentTrueAnomaly")) if isinstance(o, dict) else None

    def planet_orbit_current_radius(self, codename: Optional[str] = None) -> Optional[float]:
        o = self.planet_orbit(codename)
        return _as_float(o.get("currentRadius")) if isinstance(o, dict) else None

    def planet_orbit_current_velocity(self, codename: Optional[str] = None) -> Optional[float]:
        o = self.planet_orbit(codename)
        return _as_float(o.get("currentVelocity")) if isinstance(o, dict) else None

    def sfscontrol_version(self) -> Optional[str]:
        """
        获取 SFSControl 版本号
        来源：/version.version
        """
        data = self.info.version()
        if isinstance(data, dict) and "version" in data:
            return str(data["version"])
        return None

    def sfscontrol_name(self) -> Optional[str]:
        """
        获取 SFSControl 名称
        来源：/version.name
        """
        data = self.info.version()
        if isinstance(data, dict) and "name" in data:
            return str(data["name"])
        return None

    def sfscontrol_full_info(self) -> Optional[Dict[str, Any]]:
        """
        获取 SFSControl 完整版本信息
        来源：/version
        """
        return self.info.version()

    def part_temperatures(self, rocket: Optional[Union[int, str]] = None) -> Optional[List[Dict[str, float]]]:
        """
        获取部件温度列表（id 与 temperature）。
        来源：/rocket_sim.partTemperatures（服务端由 GetRocketInfo 填充）
        返回格式：[{"id": int, "temperature": float}, ...]，若无数据返回 None。
        """
        data = self.info.rocket_sim(rocket)
        if isinstance(data, dict) and isinstance(data.get("partTemperatures"), list):
            out: List[Dict[str, float]] = []
            for item in data["partTemperatures"]:
                if isinstance(item, dict) and "id" in item and "temperature" in item:
                    pid = _as_int(item["id"])
                    temp = _as_float(item["temperature"])
                    if pid is not None and temp is not None:
                        out.append({"id": pid, "temperature": temp})
            return out
        return None

    def heated_parts_list(self, rocket: Optional[Union[int, str]] = None, min_temperature: float = 0.0) -> Optional[List[Dict[str, Any]]]:
        """
        获取受热部件列表，包含ID、名称和温度
        参数：
        - rocket: 火箭ID或名称，None表示当前火箭
        - min_temperature: 最小温度阈值，只返回温度高于此值的部件
        返回格式：[{"id": int, "name": str, "temperature": float}, ...]，若无数据返回 None
        """
        # 获取部件温度数据
        temp_data = self.part_temperatures(rocket)
        if not temp_data:
            return None
            
        # 获取部件列表数据
        parts_list = self.info.parts_list(rocket)
        if not parts_list:
            return None
            
        # 创建部件ID到名称的映射
        part_id_to_name = {}
        for part in parts_list:
            if isinstance(part, dict) and "id" in part and "name" in part:
                part_id = _as_int(part["id"])
                part_name = part.get("name", "Unknown")
                if part_id is not None:
                    part_id_to_name[part_id] = part_name
        
        # 合并温度数据和部件信息
        heated_parts = []
        for temp_item in temp_data:
            if isinstance(temp_item, dict) and "id" in temp_item and "temperature" in temp_item:
                part_id = _as_int(temp_item["id"])
                temperature = _as_float(temp_item["temperature"])
                
                if part_id is not None and temperature is not None and temperature >= min_temperature:
                    part_name = part_id_to_name.get(part_id, f"Part_{part_id}")
                    heated_parts.append({
                        "id": part_id,
                        "name": part_name,
                        "temperature": temperature
                    })
        
        return heated_parts if heated_parts else None

    def part_temperature_by_id(self, part_id: int, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        """
        根据部件ID获取特定部件的温度
        参数：
        - part_id: 部件ID
        - rocket: 火箭ID或名称，None表示当前火箭
        返回：部件温度，若未找到返回None
        """
        temp_data = self.part_temperatures(rocket)
        if not temp_data:
            return None
            
        for item in temp_data:
            if isinstance(item, dict) and "id" in item and "temperature" in item:
                if _as_int(item["id"]) == part_id:
                    return _as_float(item["temperature"])
        return None

    def part_name_by_id(self, part_id: int, rocket: Optional[Union[int, str]] = None) -> Optional[str]:
        """
        根据部件ID获取部件名称
        参数：
        - part_id: 部件ID
        - rocket: 火箭ID或名称，None表示当前火箭
        返回：部件名称，若未找到返回None
        """
        parts_list = self.info.parts_list(rocket)
        if not parts_list:
            return None
            
        for part in parts_list:
            if isinstance(part, dict) and "id" in part and "name" in part:
                if _as_int(part["id"]) == part_id:
                    return part.get("name", "Unknown")
        return None

    def world_rocket_count(self) -> Optional[int]:
        """
        获取世界内火箭总数
        返回：火箭数量
        """
        rockets = self.info.rockets()
        if isinstance(rockets, list):
            return len(rockets)
        return None

    def rocket_parts_count(self, rocket: Optional[Union[int, str]] = None) -> Optional[int]:
        """
        获取指定火箭的部件数量
        参数：
        - rocket: 火箭ID或名称，None表示当前火箭
        返回：部件数量
        """
        parts_list = self.info.parts_list(rocket)
        if isinstance(parts_list, list):
            return len(parts_list)
        return None

    def rocket_parts_names(self, rocket: Optional[Union[int, str]] = None) -> Optional[List[str]]:
        """
        获取指定火箭的部件名称列表
        参数：
        - rocket: 火箭ID或名称，None表示当前火箭
        返回：部件名称列表
        """
        parts_list = self.info.parts_list(rocket)
        if not parts_list:
            return None
        
        names = []
        for part in parts_list:
            if isinstance(part, dict) and "name" in part:
                names.append(str(part["name"]))
        return names if names else None

    def rocket_velocity_x(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        """
        获取火箭x速度
        """
        data = self.info.rocket_save(rocket)
        if isinstance(data, dict) and "location" in data and "velocity" in data["location"]:
            return _as_float(data["location"]["velocity"]["x"])
        return None

    def rocket_velocity_y(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        """
        获取火箭y速度
        """
        data = self.info.rocket_save(rocket)
        if isinstance(data, dict) and "location" in data and "velocity" in data["location"]:
            return _as_float(data["location"]["velocity"]["y"])
        return None 