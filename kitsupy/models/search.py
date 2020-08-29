import math
import json
from typing import Any, Dict, List, Optional
from .base import General

class GeneralResult(General):
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)

class SearchContainer:
    def __init__(self, data: Dict[str, Any], elements: List[GeneralResult], page: int, limit: int):
        self.page = page
        self.results = elements
        self.total_page = math.ceil(data["meta"]["count"] / limit)
        self.total_result = data["meta"]["count"]
    
    def to_json(self, indent: Optional[int] = 2):
        return json.dumps(self.__dict__, indent=indent, ensure_ascii=False, default=str)
