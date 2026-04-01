import math


def haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """2点間の距離をkm単位で計算（Haversine公式）"""
    R = 6371.0  # 地球の半径 (km)

    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)

    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lng / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def estimate_travel_time_min(distance_km: float) -> int:
    """距離から移動時間を推定（平均時速40kmと仮定）"""
    return max(10, round(distance_km / 40 * 60))


def optimize_route(spots: list[dict]) -> list[dict]:
    """最近傍法でスポットの訪問順を最適化する。

    Args:
        spots: [{"id": int, "name": str, "lat": float, "lng": float}, ...]

    Returns:
        最適化された順序のスポットリスト
    """
    if len(spots) <= 1:
        return spots

    remaining = list(spots)
    ordered: list[dict] = [remaining.pop(0)]

    while remaining:
        last = ordered[-1]
        nearest_idx = 0
        nearest_dist = float("inf")

        for i, spot in enumerate(remaining):
            dist = haversine_distance(last["lat"], last["lng"], spot["lat"], spot["lng"])
            if dist < nearest_dist:
                nearest_dist = dist
                nearest_idx = i

        ordered.append(remaining.pop(nearest_idx))

    return ordered


def split_spots_by_day(spots: list[dict], days: int) -> list[list[dict]]:
    """スポットを日数で均等に振り分ける。"""
    if days <= 0:
        return [spots]

    per_day = max(1, len(spots) // days)
    result: list[list[dict]] = []

    for i in range(days):
        start = i * per_day
        if i == days - 1:
            result.append(spots[start:])
        else:
            result.append(spots[start : start + per_day])

    return [day_spots for day_spots in result if day_spots]
