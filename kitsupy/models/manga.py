from typing import Any, Dict
from .base import Model

class MangaModel(Model):
    def __init__(self, response: Dict[str, Dict[str, Any]]):
        super().__init__(response)
        data = response.get("data", {})
        attributes = data.get("attributes", {})

        self.chapter_count: int = attributes.get("chapterCount", None)
        self.volume_count: int = attributes.get("volumeCount", None)
        self.serialization: str = attributes.get("serialization", None)
