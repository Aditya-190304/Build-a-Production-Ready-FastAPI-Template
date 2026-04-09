from fastapi.testclient import TestClient

from tests.constants import (
    APP_VERSION_DEFAULT,
    DEFAULT_CORS_ALLOW_HEADERS,
    EXAMPLE_ADMIN_EMAIL,
    EXAMPLE_STRONG_PASSWORD,
    EXAMPLE_USER_EMAIL,
    EXAMPLE_USER_FULL_NAME,
    TEST_ADMIN_PASSWORD,
    TEST_APP_NAME,
    TEST_DUPLICATE_EMAIL,
    TEST_INVALID_EMAIL,
    TEST_INVALID_PASSWORD,
    TEST_MEMBER_EMAIL,
    TEST_SECURE_EMAIL,
    TEST_UNKNOWN_EMAIL,
    TEST_WEAK_PASSWORD,
)


def _register_user(client: TestClient, email: str, password: str) -> None:
    response = client.post(
        "/api/v1/users",
        json={"full_name": EXAMPLE_USER_FULL_NAME, "email": email, "password": password},
    )
    assert response.status_code == 201


def _login_user(client: TestClient, email: str, password: str) -> str:
    response = client.post(
        "/api/v1/auth/tokens",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_health_check_returns_expected_payload(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "app_name": TEST_APP_NAME,
        "environment": "test",
        "version": APP_VERSION_DEFAULT,
    }


def test_user_can_register_login_and_fetch_profile(client: TestClient) -> None:
    _register_user(client, EXAMPLE_USER_EMAIL, EXAMPLE_STRONG_PASSWORD)

    token = _login_user(client, EXAMPLE_USER_EMAIL, EXAMPLE_STRONG_PASSWORD)
    response = client.get(
        "/api/v1/users/current",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == EXAMPLE_USER_EMAIL
    assert response.json()["full_name"] == EXAMPLE_USER_FULL_NAME
    assert response.json()["role"] == "user"


def test_duplicate_registration_is_rejected(client: TestClient) -> None:
    _register_user(client, TEST_DUPLICATE_EMAIL, EXAMPLE_STRONG_PASSWORD)

    response = client.post(
        "/api/v1/users",
        json={
            "full_name": EXAMPLE_USER_FULL_NAME,
            "email": TEST_DUPLICATE_EMAIL,
            "password": EXAMPLE_STRONG_PASSWORD,
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "A user with this email already exists."


def test_registration_rejects_weak_password(client: TestClient) -> None:
    response = client.post(
        "/api/v1/users",
        json={
            "full_name": EXAMPLE_USER_FULL_NAME,
            "email": TEST_SECURE_EMAIL,
            "password": TEST_WEAK_PASSWORD,
        },
    )

    assert response.status_code == 422
    assert "uppercase letter" in response.text


def test_registration_rejects_invalid_email_format(client: TestClient) -> None:
    response = client.post(
        "/api/v1/users",
        json={
            "full_name": EXAMPLE_USER_FULL_NAME,
            "email": TEST_INVALID_EMAIL,
            "password": EXAMPLE_STRONG_PASSWORD,
        },
    )

    assert response.status_code == 422
    assert "email" in response.text.lower()


def test_cors_preflight_returns_expected_headers(client: TestClient) -> None:
    response = client.options(
        "/api/v1/users",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": DEFAULT_CORS_ALLOW_HEADERS,
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
    assert "POST" in response.headers["access-control-allow-methods"]
    assert "Authorization" in response.headers["access-control-allow-headers"]


def test_admin_route_requires_admin_role(client: TestClient) -> None:
    _register_user(client, TEST_MEMBER_EMAIL, EXAMPLE_STRONG_PASSWORD)
    member_token = _login_user(client, TEST_MEMBER_EMAIL, EXAMPLE_STRONG_PASSWORD)

    denied_response = client.get(
        "/api/v1/admin/overview",
        headers={"Authorization": f"Bearer {member_token}"},
    )

    assert denied_response.status_code == 403

    admin_token = _login_user(client, EXAMPLE_ADMIN_EMAIL, TEST_ADMIN_PASSWORD)
    allowed_response = client.get(
        "/api/v1/admin/overview",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert allowed_response.status_code == 200
    assert allowed_response.json()["current_user_role"] == "admin"


def test_login_rejects_invalid_credentials(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/tokens",
        json={"email": TEST_UNKNOWN_EMAIL, "password": TEST_INVALID_PASSWORD},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."
