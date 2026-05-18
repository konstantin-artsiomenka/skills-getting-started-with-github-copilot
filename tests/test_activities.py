from src import app as app_module


def test_get_activities(client):
    # Arrange: none (server seeded with activities)
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_and_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = "testuser@example.com"

    # Act: sign up
    resp1 = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert resp1.status_code == 200
    assert resp1.json()["message"].startswith("Signed up")

    # Act: duplicate signup
    resp2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert duplicate rejected
    assert resp2.status_code == 400


def test_unregister_participant(client):
    # Arrange: use an existing participant from seeded data
    activity = "Chess Club"
    existing = app_module.activities[activity]["participants"][0]

    # Act: unregister
    resp = client.delete(f"/activities/{activity}/signup", params={"email": existing})
    # Assert
    assert resp.status_code == 200
    assert resp.json()["message"].startswith("Unregistered")

    # Act: try deleting again -> not found
    resp2 = client.delete(f"/activities/{activity}/signup", params={"email": existing})
    assert resp2.status_code == 404
