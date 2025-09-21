"""Minimal Groq client wrapper.
This is written generically so you can replace the `requests` call with a Gemmini ADK client later.
"""
import json
import requests
from typing import Any
from src.common.custom_exception import CustomException as AppException


class GroqClient:
    def __init__(self, api_key: str, api_url: str, model_name: str = "llama-3.1-8b-instant"):
        self.api_key = api_key
        self.api_url = api_url.rstrip("/")
        self.model_name = model_name

    def generate_text(self, prompt: str, max_tokens: int = 512) -> str:
        """Synchronous text generation call.
        Note: Adapted for Groq OpenAI-compatible chat completions API.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.9
        }
        try:
            resp = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            # Extract text content from response
            return data["choices"][0]["message"]["content"].strip()
        except requests.RequestException as e:
            raise AppException(f"Groq request failed: {e}")


# """Minimal Groq client wrapper.
# This is written generically so you can replace the `requests` call with a Gemmini ADK client later.
# """
# import json
# import requests
# from typing import Any
# from src.common.custom_exception import CustomException as AppException


# class GroqClient:
#     def __init__(self, api_key: str, api_url: str):
#         self.api_key = api_key
#         self.api_url = api_url.rstrip("/")

#     def generate_text(self, prompt: str, max_tokens: int = 512) -> str:
#         """Synchronous text generation call.
#         NOTE: adapt headers/payload to the specific Groq endpoint format you will use.
#         """
#         headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
#         payload = {
#             "input": prompt,
#             "max_tokens": max_tokens,
#             # add other model-specific params here
#         }
#         try:
#             resp = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
#             resp.raise_for_status()
#             data = resp.json()
#             # adapt extraction depending on Groq API shape; we assume data['output'] or data['result']
#             if "output" in data:
#                 out = data["output"]
#             elif "result" in data:
#                 out = data["result"]
#             else:
#                 # fallback: entire response as string
#                 out = json.dumps(data)
#             # If structure is dict with 'text'
#             if isinstance(out, dict) and "text" in out:
#                 return out["text"]
#             # If list, join
#             if isinstance(out, list):
#                 return "\n".join(map(str, out))
#             return str(out)
#         except requests.RequestException as e:
#             raise AppException(f"Groq request failed: {e}")
