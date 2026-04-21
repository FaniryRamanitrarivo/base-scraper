from typing import Any, Optional, Union

class PaginationEngine:

    @staticmethod
    def build_url(base_url: str, config: Any, current_page: int = 1) -> str:
        """
        Constructs the URL by cleaning the base and injecting the page number.
        """
        pagination_param = config.pattern.replace("<PNum>", "")
        # Ensure we don't have trailing slashes or existing query strings interfering
        clean_base = base_url.split(pagination_param)[0].rstrip('/')
        
        # Replace the placeholder in the pattern (e.g., "/page/<PNum>")
        page_segment = config.pattern.replace("<PNum>", str(current_page))
        
        # Ensure the segment starts with a slash if it's a path, 
        # or handle query parameters if the pattern starts with '?'
        if not page_segment.startswith('/') and not page_segment.startswith('?'):
            page_segment = f"/{page_segment}"
            
        return f"{clean_base}{page_segment}"
    
    @staticmethod
    async def paginate(context: Any, base_url: Optional[str] = None) -> Union[str, bool, None]:
        config = getattr(context.payload, 'pagination', None) 

        browser = context.browser
        
        # 1. Increment Logic (URL-based)
        if config.type == "increment":
            config.start += 1  # Note: Modifying state here; ensure config persists
            next_url = PaginationEngine.build_url(base_url, config, config.start)
            await browser.get(next_url)
            return next_url

        # 2. Next Button Logic (Interaction-based)
        elif config.type == "next_button":
            try:
                next_button = await browser.find_element("xpath", config.button_xpath)
                # Check if button is actually interactable before clicking
                if next_button:
                    await next_button.click()
                    return True
                return False
            except Exception:
                return False

        # 3. Infinite Scroll Logic (JS-based)
        elif config.type == "infinite_scroll":
            try:
                # Scroll to bottom
                await browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Optional: You might want a small sleep here or a check for new content
                return True
            except Exception:
                return False

        return None