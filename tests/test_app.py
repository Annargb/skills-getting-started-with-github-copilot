import pytest
from fastapi.testclient import TestClient
from src.app import app
from src.activities_db import activities
import copy

# Исходное состояние activities
initial_activities = copy.deepcopy(activities)

@pytest.fixture(autouse=True)
def reset_activities():
    # Сбросить состояние activities перед каждым тестом
    for key in list(activities.keys()):
        del activities[key]
    for key, value in initial_activities.items():
        activities[key] = copy.deepcopy(value)

client = TestClient(app)

# Тест получения всех активностей
def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# Тест регистрации участника
def test_signup_for_activity():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Удаляем если уже есть
    client.delete(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Signed up")
    # Повторная регистрация должна вернуть ошибку
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]

# Тест удаления участника
def test_unregister_from_activity():
    email = "removeme@mergington.edu"
    activity = "Chess Club"
    # Зарегистрировать сначала
    client.post(f"/activities/{activity}/signup?email={email}")
    # Проверить, что участник добавлен
    activities_resp = client.get("/activities")
    participants = activities_resp.json()[activity]["participants"]
    assert email in participants
    # Удалить участника
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Unregistered")
    # Повторное удаление должно вернуть ошибку
    response2 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response2.status_code == 404
    assert "not found" in response2.json()["detail"]
