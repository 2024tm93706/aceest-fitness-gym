from app.app import app

def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"ACEest Gym API running" in response.data


def test_get_programs():
    client = app.test_client()
    response = client.get("/programs")
    assert response.status_code == 200
    assert b"fat-loss" in response.data


def test_get_single_program():
    client = app.test_client()
    response = client.get("/programs/fat-loss")
    assert response.status_code == 200
    assert b"Fat Loss" in response.data


def test_invalid_program():
    client = app.test_client()
    response = client.get("/programs/invalid")
    assert response.status_code == 404

def test_calorie_calculation():
    client = app.test_client()
    response = client.get("/calculate-calories/fat-loss/70")

    assert response.status_code == 200
    data = response.get_json()
    assert data["estimated_calories"] == 1540


def test_invalid_program_calories():
    client = app.test_client()
    response = client.get("/calculate-calories/invalid/70")

    assert response.status_code == 404