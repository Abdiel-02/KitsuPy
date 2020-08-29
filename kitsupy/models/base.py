import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from ..enums import Genres

class Model:
    def __init__(self, response: Dict[str, Dict[str, Any]]):
        data = response.get("data", {})
        included = response.get("included", [])
        attributes = data.get("attributes", {})
        relationship = data.get("relationships", {})

        self.id: int = self.__convert_to(data.get("id", None), int)
        self.type: str = data.get("type", None)
        self.created_at = self.__get_dates(attributes, "createdAt")
        self.updated_at = self.__get_dates(attributes, "updatedAt")
        self.slug: str = attributes.get("slug", None)
        self.synopsis: str = attributes.get("synopsis", None)
        self.description: str = attributes.get("description", None)
        self.cover_image_top_off_set: int = attributes.get("coverImageTopOffset", None)
        self.titles: Dict[str, str] = attributes.get("titles", None)
        self.canonical_title: str = attributes.get("canonicalTitle", None)
        self.abbreviated_titles: List[str] = attributes.get("abbreviatedTitles", None)
        self.average_rating: float = self.__convert_to(attributes.get("averageRating", None), float)
        self.rating_frequencies: Dict[str, str] = attributes.get("ratingFrequencies", None)
        self.user_count: int = attributes.get("userCount", None)
        self.favorites_count: int = attributes.get("favoritesCount", None)
        self.start_date = self.__get_dates(attributes, "startDate")
        self.end_date = self.__get_dates(attributes, "endDate")
        self.next_release = attributes.get("nextRelease", None)
        self.popularity_rank: int = attributes.get("popularityRank", None)
        self.rating_rank: int = attributes.get("ratingRank", None)
        self.age_rating: str = attributes.get("ageRating", None)
        self.age_rating_guide: str = attributes.get("ageRatingGuide", None)
        self.subtype: str = attributes.get("subtype", None)
        self.status: str = attributes.get("status", None)
        self.tba = attributes.get("tba", None)
        self.poster_images: Dict[str, str] = self.__get_images(attributes, "posterImage")
        self.cover_images: Dict[str, str] = self.__get_images(attributes, "coverImage")
        self.genres: List[str] = self.__get_genres(relationship)
        self.main_characters: List[int] = self.__get_main_characters(included)
        self.supporting_characters: List[int] = self.__get_supporting_characters(included)

    def __convert_to(self, value, t):
        try:
            return t(value)
        except Exception:
            return None

    def __get_dates(self, attributes: dict, key: str) -> datetime:
        _date = attributes.get(key, None)
        if _date: return datetime.fromisoformat(_date.replace("Z", "+00:00"))
        return None
    
    def __get_images(self, attributes: dict, key: str) -> Dict[str, str]:
        images = attributes.get(key, None)
        if images: return {size:value for (size, value) in images.items() if size != "meta"}
        return None

    def __get_genres(self, relationship: dict) -> List[str]:
        return [
            genre.name.replace("_", " ").lower().title() for genre in Genres
            if genre.value in [
                int(d["id"]) for d in relationship["genres"]["data"]
            ]
        ]

    def __get_main_characters(self, included) -> List[int]:
        return [
            int(d["id"]) for d in included
            if d["type"] == "mediaCharacters"
            and d["attributes"]["role"] == "main"
        ]
    
    def __get_supporting_characters(self, included) -> List[int]:
        return [
            int(d["id"]) for d in included
            if d["type"] == "mediaCharacters"
            and d["attributes"]["role"] == "supporting"
        ]
    
    def to_json(self, indent: Optional[int] = 2):
        return json.dumps(self.__dict__, indent=indent, ensure_ascii=False, default=str)


class General:
    def __init__(self, response: Dict[str, Any]):
        data = response
        attributes = response.get("attributes", {})

        self.id: int = int(data.get("id", None))
        self.type: str = data.get("type", None)
        self.titles: Dict[str, str] = attributes.get("titles", None)
        self.canonical_title: str = attributes.get("canonicalTitle", None)
        self.average_rating: float = self.__convert_to(attributes.get("averageRating", None), float)
        self.popularity_rank: int = attributes.get("popularityRank", None)
        self.rating_rank: int = attributes.get("ratingRank", None)
        self.subtype: str = attributes.get("subtype", None)
        self.status: str = attributes.get("status", None)
        self.poster_images: Dict[str, str] = self.__get_images(attributes, "posterImage")
        self.cover_images: Dict[str, str] = self.__get_images(attributes, "coverImage")

    def __convert_to(self, value, t):
        try:
            return t(value)
        except Exception:
            return None

    def __get_images(self, attributes: dict, key: str) -> Dict[str, str]:
        images = attributes.get(key, None)
        if images: return {size:value for (size, value) in images.items() if size != "meta"}
        return None

    def to_json(self, indent: Optional[int] = 2):
        return json.dumps(self.__dict__, indent=indent, ensure_ascii=False, default=str)
