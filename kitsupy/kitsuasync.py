import asyncio
from aiohttp import ClientSession
from enum import Enum
from json import dumps
from typing import Any, Dict, List, Optional, Tuple, TypeVar, Union

from .exceptions import KitsuException
from .models import *
from .enums import *

KitsuAsyncT = TypeVar("KitsuAsyncT", bound="KitsuAsync")

class KitsuAsync:
    def __init__(self):
        self.url = "https://kitsu.io/api/edge"
        self.headers = {
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json"
        }
        self.session = None

    async def __aenter__(self: KitsuAsyncT) -> KitsuAsyncT:
        return self

    async def __aexit__(self, *excinfo: Any) -> None:
        await self.close()

    async def close(self):
        if self.session is not None:
            await self.session.close()

    async def __get_session__(self) -> ClientSession:
        if self.session is None:
            self.session = ClientSession(headers=self.headers)
        return self.session

    async def __fetch__(self, url: str) -> Dict[str, Any]:
        session = await self.__get_session__()
        response = await session.get(url)
        data = await response.json()
        if response.status != 200:
            raise KitsuException(data)
        return data

    async def __get_filters__(self, media: Media, filters: Dict[Filter, List[Union[Enum, int]]]) -> str:
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
    
    async def anime(self, id: int) -> AnimeModel:
        url = f"{self.url}/anime/{id}?include=genres,animeProductions.producer,characters"
        data = await self.__fetch__(url)
        return AnimeModel(data)

    async def manga(self, id: int) -> MangaModel:
        url = f"{self.url}/manga/{id}?include=genres,characters"
        data = await self.__fetch__(url)
        return MangaModel(data)

    async def character(self, media: Media, id: int) -> Union[AnimeCharacter, MangaCharacter]:        
        url = f"{self.url}/media-characters/{id}/character" if media == Media.MANGA \
            else f"{self.url}/media-characters/{id}/character?include=mediaCharacters.voices.person"

        data = await self.__fetch__(url)
        if media == Media.ANIME: return AnimeCharacter(data)
        if media == Media.MANGA: return MangaCharacter(data)

    async def franchises(self, media: Media, id: int) -> Tuple[Franchise]:
        url = f"{self.url}/media-relationships?filter[source_id]={id}&filter[source_type]={media.value.title()}&include=destination&sort=role"
        data = await self.__fetch__(url)
        return tuple(Franchise(root, _data) for root, _data in zip(data["data"], data["included"]))

    async def popularity(
        self, media: Media,
        page: Optional[int] = 1,
        filters: Optional[Dict[Filter, List[Union[Enum, int]]]] = {},
        limit: Optional[int] = 10
    ) -> SearchContainer:
        url = ""
        offset = limit * (page - 1)
        _filters = await self.__get_filters__(media, filters)
        if _filters:
            url = f"{self.url}/{media.value}?{_filters}page[limit]={limit}&page[offset]={offset}&sort=-user_count"
        else:
            url = f"{self.url}/{media.value}?page[limit]={limit}&page[offset]={offset}&sort=-user_count"
        data = await self.__fetch__(url)
        temp = [GeneralResult(d) for d in data["data"]]
        return SearchContainer(data, temp, page, limit)
    
    async def top_rate(
        self, media: Media,
        page: Optional[int] = 1,
        filters: Optional[Dict[Filter, List[Union[Enum, int]]]] = {},
        limit: Optional[int] = 10
    ) -> SearchContainer:
        offset = limit * (page - 1)
        _filters = await self.__get_filters__(media, filters)
        if _filters:
            url = f"{self.url}/{media.value}?{_filters}page[limit]={limit}&page[offset]={offset}&sort=-averageRating"
        else:
            url = f"{self.url}/{media.value}?page[limit]={limit}&page[offset]={offset}&sort=-averageRating"
        data = await self.__fetch__(url)
        temp = [GeneralResult(d) for d in data["data"]]
        return SearchContainer(data, temp, page, limit)

    async def upcoming(
        self, media: Media,
        page: Optional[int] = 1,
        filters: Optional[Dict[Filter, List[Union[Enum, int]]]] = {},
        limit: Optional[int] = 10
    ) -> SearchContainer:
        offset = limit * (page - 1)
        _filters = await self.__get_filters__(media, filters)
        if _filters:
            url = f"{self.url}/{media.value}?{_filters}page[limit]={limit}&page[offset]={offset}&sort=-startDate"
        else:
            url = f"{self.url}/{media.value}?page[limit]={limit}&page[offset]={offset}&sort=-startDate"
        data = await self.__fetch__(url)
        temp = [GeneralResult(d) for d in data["data"]]
        return SearchContainer(data, temp, page, limit)

    async def latest(
        self, media: Media,
        page: Optional[int] = 1,
        filters: Optional[Dict[Filter, List[Union[Enum, int]]]] = {},
        limit: Optional[int] = 10
    ) -> SearchContainer:
        offset = limit * (page - 1)
        _filters = await self.__get_filters__(media, filters)
        if _filters:
            url = f"{self.url}/{media.value}?{_filters}page[limit]={limit}&page[offset]={offset}&sort=-created_at"
        else:
            url = f"{self.url}/{media.value}?page[limit]={limit}&page[offset]={offset}&sort=-created_at"
        data = await self.__fetch__(url)
        temp = [GeneralResult(d) for d in data["data"]]
        return SearchContainer(data, temp, page, limit)

    async def search(self, media: Media, query: str, page: Optional[int] = 1, limit: Optional[int] = 10) -> SearchContainer:
        offset = limit * (page - 1)
        url = f"{self.url}/{media.value}?filter[text]={query}&page[limit]={limit}&page[offset]={offset}"
        data = await self.__fetch__(url)
        temp = [GeneralResult(d) for d in data["data"]]
        return SearchContainer(data, temp, page, limit)
