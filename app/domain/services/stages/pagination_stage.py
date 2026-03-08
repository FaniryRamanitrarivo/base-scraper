from app.domain.services.pipeline.stage import ScraperStage
from app.domain.services.engine.pagination_engine import PaginationEngine

class PaginationStage(ScraperStage):

    async def run(self, context):
        payload = context.payload
        logger = context.logger

        # 1. Initialisation systématique des variables locales
        # Cela évite l'UnboundLocalError si le code plante au milieu
        pages = []
        
        # On s'assure que context.page_urls existe dès le début, par défaut vide
        context.page_urls = []

        await logger.info("[PaginationStage] starting paginating")

        # 2. Vérification des données d'entrée
        # Si category_urls n'a pas été rempli par l'étape précédente, on s'arrête proprement
        category_urls = getattr(context, 'category_urls', [])
        
        if not category_urls:
            await logger.warning("[PaginationStage] No category_urls found in context. Skipping.")
            return

        # 3. Cas sans pagination
        if not payload.pagination:
            await logger.warning("[PaginationStage] no pagination config found in payload.")
            context.page_urls = category_urls
            return

        # 4. Logique de génération des URLs
        try:
            for url in category_urls:
                await logger.info(f"[PaginationStage] paginating : {url}")

                # On génère les URLs via l'engine
                generated_urls = PaginationEngine.build_urls(
                    url,
                    payload.pagination
                )
                
                # On combine l'URL d'origine (page 1) avec les suivantes
                page_urls = [url] + generated_urls
                pages.extend(page_urls)
            
            # Mise à jour du contexte seulement après succès
            context.page_urls = list(set(pages))  # Utilisation de set() pour dédoublonner au cas où
            
        except Exception as e:
            await logger.error(f"[PaginationStage] Critical error during pagination building: {str(e)}")
            # En cas d'erreur critique, on retombe sur les URLs de base pour ne pas bloquer tout le scraper
            context.page_urls = category_urls

        # 5. Log final (maintenant sécurisé car 'pages' est initialisé à [])
        await logger.info(f"[PaginationStage] {len(context.page_urls)} pagination urls found and set in context")