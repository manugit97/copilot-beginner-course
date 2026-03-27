"""Tests for GET /activities endpoint."""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint."""

    def test_get_activities_success(self, client):
        """Test that GET /activities returns all activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        
        # Should have 9 activities
        assert len(data) == 9
        
        # Verify all expected activities are present
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class",
            "Basketball Team", "Tennis Club", "Theater Production",
            "Art Studio", "Science Club", "Debate Team"
        ]
        for activity in expected_activities:
            assert activity in data

    def test_get_activities_structure(self, client):
        """Test that activities have correct structure."""
        response = client.get("/activities")
        data = response.json()
        
        # Check structure of first activity
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club

    def test_get_activities_description_type(self, client):
        """Test that activity descriptions are strings."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["description"], str)
            assert len(activity_data["description"]) > 0

    def test_get_activities_schedule_type(self, client):
        """Test that schedules are strings."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["schedule"], str)
            assert len(activity_data["schedule"]) > 0

    def test_get_activities_max_participants_type(self, client):
        """Test that max_participants is an integer."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["max_participants"], int)
            assert activity_data["max_participants"] > 0

    def test_get_activities_participants_is_list(self, client):
        """Test that participants is a list."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_participants_are_emails(self, client):
        """Test that participants are email addresses."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant and "." in participant

    def test_root_redirect(self, client):
        """Test that GET / redirects to static index.html."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert "/static/index.html" in response.headers.get("location", "")

    def test_root_redirect_follow(self, client):
        """Test that GET / with follow_redirects works."""
        response = client.get("/", follow_redirects=True)
        assert response.status_code == 200

    def test_chess_club_initial_participants(self, client):
        """Test that Chess Club has correct initial participants."""
        response = client.get("/activities")
        data = response.json()
        
        chess_club = data["Chess Club"]
        assert len(chess_club["participants"]) == 2
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]

    def test_participants_count_matches_capacity(self, client):
        """Test that participant counts don't exceed capacity."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert len(activity_data["participants"]) <= activity_data["max_participants"]
