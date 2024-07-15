
from pydantic import BaseModel

class OrgID(BaseModel):
    组织ID: str

class QueryClassesByOrgId(OrgID):
    班次ID: str = None

class QueryTeamsByOrgId(OrgID):
    班组ID: str = None
