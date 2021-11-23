from datetime import datetime

from pydantic import BaseModel


class Posting(BaseModel):
    user_id: int
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
