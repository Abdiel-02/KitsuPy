import json
from typing import Any, Dict, List, Optional

class Character:
    def __init__(self, response: Dict[str, Any]):
        data = response.get("data", {})
        attributes = data.get("attributes", {})

        self.id: int = self.__convert_to(data.get("id", None), int)
        self.slug: str = attributes.get("slug", None)
        self.names: List[str] = attributes.get("names", None)
        self.canonical_name: str = attributes.get("canonicalName", None)
        self.other_names: List[str] = attributes.get("otherNames", None)
        self.name: str = attributes.get("name", None)
        self.mal_id: int = attributes.get("malId", None)
        self.description: str = attributes.get("description", None)
        self.image: str = attributes["image"]["original"] if attributes["image"] else None

    def __convert_to(self, value, t):
        try:
            return t(value)
        except Exception:
            return None
    
    def to_json(self, indent: Optional[int] = 2):
        return json.dumps(self.__dict__, indent=indent, ensure_ascii=False, default=str)


class AnimeCharacter(Character):
    def __init__(self, response: Dict[str, Any]):
        super().__init__(response)
        included = response.get("included", [])

        self.voice_actor: Dict[str, Dict[str, str]] = self.__get_voice_actor(included)

    def __get_voice_actor(self, included) -> Dict[str, Dict[str, str]]:
        temp = []
        locales = [locale["attributes"]["locale"] for locale in included if locale["type"] == "characterVoices"]
        for person in included:
            if person["type"] == "people":
                temp.append({
                        "name": person["attributes"]["name"],
                        "decription": person["attributes"]["description"],
                        "image": person["attributes"]["image"]["original"] if person["attributes"]["image"] else None
                    })

        return {key:value for key, value in zip(locales, temp)}

class MangaCharacter(Character):
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
