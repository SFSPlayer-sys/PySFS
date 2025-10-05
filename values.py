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
        except Exception:
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