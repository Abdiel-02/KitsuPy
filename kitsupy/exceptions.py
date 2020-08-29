from typing import Any, Dict

class ApiException(Exception):
    def __init__(self, data: Dict[str, Any]):
        self._errors = data["errors"][0]
        self.title = self._errors["title"]
        self.detail = self._errors["detail"]
        self.code = int(self._errors["code"])
        self.status = int(self._errors["status"])
        self.message = f"HTTP {self.status} {self.title} {self.detail}"

        super().__init__(self.message)

class KitsuException(ApiException):
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
