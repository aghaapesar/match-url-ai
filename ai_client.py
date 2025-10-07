import os
import json
import time
from typing import Dict, Any, Optional
import requests


class AIClientError(Exception):
    pass


class AIClient:
    """
    Provider-agnostic AI chat client supporting OpenAI, Azure OpenAI, Anthropic,
    and OpenAI-compatible/local endpoints. Focused on JSON responses.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config or {}
        self.provider = (self.config.get("provider") or "openai").lower()
        self.timeout_seconds = int(self.config.get("timeout_seconds", 60))
        self.max_retries = int(self.config.get("max_retries", 3))
        self.retry_base_delay = float(self.config.get("retry_base_delay", 1.5))
        self.qps = float(self.config.get("qps", 1.0))
        self._last_call_ts: float = 0.0

        self.model = self.config.get("model")
        self.temperature = float(self.config.get("temperature", 0.0))
        self.response_json = bool(self.config.get("response_json", True))

        self.openai_api_key = self._resolve_secret(self.config.get("openai_api_key"))
        self.openai_base_url = self.config.get("openai_base_url", "https://api.openai.com/v1")

        self.azure_endpoint = self.config.get("azure_endpoint")
        self.azure_api_key = self._resolve_secret(self.config.get("azure_api_key"))
        self.azure_api_version = self.config.get("azure_api_version", "2024-02-15-preview")
        self.azure_deployment = self.config.get("azure_deployment")

        self.anthropic_api_key = self._resolve_secret(self.config.get("anthropic_api_key"))
        self.anthropic_api_version = self.config.get("anthropic_api_version", "2023-06-01")

        self.compatible_base_url = self.config.get("compatible_base_url")
        self.compatible_api_key = self._resolve_secret(self.config.get("compatible_api_key"))

    def _resolve_secret(self, value: Optional[str]) -> Optional[str]:
        if not value:
            return None
        if isinstance(value, str) and value.startswith("env:"):
            return os.getenv(value.split(":", 1)[1])
        return value

    def _respect_rate_limit(self):
        if self.qps <= 0:
            return
        spacing = 1.0 / self.qps
        now = time.time()
        since = now - self._last_call_ts
        if since < spacing:
            time.sleep(spacing - since)
        self._last_call_ts = time.time()

    def _post_json(self, url: str, headers: Dict[str, str], payload: Dict[str, Any]) -> requests.Response:
        self._respect_rate_limit()
        return requests.post(url, headers=headers, json=payload, timeout=self.timeout_seconds)

    def _retry_loop(self, fn):
        last_exc = None
        for attempt in range(self.max_retries):
            try:
                return fn()
            except Exception as e:
                last_exc = e
                backoff = (self.retry_base_delay ** attempt) + (0.05 * attempt)
                time.sleep(backoff)
        raise AIClientError(f"AI request failed after {self.max_retries} retries: {last_exc}")

    def chat_json(self, system_prompt: str, user_prompt: str, max_output_tokens: int = 512) -> Dict[str, Any]:
        if self.provider == "openai":
            return self._chat_openai(system_prompt, user_prompt, max_output_tokens)
        if self.provider == "azure":
            return self._chat_azure(system_prompt, user_prompt, max_output_tokens)
        if self.provider == "anthropic":
            return self._chat_anthropic(system_prompt, user_prompt, max_output_tokens)
        if self.provider in {"openai_compatible", "local", "compatible", "liara"}:
            return self._chat_openai_compatible(system_prompt, user_prompt, max_output_tokens)
        raise AIClientError(f"Unsupported provider: {self.provider}")

    def _chat_openai(self, system_prompt: str, user_prompt: str, max_output_tokens: int) -> Dict[str, Any]:
        if not self.openai_api_key:
            raise AIClientError("Missing OpenAI API key")
        if not self.model:
            raise AIClientError("Missing OpenAI model in config")
        url = f"{self.openai_base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "max_tokens": max_output_tokens,
        }
        if self.response_json:
            payload["response_format"] = {"type": "json_object"}

        def _do():
            resp = self._post_json(url, headers, payload)
            if resp.status_code >= 400:
                raise AIClientError(f"OpenAI error {resp.status_code}: {resp.text}")
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            return self._ensure_json(content)

        return self._retry_loop(_do)

    def _chat_openai_compatible(self, system_prompt: str, user_prompt: str, max_output_tokens: int) -> Dict[str, Any]:
        if not self.compatible_base_url:
            raise AIClientError("Missing compatible_base_url for OpenAI-compatible provider")
        if not self.model:
            raise AIClientError("Missing model in config")
        base = self.compatible_base_url.rstrip('/')
        # If base already ends with /v1, don't append another /v1
        if base.endswith('/v1'):
            url = f"{base}/chat/completions"
        else:
            url = f"{base}/v1/chat/completions"
        headers = {"Content-Type": "application/json"}
        if self.compatible_api_key:
            headers["Authorization"] = f"Bearer {self.compatible_api_key}"
        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "max_tokens": max_output_tokens,
        }
        if self.response_json:
            payload["response_format"] = {"type": "json_object"}

        def _do():
            resp = self._post_json(url, headers, payload)
            if resp.status_code >= 400:
                raise AIClientError(f"Compatible provider error {resp.status_code}: {resp.text}")
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            return self._ensure_json(content)

        return self._retry_loop(_do)

    def _chat_azure(self, system_prompt: str, user_prompt: str, max_output_tokens: int) -> Dict[str, Any]:
        if not (self.azure_endpoint and self.azure_api_key and self.azure_deployment):
            raise AIClientError("Missing Azure OpenAI settings: endpoint/api_key/deployment")
        url = (
            f"{self.azure_endpoint.rstrip('/')}/openai/deployments/{self.azure_deployment}/chat/completions"
            f"?api-version={self.azure_api_version}"
        )
        headers = {
            "api-key": self.azure_api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "temperature": self.temperature,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "max_tokens": max_output_tokens,
        }
        if self.response_json:
            payload["response_format"] = {"type": "json_object"}

        def _do():
            resp = self._post_json(url, headers, payload)
            if resp.status_code >= 400:
                raise AIClientError(f"Azure OpenAI error {resp.status_code}: {resp.text}")
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            return self._ensure_json(content)

        return self._retry_loop(_do)

    def _chat_anthropic(self, system_prompt: str, user_prompt: str, max_output_tokens: int) -> Dict[str, Any]:
        if not self.anthropic_api_key:
            raise AIClientError("Missing Anthropic API key")
        if not self.model:
            raise AIClientError("Missing Anthropic model in config")
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.anthropic_api_key,
            "anthropic-version": self.anthropic_api_version,
            "content-type": "application/json",
        }
        payload = {
            "model": self.model,
            "max_tokens": max_output_tokens,
            "temperature": self.temperature,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": user_prompt},
            ],
        }

        def _do():
            resp = self._post_json(url, headers, payload)
            if resp.status_code >= 400:
                raise AIClientError(f"Anthropic error {resp.status_code}: {resp.text}")
            data = resp.json()
            parts = data.get("content") or []
            text = "".join(part.get("text", "") for part in parts if part.get("type") == "text")
            return self._ensure_json(text)

        return self._retry_loop(_do)

    def _ensure_json(self, content: str) -> Dict[str, Any]:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            start = content.find("{")
            end = content.rfind("}")
            if start != -1 and end != -1 and end > start:
                fragment = content[start : end + 1]
                return json.loads(fragment)
            raise AIClientError(f"Model did not return valid JSON: {content[:200]}")
