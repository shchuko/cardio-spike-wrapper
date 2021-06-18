from detect.result import BaseResult
from enum import Enum


class BaseAnalyzer:
    class AnalyzeStatus(Enum):
        PROCESSING = 1
        READY = 2
        NOT_FOUND = 3

    def queue_analyze(self, csv: str) -> str:
        pass

    def is_ready(self, result_id: str) -> AnalyzeStatus:
        pass

    def get_result(self, result_id: str) -> BaseResult:
        pass
