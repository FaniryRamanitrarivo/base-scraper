## 1️⃣ Utilise le standard Conventional Commits

👉 Format :

```code
<type>(scope): description courte

[body optionnel]

[footer optionnel]
```
Exemple :
```code
feat(auth): add JWT refresh token mechanism

Implement refresh token rotation to improve security.
Add httpOnly cookie storage.

Closes #42
```

## 2️⃣ Les types de commits (les plus importants)
| Type	| Usage
| :---  | :---
| feat	| Nouvelle fonctionnalité
| fix	| Correction de bug
| refactor	| Modification interne sans changement fonctionnel
| perf	| Optimisation performance
| docs	| Documentation
| test	| Ajout/modification de tests
| chore	| Maintenance (deps, config, build…)
| style	| Formatage uniquement

## 3️⃣ Exemples adaptés à TON contexte
- Projet Next.js
```code
feat(project): add server action for project deletion
fix(cache): prevent stale project data after deletion
refactor(api): extract fetch logic into reusable service
```
- Projet scraping Python
```code
feat(scraper): add pagination support for opham listings
fix(parser): handle missing salary field safely
perf(scraper): reduce selenium wait time using explicit waits
```
- Extension Chrome (React + TS)
```code
feat(content-script): implement message bridge with background
fix(popup): resolve state hydration issue on reload
```
## 4️⃣ Les règles d’un message pro

### ✅ 1. La première ligne :
- max 72 caractères
- impératif présent
- pas de point à la fin

✔ Bon :
```code
fix(api): handle null response correctly
```
❌ Mauvais :
```code
Fixed bug in API.
```

### ✅ 2. Toujours expliquer le "pourquoi", pas le "quoi"

Mauvais :
```
update project
```
Bon :
```
fix(project): prevent crash when project id is undefined
Add guard clause to avoid calling API with invalid id.
```

### 5️⃣ Quand écrire un body ?

Ajoute un body si :
- la logique est complexe
- il y a un changement architectural
- il y a un breaking change

Exemple :
```
refactor(auth): decouple auth logic from API layer

Move token validation into dedicated service.
This improves testability and separation of concerns.
```
Ça, c’est niveau senior.

## 6️⃣ Commit = 1 responsabilité

❌ Mauvais :
```
feat: add login and fix dashboard and update readme
```
✅ Bon :
```
feat(auth): add login endpoint
fix(dashboard): correct stats calculation
docs(readme): update setup instructions
```
## 7️⃣ Bonus : Commit "Breaking Change"
```
feat(api)!: change project response structure

BREAKING CHANGE: project list now returns paginated object
instead of raw array
```
Le `!` indique un breaking change.

## 8️⃣ Workflow professionnel

Pour ton profil senior :

- Avant commit :
```
git diff
git add -p
```
- Commit atomique :
```
git commit
```
(et écris proprement, pas en inline)

## 9️⃣ Outil recommandé

Installe **Commitlint + Husky**

👉 Ça empêche les commits mal formés.

##🎯 Résumé

Un commit pro :
- Est clair
- Est court
- Explique l’intention
- Est atomique
- Suit une convention