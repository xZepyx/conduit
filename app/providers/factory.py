from app.providers.openai_provider import OpenAIProvider
from app.providers.anthropic_provider import AnthropicProvider
from app.providers.gemini_provider import GeminiProvider
from app.providers.groq_provider import GroqProvider
from app.providers.openrouter import OpenRouterProvider


MODEL_MAP = {
    # OpenRouter
    "llama3": ("openrouter", "meta-llama/llama-3.3-70b-instruct"),
    "deepseek": ("openrouter", "deepseek/deepseek-chat"),
    "gpt4": ("openrouter", "openai/gpt-4.1"),
    # OpenAI
    "gpt-4o": ("openai", "gpt-4o"),
    "gpt-4o-mini": ("openai", "gpt-4o-mini"),
    "gpt-4-turbo": ("openai", "gpt-4-turbo"),
    "gpt-3.5-turbo": ("openai", "gpt-3.5-turbo"),
    # Anthropic
    "claude-sonnet-4": ("anthropic", "claude-sonnet-4-20250514"),
    "claude-3.5-sonnet": ("anthropic", "claude-3-5-sonnet-20241022"),
    "claude-3.5-haiku": ("anthropic", "claude-3-5-haiku-20241022"),
    "claude-3-opus": ("anthropic", "claude-3-opus-20240229"),
    # Gemini
    "gemini-2.5-pro": ("gemini", "gemini-2.5-pro"),
    "gemini-2.5-flash": ("gemini", "gemini-2.5-flash"),
    "gemini-2.0-flash": ("gemini", "gemini-2.0-flash"),
    # Groq
    "llama3-70b": ("groq", "llama3-70b-8192"),
    "llama3-8b": ("groq", "llama3-8b-8192"),
    "mixtral": ("groq", "mixtral-8x7b-32768"),
    "gemma2": ("groq", "gemma2-9b-it"),
    "deepseek-r1": ("groq", "deepseek-r1-distill-llama-70b"),
}


PREFIX_ROUTES = [
    ("gpt-", "openai"),
    ("o1-", "openai"),
    ("o3-", "openai"),
    ("claude-", "anthropic"),
    ("gemini-", "gemini"),
]


PROVIDER_INSTANCES = {
    "openai": OpenAIProvider(),
    "anthropic": AnthropicProvider(),
    "gemini": GeminiProvider(),
    "groq": GroqProvider(),
    "openrouter": OpenRouterProvider(),
}


def get_provider(model: str):
    """Determine the provider for a given model name."""
    if model in MODEL_MAP:
        provider_name, _ = MODEL_MAP[model]
        return PROVIDER_INSTANCES[provider_name]

    for prefix, provider_name in PREFIX_ROUTES:
        if model.startswith(prefix):
            return PROVIDER_INSTANCES[provider_name]

    return PROVIDER_INSTANCES["openrouter"]


def get_model_name(model: str) -> str:
    """Get the actual model ID to send to the provider API."""
    if model in MODEL_MAP:
        _, actual = MODEL_MAP[model]
        return actual
    return model


def get_all_models():
    """Return all available model aliases."""
    return list(MODEL_MAP.keys())


def get_model_info(model: str) -> dict:
    """Return model details for the /api/show endpoint."""
    return {
        "license": "",
        "modelfile": "",
        "parameters": "",
        "template": "",
        "details": {
            "family": "llama",
            "format": "gguf",
            "parameter_size": "70B",
            "quantization_level": "Q4_K_M",
        },
    }
