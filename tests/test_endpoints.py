"""
Happy-path tests for FastAPI Activities API endpoints.

Tests follow the AAA (Arrange-Act-Assert) testing pattern for clarity and structure.
"""

def test_get_activities(client):
    """
    Test that GET /activities returns the complete activities list.
    
    AAA Pattern:
    - Arrange: No setup required; activities are pre-loaded in the app
    - Act: Call GET /activities endpoint
    - Assert: Verify status code is 200 and response contains expected activity names
    """
    # Arrange
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
        "Tennis Club", "Drama Club", "Art Studio", "Debate Team", "Science Club"
    ]
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities_data = response.json()
    assert isinstance(activities_data, dict)
    assert set(activities_data.keys()) == set(expected_activities)
    
    # Verify structure of a sample activity
    chess_club = activities_data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_signup_for_activity(client):
    """
    Test successful signup for an activity.
    
    AAA Pattern:
    - Arrange: Define test data (activity name, email)
    - Act: Send POST request to signup endpoint
    - Assert: Verify status code is 200 and success message is returned
    """
    # Arrange
    activity_name = "Programming Class"
    test_email = "test_student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert test_email in data["message"]
    assert activity_name in data["message"]


def test_unregister_from_activity(client):
    """
    Test successful unregister from an activity.
    
    AAA Pattern:
    - Arrange: Sign up a student first, then prepare for unregister
    - Act: Send POST request to unregister endpoint
    - Assert: Verify status code is 200 and success message is returned
    """
    # Arrange
    activity_name = "Tennis Club"
    test_email = "unregister_test@mergington.edu"
    
    # First, sign up the student
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email}
    )
    assert signup_response.status_code == 200
    
    # Act: Now unregister the student
    unregister_response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": test_email}
    )
    
    # Assert
    assert unregister_response.status_code == 200
    data = unregister_response.json()
    assert "message" in data
    assert test_email in data["message"]
    assert activity_name in data["message"]
