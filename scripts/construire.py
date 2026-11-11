#!/usr/bin/env python3
"""Génère recensement.csv, recensement.xlsx et TABLEAU.md à partir de scripts/donnees.txt."""
import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "scripts" / "donnees.txt"
CATS = {"U": "Université", "A": "Autre établissement ESR", "N": "Cadre national"}
COLS = ["ID", "Catégorie", "Etablissement", "Entité émettrice", "Titre", "Type",
        "Public", "Doctorat", "Date", "URL page", "URL PDF", "Vérification", "Note",
        "Fichier", "Téléchargement"]
JOURNAL = ROOT / "documents" / "_journal.csv"
# Téléchargés mais sans le document attendu (page de connexion, lien invalide)
NON_PROBANT = {"U082", "U084"}

SOURCES = [
    ("Panorama des chartes sur l'utilisation de l'IA", "Observatoire IA formation, Aix-Marseille Université",
     "https://observatoire-ia-formation.univ-amu.fr/veille/chartes-sur-lutilisation-de-lia/"),
    ("Portail des chartes IA dans l'administration", "DINUM",
     "https://ia.numerique.gouv.fr/ressources/portail-des-chartes-ia-dans-ladministration/"),
    ("Références bibliographiques des chartes et guides IA", "Université Paris 8",
     "https://www.univ-paris8.fr/IMG/pdf/11_references_bibliographie.pdf"),
    ("Intelligence artificielle et technologie (documents de référence)", "CCN, Université de Strasbourg",
     "https://ccn.unistra.fr/docs-et-ressources/documents-de-reference/intelligence-artificielle-et-technologie/"),
    ("Concevoir sa charte de l'IA", "Café IA", "https://cafeia.org/concevoir-sa-charte-de-lia/"),
    ("L'IA : guides, recommandations et textes officiels", "Ascodocpsy",
     "https://www.ascodocpsy.org/actualites-de-notre-reseau/guide-dusage-de-lia-professionnel%C2%B7les-de-linformation/lia-guides-recommandations-et-textes-officiels/"),
    ("Blog APUI (copies de documents d'autres universités)", "Avignon Université",
     "https://apui.univ-avignon.fr/BlogApui/"),
    ("IA en doctorat : il faut être très discipliné dans l'usage qu'on en fait", "L'Étudiant",
     "https://www.letudiant.fr/etudes/3es-cycles-et-masters/ia-en-doctorat-il-faut-etre-tres-discipline-dans-l-usage-qu-on-en-fait.html"),
    ("Intelligence artificielle : le défi de la coopération dans l'enseignement supérieur", "EducPros",
     "https://www.letudiant.fr/educpros/enquetes/intelligence-artificielle-le-defi-de-la-cooperation-dans-lenseignement-superieur.html"),
]

LEGENDE = [
    ("Doctorat = oui", "Document propre au doctorat (école doctorale, collège doctoral, charte du doctorat, support pour doctorants)."),
    ("Doctorat = partiel", "Document général avec un volet recherche ou doctorat, ou relayé par une école doctorale."),
    ("Doctorat = à confirmer", "Présence d'un volet doctoral non vérifiée."),
    ("Vérification = Document lu", "Document téléchargé et lu : titre, date et passage sur l'IA contrôlés dans le fichier."),
    ("Vérification = Extrait", "Titre, URL et date vus dans les résultats d'un moteur de recherche. Le téléchargement a échoué (lien mort, serveur indisponible ou certificat invalide) : le document n'a pas été lu."),
    ("Vérification = Cité", "Document mentionné par une source secondaire ; URL du document non trouvée ou non confirmée."),
    ("Date", "AAAA-MM quand connue. n.d. = non datée. Une date tirée du dossier de mise en ligne peut différer de la date d'adoption."),
]


def journal():
    if not JOURNAL.exists():
        return {}
    return {r["ID"]: r for r in csv.DictReader(JOURNAL.open(encoding="utf-8"))}


def load():
    rows, jr = [], journal()
    for line in SRC.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        f = [x.strip() for x in line.split(" | ")]
        assert len(f) == 13, (len(f), line[:80])
        rid, cat = f[0], f[1]
        j = jr.get(rid)
        fichier, statut, verif = "", "non tenté", f[11]
        if rid in NON_PROBANT:
            statut = "contenu non probant (accès restreint ou lien invalide)"
        elif j and j["Statut"] in ("200", "déjà présent"):
            fichier = "documents/" + j["Fichier"]
            statut = "téléchargé"
            if verif != "Cité":
                verif = "Document lu"
        elif j:
            statut = "échec : " + j["Fichier"][:80]
        rows.append([rid, CATS[cat]] + f[2:11] + [verif, f[12], fichier, statut])
    return rows


