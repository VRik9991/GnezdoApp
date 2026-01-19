import httpx

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def _get(self, path):
        with httpx.Client() as client:
            response = client.get(
                f"{self.base_url}{path}",)
            print(response.status_code)
            return response.json()

    def _put(self, path, json):
        with httpx.Client() as client:
            response = client.put(
                f"{self.base_url}{path}",
                json=json
            )
            print(response.status_code)

    def _post(self, path, json):
        with httpx.Client() as client:
            response = client.post(
                f"{self.base_url}{path}",
                json=json
            )
            print(response.status_code)
            print(response.json())
    def get_character(self):
        pass
    def get_all_character(self):
        pass
    def create_library_item(self, name: str, item_type: str, item_text: str, date: str, access: str, author: str, picture: str):
        return self._post("/library", {"name": name, "item_text": item_text, "item_type": item_type, "date": date, "access": access, "author": author, "picture": picture})
    def get_library(self):
        return self._get("/library/all")
    def edit_library_item(self, id, name: str, item_type: str, item_text: str, access: str, picture: str):
        return self._put("/library", {"id": id, "name": name, "item_text": item_text, "item_type": item_type, "access": access, "picture": picture})
