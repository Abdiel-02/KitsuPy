from typing import Any, Dict, List
from .base import Model

class AnimeModel(Model):
    def __init__(self, response: Dict[str, Any]):
        super().__init__(response)
        data = response.get("data", {})
        included = response.get("included", [])
        attributes = data.get("attributes", {})

        self.episode_count: int = attributes.get("episodeCount", None)
        self.episode_length: int = attributes.get("episodeLength", None)
        self.youtube_video_id: str = attributes.get("youtubeVideoId", None)
        self.producer: List[str] = self.__get_producers(included)
        self.licensors: List[str] = self.__get_licensors(included)
        self.studies: List[str] = self.__get_studies(included)

    def __get_producers(self, included) -> List[str]:
        return [
            p["attributes"]["name"] for p in included
            if p["type"] == "producers" and p["id"] in [
                ap["relationships"]["producer"]["data"]["id"] for ap in included
                if ap["type"] == "animeProductions" and ap["attributes"]["role"] == "producer"
            ]
        ]

    def __get_licensors(self, included) -> List[str]:
        return [
            l["attributes"]["name"] for l in included
            if l["type"] == "producers" and l["id"] in [
                ap["relationships"]["producer"]["data"]["id"] for ap in included
                if ap["type"] == "animeProductions" and ap["attributes"]["role"] == "licensor"
            ]
        ]

    def __get_studies(self, included) -> List[str]:
        return [
            s["attributes"]["name"] for s in included
            if s["type"] == "producers" and s["id"] in [
                ap["relationships"]["producer"]["data"]["id"] for ap in included
                if ap["type"] == "animeProductions" and ap["attributes"]["role"] == "studio"
            ]
        ]
