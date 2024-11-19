import sys
import os
from fastapi.testclient import TestClient

# Adjust the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the Sanquin API! \n Visit /docs for the API documentation."
    }
