from enum import Enum, unique

@unique
class Genres(Enum):
    ACTION = 1
    ADVENTURE = 2
    COMEDY = 3
    DRAMA = 4
    SCI_FI = 5
    SPACE = 6
    MISTERY = 7
    MAGIC = 8
    SUPERNATURAL = 9
    POLICE = 10
    FANTASY = 11
    SPORTS = 13
    ROMANCE = 14
    SLICE_OF_LIFE = 16
    RACING = 17
    HORROR = 19
    PSYCHOLOGICAL = 20
    THRILLER = 21
    MARTIAL_ARTS = 22
    SUPER_POWER = 23
    SCHOOL = 24
    ECCHI = 25
    VAMPIRE = 26
    HISTORICAL = 27
    MILITARY = 28
    DEMENTIA = 29
    MECHA = 30
    DEMONS = 31
    SAMURAI = 32
    HAREM = 34
    MUSICA = 35
    PARODY = 36
    SHOUJO_AI = 37
    GAME = 38
    SHOUNEN_AI = 39
    KIDS = 40
    HENTAI = 41
    YURI = 42
    YAOI = 43
    GORE = 49
    ISEKAI = 65

    def __repr__(self):
        return self.name.replace("_", " ").lower().title()