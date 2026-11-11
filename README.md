# Chartes, recommandations et guides IA des universités françaises (2023 à 2026)

Recensement des textes publiés depuis janvier 2023 par les universités françaises sur l'usage de l'IA (surtout générative), avec un repérage spécifique des textes qui portent sur le doctorat. État au 11 novembre 2026.

## Contenu du dossier

| Fichier | Rôle |
|---|---|
| `SYNTHESE-DOCTORAT.md` | Synthèse des dispositions sur l'IA en doctorat, statistiques, tendances et sources |
| `TABLEAU.md` | Tableau lisible : d'abord les documents liés au doctorat, puis l'ensemble |
| `recensement.xlsx` | Tableau complet avec filtres, onglets Doctorat, Universités, Cadres nationaux, Sources de recensement, Légende |
| `recensement.csv` | Même contenu au format CSV (UTF-8) |
| `domaines.txt` | Domaines à autoriser pour télécharger les documents |
| `scripts/donnees.txt` | Source unique des données (une ligne par document) |
| `scripts/construire.py` | Régénère le CSV, le XLSX et `TABLEAU.md` à partir de `donnees.txt` |
| `scripts/telecharger.py` | Télécharge les documents dans `documents/` avec un journal (statut, taille, SHA-256) |
| `documents/` | Documents téléchargés, journal `_journal.csv`, texte extrait dans `_texte/` |
| `scripts/exclus.txt` | Documents retirés après lecture |

## Chiffres clés

Les chiffres à jour sont en tête de `TABLEAU.md` (régénéré à chaque téléchargement). Au 11 novembre 2026 :

- 143 documents : 125 émanant de 70 universités ou établissements universitaires (établissement, composante ou école doctorale), 6 d'autres établissements d'enseignement supérieur, 12 cadres nationaux.
- Doctorat : 12 documents propres au doctorat, 19 qui le couvrent en partie.
- 119 documents téléchargés dans `documents/` (PDF, pages HTML, un .docx), dont 106 lus et contrôlés (titre, date, passage sur l'IA). Le texte des deux premières pages de chaque PDF est dans `documents/_texte/`.
- 5 documents retirés après lecture car hors sujet ou en doublon (`scripts/exclus.txt`).

## Ce qu'il faut retenir sur le doctorat

- Aucun texte national dédié à l'IA en doctorat n'a été trouvé. Le texte national le plus proche est la fiche de l'Ofis [« Systèmes d'intelligence artificielle générative : quelques points de vigilance »](documents/N006_ofis-hceres.pdf) (février 2024).
- Les règles doctorales viennent des écoles doctorales et des chartes du doctorat. Les textes suivants ont été lus et vérifiés :
  - la [charte du doctorat PSL](documents/U033_universite-psl.pdf) (juin 2026, section 2.7, dont certaines dispositions sont obligatoires) ;
  - la [charte du doctorat de l'EHESS, ED 286](documents/U040_ehess.pdf) (section 2.1.2 L'intelligence artificielle) ;
  - la [charte du doctorat de l'ED de droit de la Sorbonne](documents/U008_universite-paris-1-pantheon-sorbonne.pdf) (Paris 1, juillet 2024, section « Pour un bon usage de l'IA ») ;
  - le [règlement intérieur de l'ED 642 VAAME](documents/U066_etablissements-doctoraux-des-pays-de-la-.pdf) (Pays de la Loire, décembre 2025) ;
  - les supports [« Faire un doctorat à l'ère des LLM »](documents/U029_universite-paris-saclay.pdf) et [« Preparing a PhD in the age of LLMs »](documents/U030_universite-paris-saclay.pdf) de l'Université Paris-Saclay (septembre 2026) ;
  - le [compte rendu du Collège des écoles doctorales normandes du 19 mai 2025](documents/U120_normandie-universite.pdf) (encadrement de l'IA générative en doctorat).
- Hors université publique, le [guide doctoral de l'Institut catholique de Paris](documents/A001_institut-catholique-de-paris.pdf) (2025) pose que l'écrit de thèse ne doit pas être produit par une IA.
- Plusieurs chartes d'établissement couvrent la recherche sans viser les doctorants en tant que tels : [Toulouse](documents/U070_universite-de-toulouse.pdf), [Clermont Auvergne](documents/U080_universite-clermont-auvergne.pdf), [La Réunion](documents/U088_universite-de-la-reunion.pdf), [Le Mans](https://www.univ-lemans.fr/_resource/06-Universit%C3%A9/Organisation-fonctionnement/Instances/Conseil%20administration/CA-2025/CA-2025-09-25/1.4.3%20%E2%80%93%20Charte%20sur%20l'utilisation%20de%20l'Intelligence%20Artificielle%20au%20sein%20de%20Le%20Mans%20Universit%C3%A9.pdf?download=true), [Rouen](https://www.univ-rouen.fr/actualites/lurn-se-dote-dune-charte-dusage-de-lia-generative/), [Orléans](documents/U065_universite-d-orleans.pdf), [Paris 8](documents/U018_universite-paris-8.pdf).

## Méthode et limites

1. Recherche par moteur de recherche, université par université (universités publiques de métropole et d'outre-mer), en trois passes, puis recherches ciblées sur le doctorat et sur les recensements existants (DINUM, observatoire IA formation d'Aix-Marseille, bibliographie de Paris 8, CCN de Strasbourg).
2. Téléchargement par GitHub Actions : l’environnement de travail ne pouvait pas joindre les sites universitaires.
3. Lecture des fichiers téléchargés pour contrôler titre, date et contenu ; les corrections sont reportées dans `scripts/donnees.txt`.
4. Colonne Vérification :
   - `Document lu` : fichier téléchargé et contrôlé.
   - `Extrait` : vu dans les résultats d'un moteur de recherche, téléchargement en échec.
   - `Cité` : seulement mentionné par une source secondaire.
5. Une date tirée du dossier de mise en ligne peut différer de la date d'adoption.
6. L'absence d'une université ne prouve pas l'absence de texte. Établissements sans document propre trouvé après trois passes : Sorbonne Paris Nord, UTC Compiègne, Littoral Côte d'Opale, Antilles, Guyane, Corse. 21 liens restent en échec et 2 pages ne contiennent pas le document attendu (liens morts, serveurs indisponibles, certificats invalides) : ces lignes gardent la mention `Extrait` ou `Cité`. Pau, Toulouse Jean Jaurès et Artois n'ont que des clauses d'examen ou des projets annoncés.

## Télécharger ou mettre à jour les documents

- Le téléchargement initial a été fait par un workflow GitHub Actions du dépôt Cercle-IA/ia-education. Le script ne retélécharge pas les fichiers déjà présents et réessaie les échecs.
- En local, avec Python 3.8 ou plus :

```bash
python3 scripts/telecharger.py
```

## Mettre à jour

Ajoutez ou corrigez une ligne dans `scripts/donnees.txt`, puis lancez `python3 scripts/construire.py`.
