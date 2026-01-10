import httpx

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def _get(self, path):
        with httpx.Client() as client:
            response = client.get(
                f"{self.base_url}{path}",)
            print(response.status_code)
            print(response.json())
            return response.json()

    def _post(self, path, json):
        with httpx.Client() as client:
            response = client.post(
                f"{self.base_url}{path}",
                json=json
            )
            print(response.status_code)
            print(response.json())

    async def register(self, email: str, password: str):
        return self._post("/auth/register", {"email": email, "password": password})
    def get_character(self):
        pass
    def get_all_character(self):
        pass
    def create_library_item(self, name: str, item_type: str, item_text: str, date: str, access: str, author: str, picture: bytes):
        return self._post("/library", {"name": name, "item_text": item_text, "item_type": item_type, "date": date, "access": access, "author": author, "picture": picture})
    def get_library(self):
        return self._get("/library")