from fastapi.testclient import TestClient


def _register_user(client: TestClient, email: str, password: str) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password},
    )
    assert response.status_code == 201


def _login_user(client: TestClient, email: str, password: str) -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_health_check_returns_expected_payload(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "app_name": "FastAPI Template Test",
        "environment": "test",
        "version": "0.1.0",
    }


def test_user_can_register_login_and_fetch_profile(client: TestClient) -> None:
    _register_user(client, "developer@example.com", "StrongPassword123!")

    token = _login_user(client, "developer@example.com", "StrongPassword123!")
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == "developer@example.com"
    assert response.json()["role"] == "user"


def test_duplicate_registration_is_rejected(client: TestClient) -> None:
    _register_user(client, "duplicate@example.com", "StrongPassword123!")

    response = client.post(
        "/api/v1/auth/register",
        json={"email": "duplicate@example.com", "password": "StrongPassword123!"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "A user with this email already exists."


def test_admin_route_requires_admin_role(client: TestClient) -> None:
    _register_user(client, "member@example.com", "StrongPassword123!")
    member_token = _login_user(client, "member@example.com", "StrongPassword123!")

    denied_response = client.get(
        "/api/v1/admin/summary",
        headers={"Authorization": f"Bearer {member_token}"},
    )

    assert denied_response.status_code == 403

    admin_token = _login_user(client, "admin@example.com", "AdminPass123!")
    allowed_response = client.get(
        "/api/v1/admin/summary",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert allowed_response.status_code == 200
    assert allowed_response.json()["current_user_role"] == "admin"


def test_login_rejects_invalid_credentials(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "unknown@example.com", "password": "WrongPassword123!"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."
