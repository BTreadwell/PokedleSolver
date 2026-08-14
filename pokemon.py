from enum import Enum

class Response(Enum):
    NOMATCH = 0
    MATCH = 1
    QUERY_LT = 2
    QUERY_GT = 3
    TYPE_WRONG_POS = 4
    HIDDEN = 999

class Attribute(Enum):
    ID = 0
    GEN = 1
    T1 = 2
    T2 = 3
    STAGE = 4
    EVO = 5
    COLOR = 6

with open("Data/colors.csv", 'r') as f:
    colors = f.readline().strip().split(',')

with open('Data/types.csv', 'r') as f:
    types = f.readline().strip().split(',')

with open('Data/names.csv', 'r') as f:
    names = f.readline().strip().split(',')

class Pokemon:
    def __init__(self, id: int, gen: int, type1: int, type2: int, evoStage: int, isFinalEvo: bool, color: int, popularity: float = 1.0):
        self.id = id
        self.gen = gen
        self.type1 = type1
        self.type2 = type2
        self.evoStage = evoStage
        self.isFinalEvo = isFinalEvo
        self.color = color
        self.popularity = popularity

    def compare(self, other: 'Pokemon') -> 'QueryResult':
        return QueryResult((
            Response.MATCH if self.id == other.id else Response.NOMATCH,
            Response.MATCH if self.gen == other.gen else Response.QUERY_LT if self.gen > other.gen else Response.QUERY_GT,
            Response.MATCH if self.type1 == other.type1 else Response.TYPE_WRONG_POS if self.type1 == other.type2 else Response.NOMATCH,
            Response.MATCH if self.type2 == other.type2 else Response.TYPE_WRONG_POS if self.type2 == other.type1 else Response.NOMATCH,
            Response.MATCH if self.evoStage == other.evoStage else Response.NOMATCH,
            Response.MATCH if self.isFinalEvo == other.isFinalEvo else Response.NOMATCH,
            Response.MATCH if self.color == other.color else Response.NOMATCH,
        ))

    def compare_limited(self, other: 'Pokemon', fields: set[Attribute]) -> 'QueryResult':
        tmp_res = self.compare(other)
        for a in Attribute:
            if a not in fields:
                tmp_res[a] = Response.HIDDEN
        return tmp_res

    def is_compatible(self, other: 'Pokemon', result: 'QueryResult', fields: list[Attribute]) -> bool:
        alt =  self.compare(other)
        for field in fields:
            if alt[field] != result[field]:
                return False
        return True

    def __str__(self):
        return  f"{names[self.id]}, {self.gen}, {types[self.type1]}, {types[self.type2]}, {self.evoStage}, {True if self.isFinalEvo else False}, {colors[self.color]}"

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

class QueryResult:
    def __init__(self, result: tuple[Response, Response, Response, Response, Response, Response, Response]):
        self.result = result

    def __getitem__(self, key: Attribute | int) -> Response:
        if isinstance(key, int):
            return self.result[key]
        elif isinstance(key, Attribute):
            return self.result[key.value]
        else:
            raise TypeError

    def __setitem__(self, key: Attribute | int, value: Response):
        res = list(self.result)
        if isinstance(key, int):
            res[key] = value
        elif isinstance(key, Attribute):
            res[key.value] = value
        else:
            raise TypeError
        self.result = tuple(res)

    def __eq__(self, other):
        for i in range(len(self.result)):
            if self.result[i] != other.result[i]:
                return False
        return True

    def __hash__(self) -> int:
        return hash(self.result)
