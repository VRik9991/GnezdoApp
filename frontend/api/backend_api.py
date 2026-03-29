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


    def _put(self, path: str, json: Optional[dict[str, Any]] = None) -> Any:
        if not path.startswith("/"):
            path = f"/{path}"
        with httpx.Client(base_url=self.base_url) as client:
            response = client.put(path, json=json)
            response.raise_for_status()
            return response.json()        



    def _post(self, path, json):
        if not path.startswith("/"):
            path = f"/{path}"
        with httpx.Client(base_url=self.base_url) as client:
            response = client.post(path, json=json)
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

    def get_actions(self, user_email: Optional[str] = None):
        params = {"user_email": user_email} if user_email else None
        return self._get("/action", params)

    def create_action(self, data: dict):
        return self._post("/action", data)

    def update_action(self, action_id: str, data: dict):
        return self._put(f"/action/{action_id}", data)
