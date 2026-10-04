import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "").strip()

NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"

DEFAULT_MODEL = "nvidia/nemotron-3.5-lightning-30b-a3b"


def get_client():
    if not NVIDIA_API_KEY:
        raise ValueError("NVIDIA_API_KEY is not set in .env")

    return OpenAI(
        api_key=NVIDIA_API_KEY,
        base_url=NVIDIA_BASE_URL
    )