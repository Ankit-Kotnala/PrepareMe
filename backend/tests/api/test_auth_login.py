from httpx import ASGITransport, AsyncClient


async def test_local_login_returns_role_aware_token(local_auth_client) -> None:
    login_response = await local_auth_client.post(
        "/v1/auth/login",
        json={
            "institution_slug": "prepareme-demo",
            "email": "teacher@prepareme.local",
            "password": "Teacher@123",
        },
    )

    assert login_response.status_code == 200
    login_payload = login_response.json()
    assert login_payload["redirect_path"] == "/teacher"
    assert login_payload["user"]["role"] == "teacher"

    token = login_payload["access_token"]
    me_response = await local_auth_client.get(
        "/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert me_response.status_code == 200
    me_payload = me_response.json()
    assert me_payload["email"] == "teacher@prepareme.local"
    assert me_payload["role"] == "teacher"
    assert me_payload["institution_slug"] == "prepareme-demo"


async def test_local_login_rejects_wrong_institution_or_password(local_auth_client) -> None:
    response = await local_auth_client.post(
        "/v1/auth/login",
        json={
            "institution_slug": "wrong-code",
            "email": "teacher@prepareme.local",
            "password": "Teacher@123",
        },
    )
    assert response.status_code == 401

    response = await local_auth_client.post(
        "/v1/auth/login",
        json={
            "institution_slug": "prepareme-demo",
            "email": "teacher@prepareme.local",
            "password": "wrong-password",
        },
    )
    assert response.status_code == 401


async def test_local_login_requires_turnstile_when_enabled(local_auth_app) -> None:
    local_auth_app.state.settings.turnstile_enabled = True

    transport = ASGITransport(app=local_auth_app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post(
            "/v1/auth/login",
            json={
                "institution_slug": "prepareme-demo",
                "email": "teacher@prepareme.local",
                "password": "Teacher@123",
            },
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Complete the Cloudflare security check and try again."
