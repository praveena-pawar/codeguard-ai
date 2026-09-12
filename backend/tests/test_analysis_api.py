from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_analysis_detects_division():
    response = client.post(
        "/analysis",
        json={
            "code": "def divide(a, b):\n    return a / b"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["issues"]) == 1
    assert data["issues"][0]["rule"] == "DIVISION"
    assert data["issues"][0]["severity"] == "warning"


def test_analysis_detects_syntax_error():
    response = client.post(
        "/analysis",
        json={
            "code": "def broken("
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["issues"][0]["rule"] == "SYNTAX_ERROR"
    assert data["issues"][0]["severity"] == "error"


def test_analysis_valid_code():
    response = client.post(
        "/analysis",
        json={
            "code": "def add(a, b):\n    return a + b"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["issues"] == []