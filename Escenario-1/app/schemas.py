from pydantic import BaseModel

class RemediateRequest(BaseModel):
    team_id: str
    cve_id: str

class SummaryResponse(BaseModel):
    summary: dict