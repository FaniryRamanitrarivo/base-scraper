# Product Links Scraper – Instance Payload
## Overview

Ce payload définit la configuration utilisée pour scraper uniquement les **liens produits/offres**.

Chaque exécution génère :
- un `run_id`
- une `scraper_instance`
- des `entrées dans scraped_links`

## 1️⃣ Structure Globale
```json
{
  "engine": {},
  "entry_points": [],
  "navigation_flow": [],
  "product_links": {},
  "pagination": {},
  "network_interception": {},
  "normalization": {}
}
```

## 2️⃣ Engine Configuration
```json
{
  "engine": {
    "browser": "playwright",
    "headless": true,
    "timeout": 30000,
    "wait_until": "networkidle"
  }
}
```

## 3️⃣ Entry Points
```json
{
  "entry_points": [
    "https://example.com/jobs",
    "https://example.com/blogs",
    "https://example.com/posts",
  ]
}
```

## 4️⃣ Navigation Flow

Définit les niveaux de navigation dynamiques.
```json
{
  "navigation_flow": [
    {
      "name": "category",
      "extract_links": {},
      "extract_label": {}
    },
    {
      "name": "sub_category",
      "extract_links": {},
      "extract_label": {}
    }
  ]
}
```

Chaque niveau peut :
- Extraire des URLs
- Extraire un label (ex: nom catégorie)
- Être facultatif

## 5️⃣ Field Definition System

Tous les extracteurs utilisent le même format :
```json
{
  "type": "selector | js",
  "selector": ".category a",
  "attribute": "href",
  "regex": null,
  "multiple": true,
  "wait": true,
  "js": null
}
```
### Exemple JS
```json
{
  "type": "js",
  "js": "return window.__STATE__.categories.map(c => c.url)",
  "multiple": true
}
```

## 6️⃣ Product Links Extraction

Définit comment extraire les URLs finales.
```json
{
  "product_links": {
    "type": "selector",
    "selector": ".product-card a",
    "attribute": "href",
  }
}
```

## 7️⃣ Pagination

### Incrementale
```json
{
  "pagination": {
    "type": "increment",
    "pattern": "?page=<PNum>",
    "start": 1,
    "max_pages": 50
  }
}
```

### Next Button
```json
{
  "pagination": {
    "type": "next_button",
    "selector": ".next",
    "max_pages": 20
  }
}
```

### Infinite Scroll
```json
{
  "pagination": {
    "type": "infinite_scroll",
    "scroll_delay": 1000,
    "max_scrolls": 10
  }
}
```

## 8️⃣ Run Identification
```json
{
  "run_id": "uuid",
  "site_id": 12,
  "config_version_id": 4,
  "trigger_type": "manual | cron | api"
}
```

Toutes les URLs collectées seront liées à ce `run_id`.


##  Exemple Complet

```json
{
  "engine": {
    "browser": "selenium-chrome",
    "headless": true
  },
  "entry_points": [
    "https://www.portaljob-madagascar.com/"
  ],
  "navigation_flow": [
    {
      "name": "category",
      "extract_links": {
        "type": "selector",
        "selector": "header[role='banner'] a[href*='secteur/liste']",
        "attribute": "href",
        "multiple": true
      },
      "extract_label": {
        "type": "selector",
        "selector": "header[role='banner'] a:is([href*='secteur=7'], [href*='secteur=6'])",
        "attribute": "textContent",
        "multiple": true
      }
    },
    {
      "name": "sub_category",
      "extract_links": {
        "type": "selector",
        "selector": "main[role='main'] a[href*='informatique']",
        "attribute": "href",
        "multiple": true
      },
      "extract_label": {
        "type": "selector",
        "selector": "main[role='main'] a[href*='informatique']",
        "attribute": "textContent",
        "multiple": true
      }
    }
  ],
  "product_links": {
    "type": "selector",
    "selector": "article[role='listitem'] a[class*='items']",
    "attribute": "href",
    "multiple": true,
    "deduplicate": true,
    "absolute": true
  },
  "pagination": {
    "type": "increment",
    "pattern": "/page/<PNum>",
    "start": 1,
    "max_pages": 3
  }
}
```

### 🧠 Philosophie

Ce payload est :
- Responsable uniquement des URLs
- Indépendant du parsing des détails
- Compatible DOM + JS
- Versionnable
- Attaché à une instance (run_id)

### 🔥 Architecture Finale

1. Phase 1 :
Product Links Scraper → remplit `scraped_links`

2. Phase 2 :
Product Details Scraper → lit `scraped_links` et remplit `scraped_entities`