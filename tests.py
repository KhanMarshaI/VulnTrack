import pytest
from app import app, db

@pytest.fixture
def client():
    # Configure the app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use in-memory DB for tests
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_home_page(client):
    """Test that the home page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"VulnTrack" in response.data or b"Vulnerability" in response.data