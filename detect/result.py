from pydantic import BaseModel


class Stats(BaseModel):
    time: int
    part: float
    tension_index: float
    mode: float
    std: float
    mean: float
    var: float
    pNN_50: float
    RMSSD: float
    ivr: float
    vpr: float
    papr: float
    idm: float
    cat: float


class StatsList(BaseModel):
    stats_items: list

    @staticmethod
    def from_python_list(items: list):
        dict_list = [item.dict() for item in items]
        return StatsList(stats_items=dict_list)

    def append(self, item: Stats):
        self.stats_items.append(item.dict())


class BaseResult:
    def get_csv_content(self) -> str:
        pass

    def get_stats(self) -> StatsList:
        pass

    def get_png_content(self) -> bytes:
        pass
