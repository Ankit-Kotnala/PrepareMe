from app.core.llm.base import Embedding, LLMProvider, LLMResponse, Prompt
from app.core.types import JSONValue


class NoopLLMProvider(LLMProvider):
    async def complete(self, prompt: Prompt, config: dict[str, JSONValue]) -> LLMResponse:
        _ = config
        return LLMResponse(
            content=f"[noop-llm] Prompt received for mode: {prompt.metadata.get('mode', 'unknown')}",
            model_used="noop-llm",
            input_tokens=0,
            output_tokens=0,
            latency_ms=0,
        )

    async def embed(self, text: str) -> Embedding:
        dimensions = max(len(text.split()), 1)
        return Embedding(vector=[0.0] * min(dimensions, 8), model_used="noop-embedding")

