import math
from typing import Any, Dict, List, Optional, Union, Tuple

from .info import InfoAPI


class CalcAPI:
    def __init__(self, info: InfoAPI) -> None:
        self.info = info

    def _as_float(self, x: Any) -> Optional[float]:
        try:
            return float(x)
        except Exception:
            return None

    def _as_int(self, x: Any) -> Optional[int]:
        try:
            return int(x)
        except Exception:
            return None

    def rocket_velocity_magnitude(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        """
        计算火箭速度大小
        """
        data = self.info.rocket_sim(rocket)
        if not isinstance(data, dict):
            return None
            
        # 尝试从轨道信息获取速度
        orbit = data.get("orbit")
        if isinstance(orbit, dict):
            # 如果有轨道信息，可以通过轨道要素计算速度
            # 这里需要更多轨道数据，暂时返回None
            pass
            
        # 从火箭保存信息获取速度
        rocket_save = self.info.rocket_save(rocket)
        if isinstance(rocket_save, dict):
            location = rocket_save.get("location")
            if isinstance(location, dict):
                velocity = location.get("velocity")
                if isinstance(velocity, dict):
                    vx = self._as_float(velocity.get("x"))
                    vy = self._as_float(velocity.get("y"))
                    if vx is not None and vy is not None:
                        return math.sqrt(vx * vx + vy * vy)
        return None

    def rocket_velocity_direction(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        """
        计算火箭速度方向（角度，度）
        """
        data = self.info.rocket_save(rocket)
        if not isinstance(data, dict):
            return None
            
        location = data.get("location")
        if isinstance(location, dict):
            velocity = location.get("velocity")
            if isinstance(velocity, dict):
                vx = self._as_float(velocity.get("x"))
                vy = self._as_float(velocity.get("y"))
                if vx is not None and vy is not None:
                    # 计算角度（弧度转度）
                    angle_rad = math.atan2(vy, vx)
                    angle_deg = math.degrees(angle_rad)
                    # 标准化到0-360度
                    return angle_deg % 360
        return None

    def rocket_orbit_period(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        """
        获取火箭轨道周期（秒）
        """
        data = self.info.rocket_sim(rocket)
        if isinstance(data, dict):
            orbit = data.get("orbit")
            if isinstance(orbit, dict):
                return self._as_float(orbit.get("period"))
        return None

    def rocket_normal_angle(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        """
        计算火箭法线角度
        """
        velocity_direction = self.rocket_velocity_direction(rocket)
        if velocity_direction is not None:
            # 法线角度 = 速度方向 + 90度
            normal_angle = velocity_direction + 90
            # 标准化到0-360度
            return normal_angle % 360
        return None

    def rocket_velocity_components(self, rocket: Optional[Union[int, str]] = None) -> Optional[Dict[str, float]]:
        """
        获取火箭速度分量（vx, vy）
        来源：/rocket.location.velocity
        """
        data = self.info.rocket_save(rocket)
        if not isinstance(data, dict):
            return None
            
        location = data.get("location")
        if isinstance(location, dict):
            velocity = location.get("velocity")
            if isinstance(velocity, dict):
                vx = self._as_float(velocity.get("x"))
                vy = self._as_float(velocity.get("y"))
                if vx is not None and vy is not None:
                    return {"vx": vx, "vy": vy}
        return None

    def rocket_position_angle(self, rocket: Optional[Union[int, str]] = None) -> Optional[float]:
        """
        计算火箭位置角度（从星球中心指向火箭的角度，度）
        """
        data = self.info.rocket_sim(rocket)
        if isinstance(data, dict):
            position = data.get("position")
            if isinstance(position, dict):
                x = self._as_float(position.get("x"))
                y = self._as_float(position.get("y"))
                if x is not None and y is not None:
                    # 计算角度（弧度转度）
                    angle_rad = math.atan2(y, x)
                    angle_deg = math.degrees(angle_rad)
                    # 标准化到0-360度
                    return angle_deg % 360
        return None

    def rocket_velocity_info(self, rocket: Optional[Union[int, str]] = None) -> Optional[Dict[str, float]]:
        """
        获取火箭速度的完整信息
        """
        velocity_components = self.rocket_velocity_components(rocket)
        if velocity_components is None:
            return None
            
        vx = velocity_components["vx"]
        vy = velocity_components["vy"]
        magnitude = math.sqrt(vx * vx + vy * vy)
        direction = math.degrees(math.atan2(vy, vx)) % 360
        
        return {
            "magnitude": magnitude,
            "direction": direction,
            "vx": vx,
            "vy": vy
        }

    def rocket_orbit_info(self, rocket: Optional[Union[int, str]] = None) -> Optional[Dict[str, float]]:
        """
        获取火箭轨道的完整信息
        """
        data = self.info.rocket_sim(rocket)
        if not isinstance(data, dict):
            return None
            
        orbit = data.get("orbit")
        if not isinstance(orbit, dict):
            return None
            
        period = self._as_float(orbit.get("period"))
        apoapsis = self._as_float(orbit.get("apoapsis"))
        periapsis = self._as_float(orbit.get("periapsis"))
        true_anomaly = self._as_float(orbit.get("trueAnomaly"))
        
        result = {}
        if period is not None:
            result["period"] = period
        if apoapsis is not None:
            result["apoapsis"] = apoapsis
        if periapsis is not None:
            result["periapsis"] = periapsis
        if true_anomaly is not None:
            result["trueAnomaly"] = true_anomaly
            
        return result if result else None

    

    def rocket_angle_info(self, rocket: Optional[Union[int, str]] = None) -> Optional[Dict[str, float]]:
        """
        获取火箭角度的完整信息
        """
        velocity_direction = self.rocket_velocity_direction(rocket)
        normal_angle = self.rocket_normal_angle(rocket)
        position_angle = self.rocket_position_angle(rocket)
        
        # 获取火箭旋转角度
        data = self.info.rocket_sim(rocket)
        rotation = None
        if isinstance(data, dict):
            rotation = self._as_float(data.get("rotation"))
        
        result = {}
        if velocity_direction is not None:
            result["velocity_direction"] = velocity_direction
        if normal_angle is not None:
            result["normal_angle"] = normal_angle
        if position_angle is not None:
            result["position_angle"] = position_angle
        if rotation is not None:
            result["rotation"] = rotation
            
        return result if result else None

    def impact_point(self,
                     rocket_x: float,
                     rocket_y: float,
                     vel_x: float,
                     vel_y: float,
                     planet_radius: float,
                     gravity: float,
                     *,
                     dt: float = 0.02,
                     max_steps: int = 100000) -> Optional[Dict[str, float]]:
        """
        数值积分计算火箭与星球的撞击点坐标。若不撞击，返回 None
        参考：加速度大小 g * (R/d)^2，方向指向星球中心（原点）

        参数（由调用方提供，不在函数内获取）：
        - rocket_x, rocket_y: 火箭初始坐标
        - vel_x, vel_y: 火箭初始速度分量
        - planet_radius: 星球半径 R
        - gravity: 星球表面重力加速度 g
        - dt: 时间步长（秒），越小越精确但计算更慢
        - max_steps: 最大模拟步数

        返回：{"x": impact_x, "y": impact_y} 或 None
        """
        # 预处理/初始化
        x = float(rocket_x)
        y = float(rocket_y)
        vx = float(vel_x)
        vy = float(vel_y)
        R = float(planet_radius)
        g = float(gravity)
        if dt <= 0:
            dt = 0.02

        R2 = R * R
        # µ = g R^2，可将 a = -µ r / |r|^3，减少乘除次数
        mu = g * R2
        # 发散阈值（平方距离）：过远视为不会撞击
        max_d2 = (10.0 ** 12) * R2  # (1e6 R)^2

        # 直接命中（已在地表内）
        d2 = x * x + y * y
        if d2 <= R2:
            return {"x": x, "y": y}

        # 计算初始加速度（a = -µ r / |r|^3）
        d = math.sqrt(d2)
        if d == 0:
            return None
        inv_d = 1.0 / d
        inv_d3 = inv_d / d2  # 1/|r|^3
        ax = -mu * x * inv_d3
        ay = -mu * y * inv_d3

        # 主循环（Velocity-Verlet，更稳定，允许较大 dt）
        for _ in range(int(max_steps)):
            # 半步速度
            vxh = vx + 0.5 * dt * ax
            vyh = vy + 0.5 * dt * ay

            # 位置更新
            x_new = x + dt * vxh
            y_new = y + dt * vyh

            # 命中/越界检测（使用平方距离，少一次开方）
            d2_new = x_new * x_new + y_new * y_new
            if d2_new <= R2:
                # 在线段 (x,y)->(x_new,y_new) 上插值求与圆 |r|=R 的交点，提高精度
                dx = x_new - x
                dy = y_new - y
                # 解 |(x,y) + s*(dx,dy)|^2 = R^2, s ∈ [0,1]
                # => (dx^2+dy^2) s^2 + 2(x dx + y dy) s + (x^2+y^2 - R^2) = 0
                A = dx * dx + dy * dy
                B = 2.0 * (x * dx + y * dy)
                C = (x * x + y * y) - R2
                if A > 0:
                    disc = B * B - 4.0 * A * C
                    if disc >= 0:
                        sqrt_disc = math.sqrt(disc)
                        s1 = (-B - sqrt_disc) / (2.0 * A)
                        s2 = (-B + sqrt_disc) / (2.0 * A)
                        s_candidates = [s for s in (s1, s2) if 0.0 <= s <= 1.0]
                        if s_candidates:
                            s_hit = min(s_candidates)
                            xi = x + s_hit * dx
                            yi = y + s_hit * dy
                            return {"x": xi, "y": yi}
                # 退化：若求解失败，返回步末位置
                return {"x": x_new, "y": y_new}

            if d2_new > max_d2:
                return None

            # 新位置处加速度
            d_new = math.sqrt(d2_new)
            inv_d_new = 1.0 / d_new
            inv_d3_new = inv_d_new / d2_new
            ax_new = -mu * x_new * inv_d3_new
            ay_new = -mu * y_new * inv_d3_new

            # 完成速度步
            vx = vxh + 0.5 * dt * ax_new
            vy = vyh + 0.5 * dt * ay_new

            # 提交位置与加速度
            x, y = x_new, y_new
            ax, ay = ax_new, ay_new

        return None