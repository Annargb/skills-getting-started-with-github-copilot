import pytest
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
