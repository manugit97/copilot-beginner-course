"""Shared test configuration and fixtures for FastAPI tests."""

import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app


@pytest.fixture
def fresh_activities():
    """Provide a fresh copy of the activities database for each test."""
    activities_data = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball training and matches",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Tennis skills development and friendly competitions",
            "schedule": "Saturdays, 10:00 AM - 12:00 PM",
            "max_participants": 10,
            "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
        },
        "Theater Production": {
            "description": "Acting, stage design, and performing in school plays",
            "schedule": "Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["mia@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, sculpture, and other visual arts",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["noah@mergington.edu", "ava@mergington.edu"]
        },
        "Science Club": {
            "description": "Explore science through experiments and competitions",
            "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
            "max_participants": 18,
            "participants": ["ethan@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation and public speaking skills",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["charlotte@mergington.edu", "james@mergington.edu"]
        }
    }
    return deepcopy(activities_data)


@pytest.fixture
def client(fresh_activities, monkeypatch):
    """Provide a TestClient with fresh activities database."""
    # Replace the app's activities with fresh data for this test
    monkeypatch.setattr("app.activities", fresh_activities)
    return TestClient(app)


@pytest.fixture
def test_data():
    """Provide common test data."""
    return {
        "test_email": "test@mergington.edu",
        "existing_activity": "Chess Club",
        "nonexistent_activity": "Non Existent Club",
        "existing_participant": "michael@mergington.edu"
    }
