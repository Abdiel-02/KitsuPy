# KitsuPy

KitsuPy es un contenedor de Python para [Kitsu](https://github.com/hummingbird-me/api-docs) que proporciona enlaces para algunas funciones del API. Para mas información sobre el API de Kitsu consulte [Kitsu API](https://kitsu.docs.apiary.io/#introduction/json-api/request-headers).

Puede usar Kitsu o KitsuAsync dependiendo de si desea una clase contenedora sincrónica o una clase contenedora asincrónica, respectivamente.

# Uso

A continuación se muestran algunos ejemplos e información sobre cómo usar Kitsu y KitsuAsync.

## Obtener información de un Anime o un Manga por su id
```python
from kitsupy import Kitsu, KitsuException
from kitsu.enums import Media

client = Kitsu()

try:
    tokyo_ghoul = client.anime(8271)
    nanatsu_no_taizai = client.manga(24208)
except KitsuException as ex:
    print(ex.message)
```

La función **`anime`** como **`manga`** solo recive un unico parametro **id** y retorna un objeto de tipo **`AnimeModel`** o **`MangaModel`** el cual pose propiedades como la sinopsis, títulos, etc... Para mas información consulte la sección **Referencia de modelos**.

## Obtener los personajes de un Anime o Manga

```python
from kitsupy import Kitsu, KitsuException
from kitsu.enums import Media

client = Kitsu()

try:
    tokyo_ghoul = client.anime(8271)
    for character_id in tokyo_ghoul.main_characters:
        character = client.character(Media.ANIME, character_id)
        print(character.name)
except KitsuException as ex:
    print(ex.message)
```
La función **`character`** recive un unico parametro que es el **id** del personaje que lo puede obtener de la propiedad **main_characters** o **supporting_characters** del objeto **AnimeModel** o **MangaModel**. El valor devuelto sera un objeto de tipo **`AnimeCharacter`** o **`MangaCharacter`**. Para mas información consulte la sección **Referencia de modelos**.

## Obtener las franquisias de un Anime o Manga
```python
from kitsupy import Kitsu, KitsuException
from kitsu.enums import Media

client = Kitsu()

try:
    franchises = client.franchises(Media.ANIME, 8271)
except KitsuException as ex:
    print(ex.message)
```
La función **`franchises`** recive solo 2 parametros **media** [`Media.ANIME` o `Media.MANGA`] e **id** del anime o manga y retornara una tupla con objetos de tipo **`Franchise`**. Para mas información consulte la sección **Referencia de modelos**.

## Buscar un anime o manga
```python
from kitsupy import Kitsu, KitsuException
from kitsu.enums import Media

client = Kitsu()

try:
    search = client.search(Media.ANIME, 'code geass', page=1)
except KitsuException as ex:
    print(ex.message)
```
La función **`search`** recive los siguientes parámetros:
- `media`: **Media** [`Media.ANIME` o `Media.MANGA`].
- `query`: **str** (cadena con el titulo del anime o manga).
- `page`: **int** (Opcional, default 1).
- `limit`: **int** (Opcional, default 10).

La misma devolverá un objeto de tipo **`SearchContainer`** con la información solicitada y las siguientes propiedades: `page`, `results`, `total_page` y `total_result`. Para mas información consulte la sección **Referencia de modelos**.

## Obtener una lista de animes o mangas con o sin filtrado
```python
from kitsupy import Kitsu, KitsuException
from kitsu.enums import Media

client = Kitsu()

try:
    # Todos devuelven un objeto SearchContainer
    popularity = client.popularity(Media.ANIME , page=1)
    top_rate = cliente.top_rate(Media.MANGA, page=2)
    upcoming = client.upcoming(Media.ANIME, page=3)
    latest = cliente.latest(Media.MANGA, page=4)
except KitsuException as ex:
    print(ex.message)
```
Puede especificar alguno de los siguientes filtros:
| Filter         | Anime  | Manga  |
|      :----:    | :----: | :----: |
| AGE_RATING     |  ✔️   |   ❌   |
| AVERAGE_RATING |  ✔️   |   ✔️   |
| GENRES         |  ✔️   |   ✔️   |
| SEASON         |  ✔️   |   ❌   |
| YEAR           |  ✔️   |   ✔️   |
| SUBTYPE        |  ✔️   |   ✔️   |

```python
from kitsu.enums import *

filters_anime = {
    Filter.GENRES: [Genres.ACTION, Genres.SCHOOL],
    Filter.SEASON: [Season.SPRING],
    Filter.YEAR: [2018, 2020]
}

filters_manga {
    Filter.AVERAGE_RATING: [75, 100],
    Filter.SUBTYPE: [MangaSubtype.NOVEL]
    Filter.GENRES: [Genres.ROMANCE, Genres.HAREM]
}

```
La función **`popularity`**, **`top_rate`**, **`upcoming`** y **`latest`** reciven los siguientes parametros:
- `media`: **Media** [`Media.ANIME` o `Media.MANGA`].
- `page`: **int** (Opcional, default = 1).
- `filters`: **Dict[Filter, List[Union[Enum, int]]]** (Opcional, default = None).
- `limit`: **int** (Opcional, default = 10).

El modulo **filters** contiene la clase **`Filter`** y sus posibles valores en las siguientes clases **`AgeRating`**, **`Season`**, **`AnimeSubtype`** y **`MangaSubtype`**.

## Convertir el model en un objeto **json**
```python
from kitsupy import Kitsu, KitsuException

client = Kitsu()

try:
    anime = client.anime(42196)
    json = anime.to_json()
    print(json)
except KitsuException as ex:
    print(ex.message)
```
Con la función **`to_json`** puede convertir el modelo en un objeto json, opcional puede especificar el tamaño de la **indentación**, por defecto el mismo es **2**. Todos los modelos cuenta con esta función.

## Ejemplos de uso con KitsuAsync

### utilizando context manager (**with**)
```python
import asyncio
from kitsupy import KitsuAsync, KitsuException
from kitsu.enums import Media

async def main():
    try:
        async with KitsuAsync() as client:
            tokyo_ghoul = await client.anime(8271)
    except KitsuException as ex:
        print(ex.message) 

if __name__ == "__main__":
    asyncio.run(main())
```

### realizando una instancia
En este caso recuerde utilizar la función **`close`**.
```python
import asyncio
from kitsupy import KitsuAsync, KitsuException
from kitsu.enums import Media

async def main():
    client = KitsuAsync()
    try:
        nanatsu_no_taizai = await client.manga(24208)
    except KitsuException as ex:
        print(ex.message)
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Todas los ejemplos mostrados mas arriba son validos al utilizar **KitsuAsync**. Se recomienda utilizar el bloque **try** para capturar posibles excepciones que se pueden dar al realizar la petición o si el servidor retorna una respuesta con algún error, para ello puede apoyarce en con la clase **`KitsuException`**.

# Referencia de modelos

## `Anime` / `Manga`
| Propiedad |   Tipo  | `AnimeModel` | `MangaModel` |
|   :----:  |  :----: |    :----:    |    :----:    |
|   *id*  | *int* |  ✔️   |   ✔️   |
|  *type* | *str* | ✔️   |   ✔️   |
| *created_at* | *datetime* | ✔️   |   ✔️   |
| *updated_at* | *datetime* | ✔️   |   ✔️   |
| *slug* | *str* | ✔️   |   ✔️   |
| *synopsis* | *str* | ✔️   |   ✔️   |
| *description* | *str* | ✔️   |   ✔️   |
| *cover_image_top_off_set* | *int* | ✔️   |   ✔️   |
| *titles* | *Dict[str, str]* | ✔️   |   ✔️   |
| *canonical_title* | *str* | ✔️   |   ✔️   |
| *abbreviated_titles* | *List[str]* | ✔️   |   ✔️   |
| *average_rating* | *float* | ✔️   |   ✔️   |
| *rating_frequencies* | *Dict[str, str]* | ✔️   |   ✔️   |
| *user_count* | *int* | ✔️   |   ✔️   |
| *favorites_count* | *int* | ✔️   |   ✔️   |
| *start_date* | *datetime* | ✔️   |   ✔️   |
| *end_date* | *datetime* | ✔️   |   ✔️   |
| *next_release* | * | ✔️   |   ✔️   |
| *popularity_rank* | *int* | ✔️   |   ✔️   |
| *rating_rank* | *int* | ✔️   |   ✔️   |
| *age_rating* | *str* | ✔️   |   ✔️   |
| *subtype* | *str* | ✔️   |   ✔️   |
| *status* | *str* | ✔️   |   ✔️   |
| *tba* | *str* | ✔️   |   ✔️   |
| *poster_images* | *Dict[str, str*] | ✔️   |   ✔️   |
| *cover_images* | *Dict[str, str*] | ✔️   |   ✔️   |
| *genres* | *List[str]* | ✔️   |   ✔️   |
| *main_characters* | *List[int]* | ✔️   |   ✔️   |
| *supporting_characters* | *List[int]* | ✔️   |   ✔️   |
| *episode_count* | *int* | ✔️   |   ❌   |
| *episode_length* | *int* | ✔️   |   ❌   |
| *youtube_video_id* | *str* | ✔️   |   ❌   |
| *producers* | *List[str]* | ✔️   |   ❌   |
| *licensors* | *List[str]* | ✔️   |   ❌   |
| *studies* | *List[str]* | ✔️   |   ❌   |
| *chapter_count* | *int* | ❌   |   ✔️   |
| *volume_count* | *int* | ❌   |   ✔️   |
| *serialization* | *str* | ❌   |   ✔️   |

## <br> **`Characters`**
| Propiedad |   Tipo  | `AnimeCharacter` | `MangaCharacter` |
|   :----:  |  :----: |     :----:       |      :----:      |
|   *id*  | *int* | ✔️   |   ✔️   |
| *slug* | *str* | ✔️   |   ✔️   |
| *names* | *List[str]* | ✔️   |   ✔️   |
| *canonical_title* | *str* | ✔️   |   ✔️   |
| *other_names* | *List[str]* | ✔️   |   ✔️   |
| *name* | *str* | ✔️   |   ✔️   |
|   *mal_id*  | *int* | ✔️   |   ✔️   |
| *description* | *str* | ✔️   |   ✔️   |
| *image* | *str* | ✔️   |   ✔️   |
| *voice_actor* | *Dict[str, Dict[str, str]]* |  ✔️   |   ❌   |

## <br> **`Franchise`**
| Propiedad |   Tipo  |
|   :----:  |  :----: |
|   *id*  | *int* |
|  *type* | *str* |
| *titles* | *Dict[str, str]* |
| *canonical_title* | *str* |
| *average_rating* | *float* |
| *popularity_rank* | *int* |
| *rating_rank* | *int* |
| *subtype* | *str* |
| *status* | *str* |
| *poster_images* | *Dict[str, str]* |
| *cover_images* | *Dict[str, str]* |

## <br> **`SearchContainer`**
| Propiedad |   Tipo  |
|   :----:  |  :----: |
|   *page*  | *int* |
|  *results* | *List[GeneralResult]* |
| *total_page* | *int* |
| *total_result* | *int* |

## <br> **`GeneralResult`**
| Propiedad |   Tipo  |
|   :----:  |  :----: |
|   *id*  | *int* |
|  *type* | *str* |
| *titles* | *Dict[str, str]* |
| *canonical_title* | *str* |
| *average_rating* | *float* |
| *popularity_rank* | *int* |
| *rating_rank* | *int* |
| *subtype* | *str* |
| *status* | *str* |
| *poster_images* | *Dict[str, str]* |
| *cover_images* | *Dict[str, str]* |
