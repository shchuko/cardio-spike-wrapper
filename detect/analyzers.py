from detect.result import BaseResult


class BaseAnalyzer:
    async def analyze(self, csv_content: str) -> BaseResult:
        pass
