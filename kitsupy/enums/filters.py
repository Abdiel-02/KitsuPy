from enum import unique, Enum

@unique
class Filter(Enum):
    AGE_RATING = "ageRating"
    AVERAGE_RATING = "averageRating"
    GENRES = "categories"
    SEASON = "season"
    YEAR = "year"
    SUBTYPE = "subtype"

@unique
class AgeRating(Enum):
    G = "G"
    PG = "PG"
    R = "R"
    R18 = "R18"

class Season(Enum):
    SPRING = "spring"
    SUMER = "summer"
    FALL = "fall"
    WINTER = "winter"

class AnimeSubtype(Enum):
    ONA = "ona"
    OVA = "ova"
    TV = "tv"
    MOVIE = "movie"
    MUSIC = "music"
    SPECIAL = "special"
    
class MangaSubtype(Enum):
    DOUJIN = "doujin"
    MANGA = "manga"
    MANHUA = "manhua"
    MANHWA = "manhwa"
    NOVEL = "novel"
    OEL = "oel"
    ONESHOT = "oneshot"