def write_csv(rows):
    with (ROOT / "recensement.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(COLS)
        w.writerows(rows)


def sheet(wb, title, header, rows, widths):
    ws = wb.create_sheet(title)
    ws.append(header)
    for r in rows:
        ws.append(r)
    fill = PatternFill("solid", fgColor="1F3A5F")
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = fill
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, wdt in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = wdt
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
            if isinstance(c.value, str) and c.value.startswith("http"):
                c.hyperlink = c.value
                c.font = Font(color="1F5FBF", underline="single")
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    return ws


def write_xlsx(rows):
    wb = Workbook()
    wb.remove(wb.active)
    widths = [7, 14, 28, 26, 50, 16, 18, 11, 9, 40, 40, 13, 55, 40, 30]
    sheet(wb, "Tous les documents", COLS, rows, widths)
    sheet(wb, "Doctorat", COLS, [r for r in rows if r[7] in ("oui", "partiel")], widths)
    sheet(wb, "Universités", COLS, [r for r in rows if r[0].startswith("U")], widths)
    sheet(wb, "Cadres nationaux", COLS, [r for r in rows if r[0].startswith("N")], widths)
    sheet(wb, "Sources de recensement", ["Titre", "Auteur", "URL"], SOURCES, [60, 40, 80])
    sheet(wb, "Légende", ["Champ", "Signification"], LEGENDE, [25, 110])
    wb.save(ROOT / "recensement.xlsx")


def md_table(rows):
    out = ["| ID | Établissement | Entité | Titre | Type | Doctorat | Date | Lien | Vérif. |",
           "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        link = r[10] or r[9]
        lien = f"[PDF]({link})" if r[10] else (f"[Page]({link})" if link else "")
        if r[13]:
            lien += f" · [copie]({r[13]})"
        cells = [r[0], r[2], r[3], r[4], r[5], r[7], r[8], lien, r[11]]
        out.append("| " + " | ".join(c.replace("|", "/") for c in cells) + " |")
    return "\n".join(out)


def write_md(rows):
    uni = [r for r in rows if r[0].startswith("U")]
    doc = [r for r in rows if r[7] in ("oui", "partiel")]
    etabs = sorted({r[2] for r in uni})
    txt = [
        "# Chartes, recommandations et guides IA des universités françaises (2023 à 2026)",
        "",
        f"Recensement établi en novembre 2026. {len(rows)} documents : {len(uni)} issus de "
        f"{len(etabs)} universités ou établissements universitaires, "
        f"{sum(r[0].startswith('A') for r in rows)} d'autres établissements, "
        f"{sum(r[0].startswith('N') for r in rows)} cadres nationaux. "
        f"{sum(r[7] == 'oui' for r in rows)} documents sont propres au doctorat, "
        f"{sum(r[7] == 'partiel' for r in rows)} le couvrent en partie.",
        "",
        f"{sum(r[14] == 'téléchargé' for r in rows)} documents téléchargés dans `documents/` "
        f"et lus ; {sum(r[14].startswith('échec') for r in rows)} téléchargements en échec "
        "(liens morts, serveurs indisponibles, certificats invalides).",
        "",
        "Fichiers : `recensement.csv` et `recensement.xlsx` (onglets Doctorat, Universités, "
        "Cadres nationaux, Sources, Légende). Les colonnes complètes (public, URL page et PDF, note) "
        "sont dans ces fichiers.",
        "",
        "## Légende",
        "",
    ] + [f"- **{k}** : {v}" for k, v in LEGENDE] + [
        "",
        "## Documents propres au doctorat ou couvrant le doctorat",
        "",
        md_table(doc),
        "",
        "## Tous les documents",
        "",
        md_table(rows),
        "",
        "## Sources de recensement utilisées",
        "",
    ] + [f"- [{t}]({u}), {a}" for t, a, u in SOURCES] + [""]
    (ROOT / "TABLEAU.md").write_text("\n".join(txt), encoding="utf-8")


if __name__ == "__main__":
    data = load()
    write_csv(data)
    write_xlsx(data)
    write_md(data)
    print(len(data), "documents")
