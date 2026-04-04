from uuid import UUID, uuid4

import pytest_asyncio

from app.core.db.models import Institution, TenantPolicy, User
from app.core.enums import AnswerStrictness, ExplanationDepth, PlanTier, UserRole


def build_auth_headers(*, user_id: UUID, institution_id: UUID, role: UserRole) -> dict[str, str]:
    return {
        "X-PrepareMe-User-Id": str(user_id),
        "X-PrepareMe-Institution-Id": str(institution_id),
        "X-PrepareMe-Role": role.value,
        "X-PrepareMe-Email": f"{role.value}@prepareme.test",
    }


@pytest_asyncio.fixture
async def seeded_policies(app) -> dict[str, object]:
    institution_a_id = uuid4()
    institution_b_id = uuid4()
    user_a_id = uuid4()
    user_b_id = uuid4()
    policy_a_id = uuid4()
    policy_b_id = uuid4()

    async with app.state.db_session_manager.session() as session:
        institution_a = Institution(
            id=institution_a_id,
            name="Institution A",
            slug="institution-a",
            plan_tier=PlanTier.PROFESSIONAL,
        )
        institution_b = Institution(
            id=institution_b_id,
            name="Institution B",
            slug="institution-b",
            plan_tier=PlanTier.PROFESSIONAL,
        )

        user_a = User(
            id=user_a_id,
            institution_id=institution_a_id,
            email="teacher-a@prepareme.test",
            role=UserRole.TEACHER,
        )
        user_b = User(
            id=user_b_id,
            institution_id=institution_b_id,
            email="teacher-b@prepareme.test",
            role=UserRole.TEACHER,
        )

        policy_a = TenantPolicy(
            id=policy_a_id,
            institution_id=institution_a_id,
            answer_strictness=AnswerStrictness.STRICT,
            min_confidence_threshold=0.8,
            content_approval_required=True,
            explanation_depth=ExplanationDepth.DETAILED,
            language="en-IN",
            updated_by=user_a_id,
        )
        policy_b = TenantPolicy(
            id=policy_b_id,
            institution_id=institution_b_id,
            answer_strictness=AnswerStrictness.STANDARD,
            min_confidence_threshold=0.55,
            content_approval_required=True,
            explanation_depth=ExplanationDepth.STANDARD,
            language="en-IN",
            updated_by=user_b_id,
        )

        session.add_all(
            [institution_a, institution_b, user_a, user_b, policy_a, policy_b],
        )
        await session.commit()

    return {
        "institution_a_id": institution_a_id,
        "institution_b_id": institution_b_id,
        "user_a_id": user_a_id,
        "user_b_id": user_b_id,
        "policy_a_id": policy_a_id,
        "policy_b_id": policy_b_id,
    }


async def test_policy_lookup_returns_current_tenant_policy(client, seeded_policies) -> None:
    response = await client.get(
        "/v1/policies/me",
        headers=build_auth_headers(
            user_id=seeded_policies["user_a_id"],
            institution_id=seeded_policies["institution_a_id"],
            role=UserRole.TEACHER,
        ),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == str(seeded_policies["policy_a_id"])
    assert payload["institution_id"] == str(seeded_policies["institution_a_id"])
    assert payload["answer_strictness"] == "strict"


async def test_policy_lookup_for_wrong_tenant_returns_not_found(client, seeded_policies) -> None:
    response = await client.get(
        f"/v1/policies/{seeded_policies['policy_a_id']}",
        headers=build_auth_headers(
            user_id=seeded_policies["user_b_id"],
            institution_id=seeded_policies["institution_b_id"],
            role=UserRole.TEACHER,
        ),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Tenant policy not found."

