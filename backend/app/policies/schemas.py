from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.core.enums import AnswerStrictness, ExplanationDepth
from app.core.types import JSONValue


class TenantPolicyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    institution_id: UUID
    answer_strictness: AnswerStrictness
    min_confidence_threshold: float
    content_approval_required: bool
    explanation_depth: ExplanationDepth
    language: str
    custom_rules: dict[str, JSONValue]
    updated_at: datetime

