from dataclasses import dataclass, field
from typing import Protocol

from app.core.types import JSONValue


@dataclass(slots=True)
class Prompt:
    system: str
    user: str
    context_chunks: list[dict[str, JSONValue]] = field(default_factory=list)
    metadata: dict[str, JSONValue] = field(default_factory=dict)


@dataclass(slots=True)
class LLMResponse:
    content: str
    model_used: str
    input_tokens: int
    output_tokens: int
    latency_ms: int


@dataclass(slots=True)
class Embedding:
    vector: list[float]
    model_used: str


class LLMProvider(Protocol):
    async def complete(self, prompt: Prompt, config: dict[str, JSONValue]) -> LLMResponse: ...

    async def embed(self, text: str) -> Embedding: ...

