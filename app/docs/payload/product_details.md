# 📘 Product Details Scraper – Payload Specification

## 1️⃣ Engine

```json
{
  "engine": {
    "browser": "playwright",
    "headless": true,
    "timeout": 30000,
    "wait_until": "networkidle",
  }
}
```

## 2️⃣ launch_js_function (IMPORTANT)

Ce bloc est exécuté immédiatement après le chargement de la page.

Objectif :
- Déclencher API interne
- Lire variables JS globales
- Interroger GraphQL
- Construire un objet exploitable
- Attendre que les données soient prêtes

### Structure

```json
{
  "launch_js_function": {
    "enabled": true,
    "wait_for": "window.__SCRAPER_READY__ === true",
    "timeout": 10000,
    "script": "async function() { ... }"
  }
}
```

### Exemple concret – fetch API interne


```json
{
  "launch_js_function": {
    "enabled": true,
    "wait_for": "window.__PRODUCT_DATA__ !== undefined",
    "script": "async function() { \
      const res = await fetch('/api/product/123'); \
      const data = await res.json(); \
      window.__PRODUCT_DATA__ = data; \
      window.__SCRAPER_READY__ = true; \
    }"
  }
}
```
Le moteur :
- injecte la fonction
- l’exécute via page.evaluate
- attend wait_for
- continue extraction

## 3️⃣ Fields (classiques)

```json
{
  "fields": {
    "title": {
      "type": "selector",
      "selector": "h1",
      "attribute": "textContent",
      "regex": null,
    },
    "brand": {
      "type": "js",
      "js": "return window.__PRODUCT_DATA__.brand"
    }
  }
}
```

## 4️⃣ Variants (Très important)

Ici on introduit un concept propre :

👉 `variants` retourne un tableau structuré.

### Structure recommandée

```json
{
  "variants": {
    "type": "js",
    "multiple": true,
    "js": "return window.__PRODUCT_DATA__.variants.map(v => ({ \
        size: v.size, \
        price: v.price, \
        is_available: v.available, \
        sku: v.sku \
    }))"
  }
}
```
Résultat attendu :
```json
[
  {
    "size": "S",
    "price": 29,
    "is_available": true,
    "sku": "ABC-S"
  },
  {
    "size": "M",
    "price": 29,
    "is_available": false,
    "sku": "ABC-M"
  }
]
```

### 🔥 Variante DOM-based (si pas d’API)

```json
{
  "variants": {
    "type": "js",
    "multiple": true,
    "js": "return Array.from(document.querySelectorAll('.variant-row')).map(row => ({ \
        size: row.querySelector('.size').innerText, \
        price: parseFloat(row.querySelector('.price').innerText), \
        is_available: row.querySelector('.stock').innerText \
    }))"
  }
}
```

## 5️⃣ Variante avancée – Structure déclarative


```json
{
  "variants": {
    "container_selector": ".variant-row",
    "fields": {
      "size": {
        "selector": ".size",
        "attribute": "textContent"
      },
      "price": {
        "selector": ".price",
        "attribute": "textContent",
        "transform": "parseFloat"
      },
      "stock": {
        "selector": ".stock",
        "attribute": "textContent"
      }
    }
  }
}
```

## 🧠 Cycle d’Exécution Final

Pour chaque URL :
1. Ouvrir page
2. Attendre wait_until
3. Exécuter launch_js_function
4. Attendre wait_for
5. Extraire fields
6. Extraire variants
7. Sauvegarder