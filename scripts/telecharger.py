#!/usr/bin/env python3
"""Télécharge les documents référencés dans ../recensement.csv.

Usage (depuis le dossier chartes-ia-universites) :
    python3 scripts/telecharger.py
    python3 scripts/telecharger.py --doctorat   # seulement les documents liés au doctorat

Les fichiers sont enregistrés dans documents/<ID>_<universite>.<ext>.
Si une ligne n'a pas d'URL PDF directe, la page HTML est enregistrée à la place.
Un journal est écrit dans documents/_journal.csv (statut HTTP, taille, empreinte SHA-256).
Aucune dépendance externe : bibliothèque standard Python 3.8+.
"""
import csv
import hashlib
import re
import sys
import time
import unicodedata
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "recensement.csv"
OUT = ROOT / "documents"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")


def slug(text, n=40):
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-").lower()[:n]


def fetch(url, essais=2):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    for k in range(essais):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.status, r.headers.get("Content-Type", ""), r.read()
        except Exception:  # noqa: BLE001
            if k == essais - 1:
                raise
            time.sleep(5)


def main():
    only_doc = "--doctorat" in sys.argv
    OUT.mkdir(exist_ok=True)
    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8")))
    log = []
    existants = {p.name.split("_")[0]: p.name for p in OUT.iterdir()
                 if p.is_file() and not p.name.startswith("_")}
    ancien = {}
    if (OUT / "_journal.csv").exists():
        for r in csv.reader((OUT / "_journal.csv").open(encoding="utf-8")):
            ancien[r[0]] = r
    for row in rows:
        if only_doc and row["Doctorat"].lower() not in ("oui", "partiel"):
            continue
        url = row["URL PDF"].strip() or row["URL page"].strip()
        if not url:
            continue
        if row["ID"] in existants:
            old = ancien.get(row["ID"])
            if old and old[2] == "200" and old[6] == existants[row["ID"]]:
                log.append(old)
            else:
                log.append([row["ID"], url, "déjà présent", "", 0, "", existants[row["ID"]]])
            continue
        try:
            status, ctype, data = fetch(url)
            ext = "pdf" if ("pdf" in ctype or data[:4] == b"%PDF") else (
                "docx" if "word" in ctype else "html")
            name = f'{row["ID"]}_{slug(row["Etablissement"])}.{ext}'
            (OUT / name).write_bytes(data)
            log.append([row["ID"], url, status, ext, len(data),
                        hashlib.sha256(data).hexdigest(), name])
            print(f'OK  {row["ID"]} {name} ({len(data)//1024} Ko)')
        except Exception as e:  # noqa: BLE001
            log.append([row["ID"], url, "ERREUR", "", 0, "", str(e)[:120]])
            print(f'ERR {row["ID"]} {url} -> {e}')
        time.sleep(1)
    with (OUT / "_journal.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ID", "URL", "Statut", "Format", "Octets", "SHA256", "Fichier"])
        w.writerows(log)


if __name__ == "__main__":
    main()
