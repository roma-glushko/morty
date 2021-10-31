from pydantic import BaseModel


class GitDetails(BaseModel):
    branch: str
    commit_hash: str
