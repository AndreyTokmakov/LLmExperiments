import requests
import json
from requests import Response, Session
from typing import Iterator, Optional, Dict, Any


class OllamaRestClient:

    def __init__(self,
                 base_url: str = "http://localhost:11434",
                 timeout: float = 60):
        self.base_url: str = base_url.rstrip("/")
        self.api_url: str = f"{self.base_url}/api"
        self.timeout: float = timeout
        self.session: Session = requests.Session()

    def _request(self,
                 method: str,
                 path: str,
                 *,
                 json_data: Optional[Dict[str, Any]] = None,
                 stream: bool = False,
                 timeout: Optional[float] = None) -> Response:
        response: Response = self.session.request(method=method,
                                                  url=f"{self.api_url}{path}",
                                                  json=json_data,
                                                  stream=stream,
                                                  timeout=timeout or self.timeout)
        response.raise_for_status()
        return response

    @staticmethod
    def _build_payload(model: str,
                       prompt: str,
                       *,
                       stream: bool,
                       system: Optional[str] = None,
                       options: Optional[Dict[str, Any]] = None,
                       keep_alive: Optional[str] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
        }

        if system:
            payload["system"] = system
        if options:
            payload["options"] = options
        if keep_alive:
            payload["keep_alive"] = keep_alive

        return payload

    def generate(self,
                 model: str,
                 prompt: str,
                 *,
                 system: Optional[str] = None,
                 options: Optional[Dict[str, Any]] = None,
                 keep_alive: Optional[str] = None) -> str:
        payload: Dict[str, Any] = self._build_payload(
            model=model,
            prompt=prompt,
            stream=False,
            system=system,
            options=options,
            keep_alive=keep_alive,
        )
        response: Response = self._request("POST", "/generate", json_data=payload)
        data = response.json()
        return data.get("response", "")

    def generate_stream(self,
                        model: str,
                        prompt: str,
                        *,
                        system: Optional[str] = None,
                        options: Optional[Dict[str, Any]] = None,
                        keep_alive: Optional[str] = None) -> Iterator[str]:
        payload: Dict[str, Any] = self._build_payload(
            model=model,
            prompt=prompt,
            stream=True,
            system=system,
            options=options,
            keep_alive=keep_alive,
        )
        with self._request(method="POST",
                           path="/generate",
                           json_data=payload,
                           stream=True) as response:
            for line in response.iter_lines():
                if not line:
                    continue
                try:
                    chunk = json.loads(line.decode("utf-8"))
                except json.JSONDecodeError:
                    continue
                if "response" in chunk:
                    yield chunk["response"]
                if chunk.get("done"):
                    break

    def version(self) -> Dict[str, Any]:
        response: Response = self._request(method="GET", path="/version")
        return response.json()

    def list_models(self) -> Dict[str, Any]:
        response: Response = self._request(method="GET", path="/tags")
        return response.json()

    def show(self, model: str) -> Dict[str, Any]:
        response: Response = self._request(method="POST",
                                           path="/show",
                                           json_data={"name": model},
                                           timeout=300)
        return response.json()

    def ps(self) -> Dict[str, Any]:
        response: Response = self._request(method="GET", path="/ps")
        return response.json()

    def pull_model(self, model: str) -> None:
        self._request(method="POST",
                      path="/pull",
                      json_data={"name": model},
                      timeout=300)

    def delete_model(self, model: str) -> None:
        self._request(method="DELETE",
                      path="/delete",
                      json_data={"name": model})

    def warmup(self, model: str, keep_alive: str = "inf") -> None:
        self.generate(model=model,
                      prompt="warmup",
                      keep_alive=keep_alive)

    def close(self) -> None:
        self.session.close()
