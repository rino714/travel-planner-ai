def test_create_spot(client):
    response = client.post("/api/spots", json={
        "name": "東京タワー",
        "address": "東京都港区芝公園4-2-8",
        "lat": 35.6586,
        "lng": 139.7454,
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "東京タワー"
    assert data["lat"] == 35.6586
    assert "id" in data


def test_list_spots(client):
    client.post("/api/spots", json={"name": "Spot A", "lat": 35.0, "lng": 139.0})
    client.post("/api/spots", json={"name": "Spot B", "lat": 35.1, "lng": 139.1})

    response = client.get("/api/spots")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_delete_spot(client):
    res = client.post("/api/spots", json={"name": "Spot", "lat": 35.0, "lng": 139.0})
    spot_id = res.json()["id"]

    response = client.delete(f"/api/spots/{spot_id}")
    assert response.status_code == 204

    response = client.get("/api/spots")
    assert len(response.json()) == 0


def test_delete_spot_not_found(client):
    response = client.delete("/api/spots/9999")
    assert response.status_code == 404
