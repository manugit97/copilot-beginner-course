"""Tests for POST /activities/{activity_name}/signup endpoint."""

import pytest


class TestSignupForActivity:
    """Test suite for POST /signup endpoint."""

    def test_signup_success(self, client, test_data):
        """Test successful signup for an activity."""
        response = client.post(
            f"/activities/{test_data['existing_activity']}/signup",
            params={"email": test_data["test_email"]}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert test_data["test_email"] in data["message"]
        assert test_data["existing_activity"] in data["message"]

    def test_signup_adds_participant(self, client, test_data):
        """Test that signup actually adds participant to activity."""
        email = test_data["test_email"]
        activity = test_data["existing_activity"]
        
        # Get initial count
        response1 = client.get("/activities")
        initial_count = len(response1.json()[activity]["participants"])
        
        # Sign up
        response2 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response2.status_code == 200
        
        # Verify participant is added
        response3 = client.get("/activities")
        final_count = len(response3.json()[activity]["participants"])
        assert final_count == initial_count + 1
        assert email in response3.json()[activity]["participants"]

    def test_signup_activity_not_found(self, client, test_data):
        """Test signup for non-existent activity returns 404."""
        response = client.post(
            f"/activities/{test_data['nonexistent_activity']}/signup",
            params={"email": test_data["test_email"]}
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data.get("detail", "")

    def test_signup_already_registered(self, client, test_data):
        """Test signup for already registered participant returns 400."""
        activity = test_data["existing_activity"]
        email = test_data["existing_participant"]
        
        # Try to sign up someone already registered
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data.get("detail", "").lower()

    def test_signup_multiple_activities(self, client, test_data):
        """Test that someone can sign up for multiple activities."""
        email = test_data["test_email"]
        activities = ["Chess Club", "Programming Class"]
        
        # Sign up for first activity
        response1 = client.post(
            f"/activities/{activities[0]}/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Sign up for second activity
        response2 = client.post(
            f"/activities/{activities[1]}/signup",
            params={"email": email}
        )
        assert response2.status_code == 200
        
        # Verify in both activities
        response3 = client.get("/activities")
        data = response3.json()
        assert email in data[activities[0]]["participants"]
        assert email in data[activities[1]]["participants"]

    def test_signup_response_format(self, client, test_data):
        """Test that signup response has correct format."""
        response = client.post(
            f"/activities/{test_data['existing_activity']}/signup",
            params={"email": test_data["test_email"]}
        )
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, dict)
        assert "message" in data
        assert isinstance(data["message"], str)

    def test_signup_with_different_emails(self, client):
        """Test signup with various email formats."""
        activity = "Chess Club"
        emails = [
            "alice.smith@mergington.edu",
            "bob_jones@mergington.edu",
            "charlie123@mergington.edu"
        ]
        
        for email in emails:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert response.status_code == 200

    def test_signup_activity_name_case_sensitive(self, client, test_data):
        """Test that activity names are case-sensitive."""
        response = client.post(
            "/activities/chess club/signup",  # lowercase
            params={"email": test_data["test_email"]}
        )
        assert response.status_code == 404

    def test_signup_url_encoding(self, client, test_data):
        """Test signup with URL-encoded activity name."""
        # Test with special characters that need encoding
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": test_data["test_email"]}
        )
        assert response.status_code == 200

    def test_signup_participant_order_preserved(self, client, test_data):
        """Test that participant order is maintained."""
        activity = test_data["existing_activity"]
        
        # Get initial participants
        response1 = client.get("/activities")
        initial_participants = response1.json()[activity]["participants"].copy()
        
        # Sign up new participant
        response2 = client.post(
            f"/activities/{activity}/signup",
            params={"email": test_data["test_email"]}
        )
        assert response2.status_code == 200
        
        # Check new participant is appended
        response3 = client.get("/activities")
        final_participants = response3.json()[activity]["participants"]
        
        assert final_participants[:len(initial_participants)] == initial_participants
        assert final_participants[-1] == test_data["test_email"]
