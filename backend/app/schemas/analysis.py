from pydantic import BaseModel


class AnalysisRequest(BaseModel):
    code: str