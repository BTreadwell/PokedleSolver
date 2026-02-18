from enum import Enum

class Response(Enum):
    NOMATCH = 0
    MATCH = 1
    QUERY_LT = 2
    QUERY_GT = 3
    TYPE_WRONG_POS = 4

class Attribute(Enum):
    ID = 0
    GEN = 1
    T1 = 2
    T2 = 3
    STAGE = 4
    EVO = 5
    COLOR = 6

class Pokemon:
    def __init__(self, id: int, gen: int, type1: int, type2: int, evoStage: int, isFinalEvo: bool, color: int):
        self.id = id
        self.gen = gen
        self.type1 = type1
        self.type2 = type2
        self.evoStage = evoStage
        self.isFinalEvo = isFinalEvo
        self.color = color

    def compare(self, other: 'Pokemon') -> 'QueryResult':
        return QueryResult([
            Response.MATCH if self.id == other.id else Response.NOMATCH,
            Response.MATCH if self.gen == other.gen else Response.QUERY_LT if self.gen > other.gen else Response.QUERY_GT,
            Response.MATCH if self.type1 == other.type1 else Response.TYPE_WRONG_POS if self.type1 == other.type2 else Response.NOMATCH,
            Response.MATCH if self.type2 == other.type2 else Response.TYPE_WRONG_POS if self.type2 == other.type1 else Response.NOMATCH,
            Response.MATCH if self.evoStage == other.evoStage else Response.NOMATCH,
            Response.MATCH if self.isFinalEvo == other.isFinalEvo else Response.NOMATCH,
            Response.MATCH if self.color == other.color else Response.NOMATCH,
        ])

    def is_compatible(self, other: 'Pokemon', result: 'QueryResult') -> bool:
        return self.compare(other) == result


class QueryResult:
    def __init__(self, result: list[Response]):
        self.result = result

    def __getitem__(self, key: Attribute | int) -> Response:
        if isinstance(key, int):
            return self.result[key]
        elif isinstance(key, Attribute):
            return self.result[key.value]
        else:
            raise TypeError

    def __eq__(self, other):
        for i in range(len(self.result)):
            if self.result[i] != other.result[i]:
                return False
        return True

