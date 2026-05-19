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



    def _post(
        self,
        path: str,
        json: dict[str, Any],
        params: Optional[dict[str, Any]] = None,
    ) -> Any:
        if not path.startswith("/"):
            path = f"/{path}"
        with httpx.Client(base_url=self.base_url) as client:
            response = client.post(path, params=params, json=json)
            response.raise_for_status()
            return response.json()

    def _delete(self, path: str, params: Optional[dict[str, Any]] = None) -> Any:
        if not path.startswith("/"):
            path = f"/{path}"
        with httpx.Client(base_url=self.base_url) as client:
            response = client.delete(path, params=params)
            response.raise_for_status()
            return response.json()

    def _delete_json(
        self,
        path: str,
        json: dict[str, Any],
        params: Optional[dict[str, Any]] = None,
    ) -> Any:
        if not path.startswith("/"):
            path = f"/{path}"
        with httpx.Client(base_url=self.base_url) as client:
            response = client.request("DELETE", path, params=params, json=json)
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

    def create_news(self, data: dict):
        return self._post("/news", data)

    def get_news(self, name: str):
        return self._get("/news", {"name": name})

    def change_news(self, data: dict):
        return self._put("/news", data)

    def delete_news(self, name: str):
        return self._delete("/news", {"name": name})

    def post_comment(self, news_name: str, data: dict):
        return self._post("/comment", data, {"news_name": news_name})

    def delete_comment(self, news_name: str, data: dict):
        return self._delete_json("/comment", data, {"news_name": news_name})
