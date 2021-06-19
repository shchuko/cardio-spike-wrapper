from detect.result import BaseResult
from enum import Enum


class BaseAnalyzer:
    class AnalyzeStatus(Enum):
        PROCESSING = 1
        READY = 2
        NOT_FOUND = 3

    async def analyze(self, csv_content: str) -> BaseResult:
        pass
