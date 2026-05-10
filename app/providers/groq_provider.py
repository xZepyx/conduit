from app.providers.openai_provider import OpenAIProvider


class GroqProvider(OpenAIProvider):
    """Groq uses the OpenAI-compatible API format."""

    provider_name = "groq"
    api_key_env = "GROQ_API_KEY"
    base_url = "https://api.groq.com/openai/v1/chat/completions"
