def test_create_trip(client):
    # スポット登録
    spots = [
        {"name": "浅草寺", "lat": 35.7148, "lng": 139.7967},
        {"name": "東京スカイツリー", "lat": 35.7101, "lng": 139.8107},
        {"name": "東京タワー", "lat": 35.6586, "lng": 139.7454},
    ]
    spot_ids = []
    for s in spots:
        res = client.post("/api/spots", json=s)
        spot_ids.append(res.json()["id"])

    # プラン生成
    response = client.post("/api/trips", json={
        "spot_ids": spot_ids,
        "start_date": "2026-05-01",
        "days": 1,
    })
    assert response.status_code == 201
    data = response.json()
    assert data["days"] == 1
    assert len(data["schedule"]) == 1
    assert len(data["schedule"][0]["items"]) > 0


def test_create_trip_multi_day(client):
    spots = [
        {"name": "浅草寺", "lat": 35.7148, "lng": 139.7967},
        {"name": "東京スカイツリー", "lat": 35.7101, "lng": 139.8107},
        {"name": "東京タワー", "lat": 35.6586, "lng": 139.7454},
        {"name": "渋谷スクランブル", "lat": 35.6595, "lng": 139.7004},
    ]
    spot_ids = []
    for s in spots:
        res = client.post("/api/spots", json=s)
        spot_ids.append(res.json()["id"])

    response = client.post("/api/trips", json={
        "spot_ids": spot_ids,
        "start_date": "2026-05-01",
        "days": 2,
    })
    assert response.status_code == 201
    data = response.json()
    assert len(data["schedule"]) == 2
    # 最終日以外に宿泊提案がある
    day1_types = [item["type"] for item in data["schedule"][0]["items"]]
    assert "accommodation" in day1_types


def test_create_trip_invalid_spots(client):
    response = client.post("/api/trips", json={
        "spot_ids": [9999],
        "start_date": "2026-05-01",
        "days": 1,
    })
    assert response.status_code == 400


def test_get_trip(client):
    res = client.post("/api/spots", json={"name": "Spot", "lat": 35.0, "lng": 139.0})
    spot_id = res.json()["id"]

    res = client.post("/api/trips", json={
        "spot_ids": [spot_id],
        "start_date": "2026-05-01",
        "days": 1,
    })
    trip_id = res.json()["id"]

    response = client.get(f"/api/trips/{trip_id}")
    assert response.status_code == 200
    assert response.json()["id"] == trip_id


def test_get_trip_not_found(client):
    response = client.get("/api/trips/9999")
    assert response.status_code == 404
