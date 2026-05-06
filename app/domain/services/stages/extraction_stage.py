import asyncio
from typing import Any, Set, List

# Imports de ton architecture
from app.domain.services.pipeline.stage import ScraperStage
from app.domain.services.engine.extraction_engine import ExtractionEngine
# On importe le moteur ET l'Enum pour la comparaison à la fin
from app.domain.services.engine.pagination_engine import PaginationEngine, PaginationType

class ExtractionStage(ScraperStage):

    async def run(self, context: Any) -> None:
        payload = context.payload
        logger = context.logger
        pagination_cfg = getattr(payload, 'pagination', None) 
        
        # Sécurisation des valeurs par défaut
        max_pages = getattr(pagination_cfg, 'max_pages', 1) if pagination_cfg else 1
        wait_delay = getattr(pagination_cfg, 'delay_seconds', 3.0) if pagination_cfg else 3.0

        await logger.info(f"[ExtractionStage] Démarrage. Limite: {max_pages} pages/catégorie.")
        
        results: Set[Any] = set()
        category_urls: List[str] = list(getattr(context, 'category_urls', []))
        
        for start_url in category_urls:
            try:
                await self._process_category(
                    context, start_url, max_pages, wait_delay, results
                )
            except Exception as e:
                await logger.error(f"Erreur critique sur la catégorie {start_url}: {str(e)}")

        context.results = list(results)
        await logger.info(f"[ExtractionStage] Terminé. {len(context.results)} produits uniques trouvés.")

    async def _process_category(
        self, 
        context: Any, 
        start_url: str, 
        max_pages: int, 
        wait_delay: float, 
        global_results: Set[Any]
    ) -> None:
        """
        Traite une catégorie spécifique et gère sa pagination.
        """
        logger = context.logger
        browser = context.browser
        payload = context.payload
        current_url = start_url
        
        await logger.info(f"Ouverture de la catégorie : {current_url}")
        await browser.open(current_url)

        for page_index in range(max_pages):
            await logger.info(f"Extraction Page {page_index + 1}/{max_pages} [URL: {current_url}]")

            # 1. Extraction
            products = await ExtractionEngine.extract(
                browser,
                payload.product_links,
                base_url=current_url
            )

            if not products:
                await logger.warning(f"Aucun lien trouvé sur la page {page_index + 1}.")
                break
            
            await logger.success(f"{len(products)} produits trouvés.", products)
            global_results.update(products)

            if page_index >= max_pages - 1:
                break

            # 2. Appel au PaginationEngine
            # Note: On passe page_index + 1 car l'index commence à 0
            pagination_result = await PaginationEngine.paginate(context, current_url, page_index + 1)
            
            if not pagination_result or not pagination_result.success:
                await logger.info("Plus aucune page suivante trouvée.")
                break

            # 3. Actions basées sur le type de pagination
            if pagination_result.type == PaginationType.NAVIGATION:
                next_url = pagination_result.next_url
                await logger.info(f"Navigation vers: {next_url}")
                await browser.open(next_url)
                current_url = next_url 

            elif pagination_result.type == PaginationType.IN_PLACE:
                await logger.info(f"Pagination locale effectuée. Attente de {wait_delay}s...")
                await asyncio.sleep(wait_delay)