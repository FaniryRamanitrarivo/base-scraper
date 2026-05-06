import asyncio
from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional, List, Set

class PaginationType(str, Enum):
    NAVIGATION = "navigation" # L'URL change (ex: href, increment)
    IN_PLACE = "in_place"     # L'URL reste la même, le DOM mute (ex: click, scroll)

@dataclass
class PaginationResult:
    """Standardise la réponse du moteur de pagination."""
    success: bool
    type: Optional[PaginationType] = None
    next_url: Optional[str] = None


class PaginationEngine:
    """
    Gère les différentes méthodes de pagination de manière statique.
    Retourne toujours un PaginationResult pour un traitement unifié.
    """

    @staticmethod
    def build_url(base_url: str, config: Any, page_index: int) -> str:
        """
        Construit l'URL paginée en fonction de l'index de la page courante.
        """
        # Ex: si config.start = 1, la page 2 sera index 1 -> 1 + 1 = 2
        next_page_num = getattr(config, "start", 1) + page_index
        segment = config.pattern.replace("<PNum>", str(next_page_num))

        if not segment.startswith("/") and not segment.startswith("?"):
            segment = f"/{segment}"

        pattern_placeholder = config.pattern.replace("<PNum>", "")
        clean_base = base_url.split(pattern_placeholder)[0].rstrip("/")
        
        return f"{clean_base}{segment}"

    @staticmethod
    async def paginate(context: Any, current_url: str, page_index: int) -> PaginationResult:
        config = getattr(context.payload, "pagination", None)
        if not config:
            return PaginationResult(success=False)

        browser = context.browser
        pag_type = getattr(config, "type", None)

        match pag_type:
            case "increment":
                next_url = PaginationEngine.build_url(current_url, config, page_index)
                return PaginationResult(success=True, type=PaginationType.NAVIGATION, next_url=next_url)

            case "href_redirection":
                try:
                    next_url = await browser.get_attribute(config.selector, getattr(config, "attribute", "href"))
                    if next_url:
                        return PaginationResult(success=True, type=PaginationType.NAVIGATION, next_url=next_url)
                except Exception as e:
                    await context.logger.error(f"Href pagination failed: {e}")
                return PaginationResult(success=False)

            case "next_button":
                success = await browser.click(config.selector)
                if success:
                    return PaginationResult(success=True, type=PaginationType.IN_PLACE)
                return PaginationResult(success=False)

            case "infinite_scroll":
                try:
                    await browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    return PaginationResult(success=True, type=PaginationType.IN_PLACE)
                except Exception as e:
                    await context.logger.error(f"Scroll pagination failed: {e}")
                return PaginationResult(success=False)

            case _:
                await context.logger.warning(f"Unknown pagination type: {pag_type}")
                return PaginationResult(success=False)