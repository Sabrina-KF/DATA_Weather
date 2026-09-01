# Pipeline ELT — Météo Tours

Pipeline de données de bout en bout : extraction d'une API publique, transformation avec contrôle qualité, orchestration via Dagster, chargement en base PostgreSQL, et restitution dans un dashboard Streamlit.

Projet construit pour démontrer une chaîne Data Engineering complète et réellement exécutable, pas seulement un notebook isolé.

## Pourquoi ce projet

En reconversion vers le Data Engineering après plusieurs années en ingénierie logicielle et QA, je voulais un projet qui prouve que je sais construire un pipeline de bout en bout et le faire tourner en production locale, pas seulement écrire une requête SQL ou un notebook Jupyter.

## Architecture

\`\`\`mermaid
flowchart LR
    A[API Open-Meteo] -->|extract.py| B[Données brutes]
    B -->|transform.py + quality.py| C[Données validées]
    C -->|load.py| D[(PostgreSQL)]
    D --> E[Dashboard Streamlit]

    subgraph Orchestration Dagster
        B
        C
        D
    end
\`\`\`

Chaque étape est un asset Dagster : versionné, observable, rejouable indépendamment depuis l'interface Dagster (localhost:3000).

## Stack technique

| Étape | Outil | Pourquoi |
|---|---|---|
| Extraction | API Open-Meteo | Gratuite, sans clé, données réelles |
| Transformation | Python / Pandas | Typage, colonnes dérivées |
| Qualité des données | Module maison | Simple, lisible, testé |
| Orchestration | Dagster | Paradigme asset-based, moderne |
| Stockage | PostgreSQL | Standard, robuste |
| Visualisation | Streamlit | Rapide, lisible |
| Tests | Pytest | 6 tests unitaires |
| CI | GitHub Actions | Tests à chaque push |

## Lancer le projet

\`\`\`bash
git clone https://github.com/Sabrina-KF/DATA_Weather
cd tours-weather-pipeline
cp .env.example .env
pip install -r requirements.txt

make up
make dagster
make dashboard
make test
\`\`\`

## Structure du projet

\`\`\`
tours-weather-pipeline/
├── src/
├── dashboard/
├── tests/
├── docker-compose.yml
├── Makefile
└── .github/workflows/ci.yml
\`\`\`

## Ce que ce projet démontre

- Extraction depuis une API réelle, gestion d'erreurs HTTP
- Contrôles qualité systématiques avant chargement
- Orchestration moderne (Dagster)
- Tests unitaires sur la logique métier
- CI à chaque commit
- Dashboard réellement consultable

---

*Je rends public la version finale de ce projet réalisé dans le cadre de ma reconversion en Data Engineering, en complément de mon IBM Data Science Professional Certificate. Voici le résultat de l'apprentissage et de l'utilisation des outils et méthodes apprises tout au long de ma carrière dans le cadre d'une requête propre à la ville de Tours.*