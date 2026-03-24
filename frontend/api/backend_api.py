from typing import Any, Optional

import httpx

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(base_url=self.base_url, timeout=10.0)

    def _get(self, path: str, params: Optional[dict[str, Any]] = None) -> Any:
        if not path.startswith("/"):
            path = f"/{path}"
        response = self._client.get(path, params=params)
        response.raise_for_status()
        return response.json()


    def _put(self, path: str, json: Optional[dict[str, Any]] = None) -> Any:
        if not path.startswith("/"):
            path = f"/{path}"
        response = self._client.put(path, json=json)
        response.raise_for_status()
        return response.json()



    def _post(self, path, json):
        response = self._client.post(path, json=json)
        response.raise_for_status()
        return response.json()

    def register(self, email: str, password: str):
        return self._post("/auth/register", {"email": email, "password": password})

    def user_credentials(self):
        return self._get("/user_credentials")   
    
    def get_user(self, email: str):
        return self._get("/user", {"email": email})
    
    def put_user(self, data: dict):
        return self._put("/user", data)
