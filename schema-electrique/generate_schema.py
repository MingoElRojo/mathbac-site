#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genere le schema unifilaire de l'etat existant.

Usage :
    python3 generate_schema.py                      # PDF (defaut)
    python3 generate_schema.py --format dxf         # DXF, echelle 1:1 en mm
    python3 generate_schema.py --format dwg         # DWG (via convertisseur)
    python3 generate_schema.py --format all         # les trois
    python3 generate_schema.py --out rep/ --format all
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import data_installation as data
from unifilaire.document import Document

ENSEMBLES = [
    ("1", "TGBT", "Armoire modulaire Merlin Gerin, 4 rangées", "3P+N probable",
     "Non — NS160N déporté au comptage", "Probable"),
    ("2", "TD entrepôt — bât. annexe", "Armoire Schneider récente, 3 rangées", "3P+N",
     "IG Acti9 iSW-NA 4P 63 A", "Confirmé"),
    ("3", "TDS prises entrepôt", "Coffret étanche, 1 rangée", "3P+N probable",
     "Non visible — ID1 4P 40 A 30 mA", "Confirmé"),
    ("4", "TD rideaux hangar", "Coffret étanche gris, 2 rangées", "Tri probable",
     "Non visible", "Probable"),
    ("5", "TD hangar — bât. annexe", "Grande armoire métallique ancienne", "3P+N probable",
     "Non identifiée", "À confirmer"),
    ("6", "TD établi", "Coffret modulaire blanc Schneider, 1 rangée", "Tri + mono",
     "Non visible", "À confirmer"),
    ("7", "TD 138601-ELE-ARDV-0003", "Armoire métallique murale — baie info + onduleur",
     "230 V (2P)", "ID K 2P 40 A 30 mA", "Probable"),
    ("8", "Disjoncteur d'abonné", "Appareil mural déporté — Compact NS160N", "4P",
     "Oui — STR AB 160 + Vigi MH", "Confirmé"),
    ("9", "Comptage Enedis/ERDF", "Panneau scellé — Itron ACE6000 + ACTIA", "3 × 230/400 V",
     "Sans objet", "Confirmé"),
]

RESERVES = [
    "Cheminement réel et sections des câbles entre comptage, disjoncteur d'abonné, TGBT et tableaux divisionnaires.",
    "Régime de neutre du site.",
    "Icc réel aux différents tableaux.",
    "Répartition exacte des circuits D1 à D17 sous DF1, DF2 et DF3 dans le TGBT.",
    "Calibres, sensibilités et types différentiels illisibles sur les photographies.",
    "Références exactes des anciens appareils Merlin Gerin.",
    "Protection amont et protection différentielle du TD établi.",
    "Protection générale locale du TD rideaux hangar.",
    "Fonction exacte des relais Finder et des temporisateurs du TD hangar.",
    "Séparation exacte des circuits normaux et ondulés du tableau 138601-ELE-ARDV-0003.",
    "Plaque signalétique et puissance de l'onduleur.",
    "Rapport des transformateurs de courant du comptage.",
]


BASENAME = "Schema_Unifilaire_Etat_Existant"


def _produire(chemin, backend):
    doc = Document(chemin, data.PROJET, data.VERSION, data.DATE, backend=backend)
    doc.build(data.TABLEAUX, ENSEMBLES, RESERVES)
    return doc


def main():
    ici = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("sortie", nargs="?", default=None,
                    help="chemin du fichier de sortie (déduit du format sinon)")
    ap.add_argument("--format", "-f", default="pdf",
                    choices=["pdf", "dxf", "dwg", "all"],
                    help="format à produire (défaut : pdf)")
    ap.add_argument("--out", "-o", default=os.path.join(ici, "out"),
                    help="répertoire de sortie")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    base = os.path.join(args.out, BASENAME)
    formats = ["pdf", "dxf", "dwg"] if args.format == "all" else [args.format]
    # le DWG est produit a partir du DXF : il l'entraine toujours
    if "dwg" in formats and "dxf" not in formats:
        formats.insert(0, "dxf")

    chemins = {}
    for fmt in formats:
        if fmt == "dwg":
            continue
        cible = args.sortie if (args.sortie and len(formats) == 1) \
            else base + "." + fmt
        os.makedirs(os.path.dirname(os.path.abspath(cible)), exist_ok=True)
        doc = _produire(cible, "dxf" if fmt == "dxf" else "pdf")
        chemins[fmt] = cible
        print("%-4s : %s (%d folios + page de garde)"
              % (fmt.upper(), cible, doc.n_folios))

    if "dwg" in formats:
        from unifilaire import dwg_export
        cible = args.sortie if (args.sortie and args.format == "dwg") \
            else base + ".dwg"
        try:
            dwg_export.dxf_to_dwg(chemins["dxf"], cible)
            print("DWG  : %s" % cible)
            res = dwg_export.verify_dwg(cible, chemins["dxf"])
            if res.get("verifie"):
                print("       contrôle aller-retour : %d entités restituées à "
                      "l'identique" % res["entites"])
            else:
                print("       contrôle aller-retour non effectué (%s)"
                      % res.get("motif"))
        except dwg_export.ConverterNotFound as exc:
            print("DWG  : non produit.\n%s" % exc, file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
