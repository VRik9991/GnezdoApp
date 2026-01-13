from typing import Any, Optional

import httpx

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
    def _get(self, path: str, params: Optional[dict[str, Any]] = None) -> Any:
        if not path.startswith("/"):
            path = f"/{path}"
        with httpx.Client(base_url=self.base_url) as client:
            response = client.get(path, params=params)
            response.raise_for_status()
            return response.json()



    def _post(self, path, json):
        with httpx.Client() as client:
            response = client.post(
                f"{self.base_url}{path}",
                json=json
            )
            print(response.status_code)
            print(response.json())

    def register(self, email: str, password: str):
        return self._post("/auth/register", {"email": email, "password": password})

    def user_credentials(self):
        return self._get("/user_credentials")   