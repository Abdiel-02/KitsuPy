from typing import Any, Dict
from .base import General

class Franchise(General):
    def __init__(self, root: Dict[str, Any], data: Dict[str, Any]):
        super().__init__(data)
        self.role = root["attributes"]["role"]
    