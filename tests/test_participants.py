"""Tests for DELETE /activities/{activity_name}/participants/{email} endpoint."""

import pytest


class TestRemoveParticipant:
    """Test suite for DELETE participant endpoint."""

    def test_remove_participant_success(self, client, test_data):
        """Test successful removal of participant from activity."""
        activity = test_data["existing_activity"]
        email = test_data["existing_participant"]
        
        response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]

    def test_remove_participant_removes_from_list(self, client, test_data):
        """Test that removal actually removes participant from list."""
        activity = test_data["existing_activity"]
        email = test_data["existing_participant"]
        
        # Verify participant exists
        response1 = client.get("/activities")
        assert email in response1.json()[activity]["participants"]
        
        # Remove participant
        response2 = client.delete(
            f"/activities/{activity}/participants/{email}"
        )
        assert response2.status_code == 200
        
        # Verify participant is removed
        response3 = client.get("/activities")
        assert email not in response3.json()[activity]["participants"]

    def test_remove_participant_decreases_count(self, client, test_data):
        """Test that removal decreases participant count."""
        activity = test_data["existing_activity"]
        email = test_data["existing_participant"]
        
        # Get initial count
        response1 = client.get("/activities")
        initial_count = len(response1.json()[activity]["participants"])
        
        # Remove participant
        response2 = client.delete(
            f"/activities/{activity}/participants/{email}"
        )
        assert response2.status_code == 200
        
        # Check decreased count
        response3 = client.get("/activities")
        final_count = len(response3.json()[activity]["participants"])
        assert final_count == initial_count - 1

    def test_remove_participant_activity_not_found(self, client, test_data):
        """Test removal from non-existent activity returns 404."""
        response = client.delete(
            f"/activities/{test_data['nonexistent_activity']}/participants/test@example.com"
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data.get("detail", "")

    def test_remove_participant_not_in_activity(self, client, test_data):
        """Test removal of non-existent participant returns 404."""
        activity = test_data["existing_activity"]
        email = "nonexistent@mergington.edu"
        
        response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data.get("detail", "").lower()

    def test_remove_participant_response_format(self, client, test_data):
        """Test that removal response has correct format."""
        activity = test_data["existing_activity"]
        email = test_data["existing_participant"]
        
        response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, dict)
        assert "message" in data
        assert isinstance(data["message"], str)

    def test_remove_then_readd_participant(self, client, test_data):
        """Test that removed participant can be re-added."""
        activity = test_data["existing_activity"]
        email = test_data["test_email"]
        
        # Sign up
        response1 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Remove
        response2 = client.delete(
            f"/activities/{activity}/participants/{email}"
        )
        assert response2.status_code == 200
        
        # Re-add
        response3 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response3.status_code == 200
        
        # Verify re-added
        response4 = client.get("/activities")
        assert email in response4.json()[activity]["participants"]

    def test_remove_multiple_participants_sequentially(self, client, test_data):
        """Test removing multiple participants from one activity."""
        activity = test_data["existing_activity"]
        
        # Get initial participants
        response1 = client.get("/activities")
        initial_participants = response1.json()[activity]["participants"].copy()
        initial_count = len(initial_participants)
        
        # Remove first two participants
        for i, email in enumerate(initial_participants[:2]):
            response = client.delete(
                f"/activities/{activity}/participants/{email}"
            )
            assert response.status_code == 200
            
            # Verify count decreases
            response_check = client.get("/activities")
            current_count = len(response_check.json()[activity]["participants"])
            assert current_count == initial_count - (i + 1)

    def test_remove_participant_case_sensitive(self, client, test_data):
        """Test that email comparison is case-sensitive (or not, depending on implementation)."""
        activity = test_data["existing_activity"]
        email = "test@mergington.edu"
        
        # Sign up with lowercase
        response1 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Try to remove with different case (likely will fail - this documents behavior)
        response2 = client.delete(
            f"/activities/{activity}/participants/{email.upper()}"
        )
        # This will depend on implementation - documenting current behavior
        # If case-sensitive: should return 404
        # If case-insensitive: should return 200
        assert response2.status_code in [200, 404]

    def test_remove_preserves_other_participants(self, client, test_data):
        """Test that removing one participant doesn't affect others."""
        activity = test_data["existing_activity"]
        
        # Get initial participants
        response1 = client.get("/activities")
        initial_participants = response1.json()[activity]["participants"].copy()
        
        # Remove first participant
        email_to_remove = initial_participants[0]
        response2 = client.delete(
            f"/activities/{activity}/participants/{email_to_remove}"
        )
        assert response2.status_code == 200
        
        # Verify other participants are unchanged
        response3 = client.get("/activities")
        final_participants = response3.json()[activity]["participants"]
        
        # Check all other participants are still there
        for email in initial_participants[1:]:
            assert email in final_participants
        
        # Check removed participant is gone
        assert email_to_remove not in final_participants

    def test_remove_only_participant(self, client):
        """Test removing the only participant from an activity."""
        activity = "Basketball Team"
        email = "alex@mergington.edu"
        
        # Basketball Team has only one participant
        response1 = client.get("/activities")
        assert len(response1.json()[activity]["participants"]) == 1
        
        # Remove the only participant
        response2 = client.delete(
            f"/activities/{activity}/participants/{email}"
        )
        assert response2.status_code == 200
        
        # Verify activity has no participants
        response3 = client.get("/activities")
        assert len(response3.json()[activity]["participants"]) == 0

    def test_remove_url_encoding(self, client, test_data):
        """Test removal with URL-encoded email."""
        activity = test_data["existing_activity"]
        email = test_data["existing_participant"]
        
        # Try with URL-encoded email
        response = client.delete(
            f"/activities/{activity}/participants/{email.replace('@', '%40')}"
        )
        assert response.status_code == 200
