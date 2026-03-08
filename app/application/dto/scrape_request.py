from pydantic import BaseModel
from typing import List, Optional


class ExtractLinksConfig(BaseModel):

    selector: str
    attribute: str


class PaginationConfig(BaseModel):

    pattern: str
    start: int
    max_pages: int


class NavigationStep(BaseModel):

    name: str
    extract_links: ExtractLinksConfig


class ScrapeRequest(BaseModel):

    entry_points: List[str]

    navigation_flow: Optional[List[NavigationStep]] = None

    pagination: Optional[PaginationConfig] = None

    extract_links: ExtractLinksConfig