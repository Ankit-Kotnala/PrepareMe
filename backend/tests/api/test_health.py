async def test_liveness_is_public(client) -> None:
    response = await client.get("/v1/health/liveness")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "environment": "test"}


async def test_auth_me_resolves_request_context(client) -> None:
    response = await client.get(
        "/v1/auth/me",
        headers={
            "X-PrepareMe-User-Id": "11111111-1111-1111-1111-111111111111",
            "X-PrepareMe-Institution-Id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "X-PrepareMe-Role": "teacher",
            "X-PrepareMe-Email": "teacher@prepareme.test",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["user_id"] == "11111111-1111-1111-1111-111111111111"
    assert payload["institution_id"] == "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    assert payload["role"] == "teacher"

