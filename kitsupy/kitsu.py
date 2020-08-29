from enum import Enum
from json import dumps
from requests import Session
from typing import Any, Dict, List, Optional, Tuple, TypeVar, Union

from .exceptions import KitsuException
from .models import *
from .enums import *

class Kitsu:
    def __init__(self):
        self.url = "https://kitsu.io/api/edge"
        self.headers = {
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json"
        }
        self.session = Session()
        self.session.headers.update(self.headers)        

    def __fetch__(self, url) -> Dict[str, Any]:
        response = self.session.get(url)
        data = response.json()
        if response.status_code != 200:
            raise KitsuException(data)
        return data

    def __get_filters__(self, media: Media, filters: Dict[Filter, List[Union[Enum, int]]]) -> str:
        to_string = lambda iterable, sep: sep.join(iterable)
        is_type = lambda iterable, t: all(isinstance(value, t) for value in iterable)
        in_range = lambda iterable, _min, _max: all(n >= _min and n <= _max for n in iterable)

        temp = {}
        for key, values in filters.items():
            if key == Filter.AGE_RATING and media == Media.ANIME:
                aux = [value.value for value in values if value in AgeRating]
                temp[key.value] = to_string(aux, ",")

            if key == Filter.AVERAGE_RATING and is_type(values, int) and in_range(values, 5, 100):
                if len(values) == 1: temp[key.value] = f"{values[0]}.."
                elif len(values) > 1: temp[key.value] = to_string([f"{values[0]}", f"{values[-1]}"], "..")

            if key == Filter.GENRES:
                aux = [value.name.lower().replace("_", "-") for value in values if value in Genres]
                temp[key.value] = to_string(aux, ",")

            if key == Filter.SEASON and media == Media.ANIME:
                aux = [value.value for value in values if value in Season]
                temp[key.value] = to_string(aux, ",")

            if key == Filter.SUBTYPE:
                if media == Media.ANIME:
                    aux = [value.value for value in values if value in AnimeSubtype]
                if media == Media.MANGA:
                    aux = [value.value for value in values if value in MangaSubtype]
                temp[key.value] = to_string(aux, ",")

            if key == Filter.YEAR and is_type(values, int) and in_range(values, 1868, 2030):
                if len(values) == 1: temp[key.value] = f"{values[0]}.."
                elif len(values) > 1: temp[key.value] = to_string([f"{values[0]}", f"{values[-1]}"], "..")

        _filter = ""
        for key in sorted(temp.keys()):
            if temp[key]: _filter += f"filter[{key}]={temp[key]}&"
        return _filter
    
    def anime(self, id: int) -> AnimeModel:
        url = f"{self.url}/anime/{id}?include=genres,animeProductions.producer,characters"
        data = self.__fetch__(url)
        return AnimeModel(data)
    
    def manga(self, id: int) -> MangaModel:
        url = f"{self.url}/manga/{id}?include=genres,characters"
        data = self.__fetch__(url)
        return MangaModel(data)
    
    def character(self, media: Media, id: int) -> Union[AnimeCharacter, MangaCharacter]:        
        url = f"{self.url}/media-characters/{id}/character" if media == Media.MANGA \
            else f"{self.url}/media-characters/{id}/character?include=mediaCharacters.voices.person"

        data = self.__fetch__(url)
        if media == Media.ANIME: return AnimeCharacter(data)
        if media == Media.MANGA: return MangaCharacter(data)

    def franchises(self, media: Media, id: int) -> Tuple[Franchise]:
        url = f"{self.url}/media-relationships?filter[source_id]={id}&filter[source_type]={media.value.title()}&include=destination&sort=role"
        data = self.__fetch__(url)
        return tuple(Franchise(root, _data) for root, _data in zip(data["data"], data["included"]))

    def popularity(
        self, media: Media,
        page: Optional[int] = 1,
        filters: Optional[Dict[Filter, List[Union[Enum, int]]]] = {},
        limit: Optional[int] = 10
    ) -> SearchContainer:
        url = ""
        offset = limit * (page - 1)
        _filters = self.__get_filters__(media, filters)
        if _filters:
            url = f"{self.url}/{media.value}?{_filters}page[limit]={limit}&page[offset]={offset}&sort=-user_count"
        else:
            url = f"{self.url}/{media.value}?page[limit]={limit}&page[offset]={offset}&sort=-user_count"
        data = self.__fetch__(url)
        temp = [GeneralResult(d) for d in data["data"]]
        return SearchContainer(data, temp, page, limit)
    
    def top_rate(
        self, media: Media,
        page: Optional[int] = 1,
        filters: Optional[Dict[Filter, List[Union[Enum, int]]]] = {},
        limit: Optional[int] = 10
    ) -> SearchContainer:
        offset = limit * (page - 1)
        _filters = self.__get_filters__(media, filters)
        if _filters:
            url = f"{self.url}/{media.value}?{_filters}page[limit]={limit}&page[offset]={offset}&sort=-averageRating"
        else:
            url = f"{self.url}/{media.value}?page[limit]={limit}&page[offset]={offset}&sort=-averageRating"
        data = self.__fetch__(url)
        temp = [GeneralResult(d) for d in data["data"]]
        return SearchContainer(data, temp, page, limit)

    def upcoming(
        self, media: Media,
        page: Optional[int] = 1,
        filters: Optional[Dict[Filter, List[Union[Enum, int]]]] = {},
        limit: Optional[int] = 10
    ) -> SearchContainer:
        offset = limit * (page - 1)
        _filters = self.__get_filters__(media, filters)
        if _filters:
            url = f"{self.url}/{media.value}?{_filters}page[limit]={limit}&page[offset]={offset}&sort=-startDate"
        else:
            url = f"{self.url}/{media.value}?page[limit]={limit}&page[offset]={offset}&sort=-startDate"
        data = self.__fetch__(url)
        temp = [GeneralResult(d) for d in data["data"]]
        return SearchContainer(data, temp, page, limit)

    def latest(
        self, media: Media,
        page: Optional[int] = 1,
        filters: Optional[Dict[Filter, List[Union[Enum, int]]]] = {},
        limit: Optional[int] = 10
    ) -> SearchContainer:
        offset = limit * (page - 1)
        _filters = self.__get_filters__(media, filters)
        if _filters:
            url = f"{self.url}/{media.value}?{_filters}page[limit]={limit}&page[offset]={offset}&sort=-created_at"
        else:
            url = f"{self.url}/{media.value}?page[limit]={limit}&page[offset]={offset}&sort=-created_at"
        data = self.__fetch__(url)
        temp = [GeneralResult(d) for d in data["data"]]
        return SearchContainer(data, temp, page, limit)

    def search(self, media: Media, query: str, page: Optional[int] = 1, limit: Optional[int] = 10) -> SearchContainer:
        offset = limit * (page - 1)
        url = f"{self.url}/{media.value}?filter[text]={query}&page[limit]={limit}&page[offset]={offset}"
        data = self.__fetch__(url)
        temp = [GeneralResult(d) for d in data["data"]]
        return SearchContainer(data, temp, page, limit)
