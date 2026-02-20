from dataclasses import dataclass

@dataclass
class Job:
    title: str
    url: str
    company: str | None = None
    location: str | None = None