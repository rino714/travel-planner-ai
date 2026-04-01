def suggest_accommodation(lat: float, lng: float) -> str:
    """緯度経度からエリア名ベースの宿泊地を提案する（MVP版）。

    MVPでは逆ジオコーディングは行わず、主要エリアの緯度経度範囲で
    大まかなエリア名を返す。マッチしない場合は座標ベースの文字列を返す。
    """
    areas = [
        {"name": "東京駅", "lat": 35.6812, "lng": 139.7671, "radius_km": 3},
        {"name": "新宿", "lat": 35.6896, "lng": 139.6922, "radius_km": 3},
        {"name": "渋谷", "lat": 35.6580, "lng": 139.7016, "radius_km": 2},
        {"name": "浅草", "lat": 35.7148, "lng": 139.7967, "radius_km": 2},
        {"name": "池袋", "lat": 35.7295, "lng": 139.7109, "radius_km": 2},
        {"name": "品川", "lat": 35.6284, "lng": 139.7387, "radius_km": 2},
        {"name": "横浜", "lat": 35.4437, "lng": 139.6380, "radius_km": 5},
        {"name": "鎌倉", "lat": 35.3192, "lng": 139.5467, "radius_km": 3},
        {"name": "京都駅", "lat": 34.9858, "lng": 135.7588, "radius_km": 3},
        {"name": "大阪・梅田", "lat": 34.7024, "lng": 135.4959, "radius_km": 3},
        {"name": "大阪・難波", "lat": 34.6629, "lng": 135.5013, "radius_km": 2},
        {"name": "神戸・三宮", "lat": 34.6932, "lng": 135.1956, "radius_km": 3},
        {"name": "奈良", "lat": 34.6851, "lng": 135.8048, "radius_km": 3},
        {"name": "名古屋駅", "lat": 35.1709, "lng": 136.8815, "radius_km": 3},
        {"name": "札幌", "lat": 43.0621, "lng": 141.3544, "radius_km": 5},
        {"name": "福岡・博多", "lat": 33.5904, "lng": 130.4017, "radius_km": 3},
        {"name": "沖縄・那覇", "lat": 26.3344, "lng": 127.8001, "radius_km": 5},
        {"name": "広島", "lat": 34.3853, "lng": 132.4553, "radius_km": 3},
        {"name": "仙台", "lat": 38.2682, "lng": 140.8694, "radius_km": 3},
        {"name": "金沢", "lat": 36.5613, "lng": 136.6562, "radius_km": 3},
    ]

    from app.services.route_optimizer import haversine_distance

    nearest_area = None
    nearest_dist = float("inf")

    for area in areas:
        dist = haversine_distance(lat, lng, area["lat"], area["lng"])
        if dist < area["radius_km"] and dist < nearest_dist:
            nearest_dist = dist
            nearest_area = area["name"]

    if nearest_area:
        return f"{nearest_area}エリアのホテル"

    return f"付近（{lat:.2f}, {lng:.2f}）のホテル"
