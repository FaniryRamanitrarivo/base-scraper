## Job Scraper API

Une API pour scraper les offres d'emploi depuis différents sites web, avec intégration Selenium pour le scraping dynamique, et exposée via une API REST. Permet également l’export des données et la gestion des scrapers de manière centralisée.

# Table des matières

Fonctionnalités

Technologies

Prérequis

Installation

Configuration

Usage

Architecture

Contribuer

Licence

# Fonctionnalités

Scraping dynamique des offres d'emploi via Selenium.

Support Docker pour un déploiement facile.

Gestion des scrapers indépendants pour différents sites.

API REST pour récupérer les données scrapées.

Option de récupération offline des données pour applications mobiles/web.

# Technologies

Python 3.11+

Selenium

FastAPI

Docker & Docker Compose

PostgreSQL (ou autre DB selon config)

Vite/React (optionnel pour interface front)

# Prérequis

Docker et Docker Compose installés sur votre machine.

Python 3.11+ (si exécution locale hors Docker)

Navigateur Chrome et ChromeDriver compatibles (pour Selenium)

# Installation

Cloner le repository :

```bash

git clone https://github.com/FaniryRamanitrarivo/job-scraper-api.git 
cd job-scraper-api

```
Configurer les variables d’environnement (.env) :

```
SELENIUM_URL=http://selenium_chrome:4444/wd/hub
DB_HOST=postgres
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=job_scraper
```
Lancer avec Docker Compose :

```
docker-compose up --build
```

Note : Le service job_scraper_api dépend du service Selenium Chrome. Le conteneur Selenium doit être sain avant de démarrer le scraping.

Usage

Démarrer le scraper :

```bash
curl -X POST http://localhost:8000/scrape

```

Récupérer les données scrapées :

```bash
curl http://localhost:8000/jobs

```

Options de filtre (exemple) :

```bash
curl "http://localhost:8000/jobs?location=Paris&keywords=Python"
```

Architecture
┌─────────────────────────┐
│ Job Scraper API         │
│ (FastAPI REST)          │
└─────────┬───────────────┘
          │
          ▼
┌─────────────────────────┐
│ Selenium Chrome         │
│ (Docker Service)        │
└─────────┬───────────────┘
          │
          ▼
┌─────────────────────────┐
│ Database (PostgreSQL)   │
└─────────────────────────┘

- job_scraper_api : Contient les endpoints REST et la logique des scrapers.

- Selenium Chrome : Pour exécuter le scraping dynamique.

- Database : Stocke les jobs scrapés pour consultation et usage offline.

# Contribuer

1. Forker le repository.

2. Créer une branche feature : `git checkout -b feature/ma-nouvelle-fonction`.

3. Commit et push : `git commit -m "Ajout d'une fonctionnalité"`

4. Ouvrir un Pull Request pour revue.

# Licence

MIT License © Faniriniaina Andry Ramanitrarivo