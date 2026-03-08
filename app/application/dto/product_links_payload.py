from typing import List, Optional, Literal, Union
from uuid import UUID
from pydantic import BaseModel, Field, AnyUrl, field_validator
from typing import Annotated

# ============================================================
# 1️⃣ ENGINE CONFIG
# ============================================================

class EngineConfig(BaseModel):
    browser: Literal["playwright", "selenium-chrome", "selenium-firefox"]
    headless: bool = True
    timeout: Optional[int] = Field(default=30000, ge=1000)
    wait_until: Optional[Literal["load", "domcontentloaded", "networkidle"]] = "domcontentloaded"


# ============================================================
# 2️⃣ FIELD DEFINITION SYSTEM (Selector | JS)
# ============================================================

class BaseExtractor(BaseModel):
    type: Literal["selector", "js"]
    multiple: bool = False
    wait: Optional[bool] = False
    regex: Optional[str] = None


class SelectorExtractor(BaseExtractor):
    type: Literal["selector"]
    selector: str
    attribute: Optional[str] = "href"
    js: Optional[str] = None


class JSExtractor(BaseExtractor):
    type: Literal["js"]
    js: str
    selector: Optional[str] = None
    attribute: Optional[str] = None


Extractor = Annotated[
    Union[SelectorExtractor, JSExtractor],
    Field(discriminator="type")
]


# ============================================================
# 3️⃣ NAVIGATION FLOW
# ============================================================

class NavigationStep(BaseModel):
    name: str
    extract_links: Extractor
    extract_label: Optional[Extractor] = None


# ============================================================
# 4️⃣ PRODUCT LINKS
# ============================================================

class ProductLinksConfig(BaseModel):
    type: Literal["selector", "js"]
    selector: Optional[str] = None
    attribute: Optional[str] = "href"
    js: Optional[str] = None
    multiple: bool = True
    deduplicate: bool = True
    absolute: bool = True


# ============================================================
# 5️⃣ PAGINATION (Polymorphic)
# ============================================================

class IncrementPagination(BaseModel):
    type: Literal["increment"]
    pattern: str
    start: int = 1
    max_pages: int = 1


class NextButtonPagination(BaseModel):
    type: Literal["next_button"]
    selector: str
    max_pages: int = 1


class InfiniteScrollPagination(BaseModel):
    type: Literal["infinite_scroll"]
    scroll_delay: int = 1000
    max_scrolls: int = 5


PaginationConfig = Annotated[
    Union[
        IncrementPagination,
        NextButtonPagination,
        InfiniteScrollPagination,
    ],
    Field(discriminator="type")
]


# ============================================================
# 6️⃣ NETWORK INTERCEPTION (OPTIONAL FUTURE SUPPORT)
# ============================================================

class NetworkInterceptionConfig(BaseModel):
    enabled: bool = False
    url_pattern: Optional[str] = None
    method: Optional[Literal["GET", "POST"]] = None


# ============================================================
# 7️⃣ NORMALIZATION
# ============================================================

class NormalizationConfig(BaseModel):
    strip_query_params: Optional[bool] = False
    force_https: Optional[bool] = False
    remove_trailing_slash: Optional[bool] = True


# ============================================================
# 8️⃣ RUN IDENTIFICATION
# ============================================================

class RunMetadata(BaseModel):
    run_id: UUID
    site_id: int
    config_version_id: int
    trigger_type: Literal["manual", "cron", "api"]


# ============================================================
# ROOT PAYLOAD
# ============================================================

class ProductLinksScraperPayload(BaseModel):
    engine: EngineConfig
    entry_points: List[AnyUrl] = Field(..., min_length=1)
    navigation_flow: Optional[List[NavigationStep]] = []
    product_links: ProductLinksConfig
    pagination: Optional[PaginationConfig] = None
    network_interception: Optional[NetworkInterceptionConfig] = None
    normalization: Optional[NormalizationConfig] = None
    run: Optional[RunMetadata] = None

    @field_validator("entry_points", mode="after")
    @classmethod
    def normalize_urls(cls, urls):
        return [str(url) for url in urls]