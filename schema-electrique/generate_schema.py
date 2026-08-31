#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genere le schema unifilaire de l'etat existant (PDF multi-folios).

Usage :
    python3 generate_schema.py [chemin/de/sortie.pdf]
"""

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


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "out",
        "Schema_Unifilaire_Etat_Existant.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    doc = Document(out, data.PROJET, data.VERSION, data.DATE)
    doc.build(data.TABLEAUX, ENSEMBLES, RESERVES)
    print("Schéma généré : %s (%d folios + page de garde)" % (out, doc.n_folios))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
