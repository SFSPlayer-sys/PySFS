import math
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .http import HttpClient


Vec2 = Tuple[float, float]
Vec3 = Tuple[float, float, float]


def _to_vec3(p: Sequence[float]) -> Vec3:
    if len(p) == 2:
        return (float(p[0]), float(p[1]), 0.0)
    return (float(p[0]), float(p[1]), float(p[2]))


def _color_array(color: Optional[Sequence[float]]) -> Optional[List[float]]:
    if color is None:
        return None
    if len(color) == 3:
        r, g, b = color
        return [float(r), float(g), float(b), 1.0]
    r, g, b, a = color
    return [float(r), float(g), float(b), float(a)]


class DrawAPI:
    """
    绘图 API（对应服务端 POST /draw）。
    - 坐标均为世界坐标（非屏幕坐标）。
    - 颜色为 [r,g,b,a]，范围 0..1。
    - 已绘制对象会持续显示，直到 clear。
    """

    def __init__(self, http: HttpClient) -> None:
        self.http = http

    def _post(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.http.post_json("/draw", payload)

    # 基础：清空
    def clear(self) -> Dict[str, Any]:
        return self._post({"cmd": "clear"})

    # 基础：线段
    def line(
        self,
        start: Sequence[float],
        end: Sequence[float],
        *,
        color: Optional[Sequence[float]] = None,
        width: Optional[float] = None,
        sorting: Optional[float] = None,
        layer: Optional[float] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "cmd": "line",
            "start": list(_to_vec3(start)),
            "end": list(_to_vec3(end)),
        }
        c = _color_array(color)
        if c is not None:
            payload["color"] = c
        if width is not None:
            payload["width"] = float(width)
        if sorting is not None:
            payload["sorting"] = float(sorting)
        if layer is not None:
            payload["layer"] = float(layer)
        return self._post(payload)

    # 基础：圆（描边）
    def circle(
        self,
        center: Sequence[float],
        radius: float,
        *,
        color: Optional[Sequence[float]] = None,
        resolution: Optional[int] = None,
        sorting: Optional[float] = None,
        layer: Optional[float] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "cmd": "circle",
            "center": [float(center[0]), float(center[1])],
            "radius": float(radius),
        }
        if resolution is not None:
            payload["resolution"] = max(8, int(resolution))
        c = _color_array(color)
        if c is not None:
            payload["color"] = c
        if sorting is not None:
            payload["sorting"] = float(sorting)
        if layer is not None:
            payload["layer"] = float(layer)
        return self._post(payload)

    # 组合：正多边形（闭合多段线）
    def regular_polygon(
        self,
        center: Sequence[float],
        radius: float,
        sides: int,
        *,
        color: Optional[Sequence[float]] = None,
        width: Optional[float] = None,
        sorting: Optional[float] = None,
        layer: Optional[float] = None,
        rotation_deg: float = 0.0,
    ) -> None:
        if sides < 3:
            return
        cx, cy = float(center[0]), float(center[1])
        rot = math.radians(rotation_deg)
        pts: List[Vec2] = []
        for i in range(sides):
            ang = rot + 2.0 * math.pi * (i / sides)
            x = cx + radius * math.cos(ang)
            y = cy + radius * math.sin(ang)
            pts.append((x, y))
        for i in range(sides):
            a = pts[i]
            b = pts[(i + 1) % sides]
            self.line(a, b, color=color, width=width, sorting=sorting, layer=layer)

    


    # 组合：矩形（可选填充），p0 与 p1 为对角点
    def rect(
        self,
        p0: Sequence[float],
        p1: Sequence[float],
        *,
        color: Optional[Sequence[float]] = None,
        sorting: Optional[float] = None,
        layer: Optional[float] = None,
        filled: bool = False,
        fill_axis: str = "x",
    ) -> None:
        """
        绘制矩形：
        - p0, p1：对角点，支持 (x,y) 或 (x,y,z)
        - filled=False：仅描边；True：使用单条超粗线段近似填充
        - fill_axis："x" 或 "y"，控制超粗线段方向
        """

        x1, y1, z1 = _to_vec3(p0)
        x2, y2, z2 = _to_vec3(p1)
        xmin, xmax = (x1, x2) if x1 <= x2 else (x2, x1)
        ymin, ymax = (y1, y2) if y1 <= y2 else (y2, y1)
        z = z1  # 使用 p0 的 z（一般为 0）

        # 填充：用一条“超粗”线段近似实心矩形
        if filled:
            # 注意：x 表示长度（线的方向），y 表示线宽；忽略传入的 width
            if fill_axis.lower() == "y":
                # 纵向线：长度沿 y，线宽由 x 范围决定
                cx = (xmin + xmax) * 0.5
                line_width = max(1.0, xmax - xmin)
                self.line((cx, ymin, z), (cx, ymax, z), color=color, width=line_width, sorting=sorting, layer=layer)
            else:
                # 横向线：长度沿 x，线宽由 y 范围决定
                cy = (ymin + ymax) * 0.5
                line_width = max(1.0, ymax - ymin)
                self.line((xmin, cy, z), (xmax, cy, z), color=color, width=line_width, sorting=sorting, layer=layer)
            return

        # 仅描边
        a = (xmin, ymin, z)
        b = (xmax, ymin, z)
        c = (xmax, ymax, z)
        d = (xmin, ymax, z)
        self.line(a, b, color=color, sorting=sorting, layer=layer)
        self.line(b, c, color=color, sorting=sorting, layer=layer)
        self.line(c, d, color=color, sorting=sorting, layer=layer)
        self.line(d, a, color=color, sorting=sorting, layer=layer)

    # 组合：空心矩形（仅描边），p0 与 p1 为对角点
    def rect_outline(
        self,
        p0: Sequence[float],
        p1: Sequence[float],
        *,
        color: Optional[Sequence[float]] = None,
        width: Optional[float] = None,
        sorting: Optional[float] = None,
        layer: Optional[float] = None,
    ) -> None:
        x1, y1, z1 = _to_vec3(p0)
        x2, y2, z2 = _to_vec3(p1)
        xmin, xmax = (x1, x2) if x1 <= x2 else (x2, x1)
        ymin, ymax = (y1, y2) if y1 <= y2 else (y2, y1)
        z = z1

        a = (xmin, ymin, z)
        b = (xmax, ymin, z)
        c = (xmax, ymax, z)
        d = (xmin, ymax, z)
        self.line(a, b, color=color, width=width, sorting=sorting, layer=layer)
        self.line(b, c, color=color, width=width, sorting=sorting, layer=layer)
        self.line(c, d, color=color, width=width, sorting=sorting, layer=layer)
        self.line(d, a, color=color, width=width, sorting=sorting, layer=layer)