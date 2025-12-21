import httpx

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def _get(self, path):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}{path}",)
            print(response.status_code)
            print(response.json())

    async def _post(self, path, json):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}{path}",
                json=json
            )
            print(response.status_code)
            print(response.json())

    async def register(self, email: str, password: str):
        return self._post("/auth/register", {"email": email, "password": password})