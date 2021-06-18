from pydantic import BaseModel


class StatsWrapper(BaseModel):
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


class BaseResult:
    def get_csv_path(self) -> str:
        pass

    def get_stats(self) -> list:
        pass

    def get_png(self) -> bytes:
        pass
