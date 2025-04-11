from pydantic import BaseModel
from datetime import datetime

class NewsItem(BaseModel):
    headline: str
    link: str
    source: str
    scraped_at: datetime

class NewsCreate(BaseModel):
    headline: str
    link: str
    source: str