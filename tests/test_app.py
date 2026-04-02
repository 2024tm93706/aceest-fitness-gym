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

def test_save_client_db():
    client = app.test_client()

    res = client.post("/clients", json={
        "name": "Alice",
        "age": 28,
        "weight": 65,
        "program": "fat-loss"
    })

    assert res.status_code == 201


def test_load_client():
    client = app.test_client()

    res = client.get("/clients/Alice")

    assert res.status_code in [200, 404]


def test_save_progress():
    client = app.test_client()

    res = client.post("/progress", json={
        "name": "Alice",
        "adherence": 85
    })

    assert res.status_code == 201

def test_get_progress():
    client = app.test_client()

    # First insert some progress
    client.post("/progress", json={
        "name": "Alice",
        "adherence": 75
    })

    res = client.get("/progress/Alice")

    assert res.status_code in [200, 404]

    if res.status_code == 200:
        data = res.get_json()
        assert "progress" in data

def test_log_workout():
    client = app.test_client()

    res = client.post("/workouts", json={
        "name": "Alice",
        "date": "2026-04-01",
        "type": "Strength",
        "duration": 60
    })

    assert res.status_code == 201


def test_log_metrics():
    client = app.test_client()

    res = client.post("/metrics", json={
        "name": "Alice",
        "date": "2026-04-01",
        "weight": 70
    })

    assert res.status_code == 201


def test_get_workouts():
    client = app.test_client()

    res = client.get("/workouts/Alice")

    assert res.status_code == 200


def test_bmi():
    client = app.test_client()

    res = client.get("/bmi/Alice")

    assert res.status_code in [200, 400]