# -*- coding: utf-8 -*-
"""Constantes graphiques : format de folio, gabarit et couleurs.

Le gabarit reproduit la mise en page des schemas unifilaires produits par
Schneider Electric eDesign : folio A4 paysage, cartouche en pied de page,
tableau des circuits, barre PE vert/jaune et colonnes alternees.
"""

from reportlab.lib.colors import HexColor

# ---------------------------------------------------------------- format
PAGE_W = 841.89          # A4 paysage (pt)
PAGE_H = 595.28

# ---------------------------------------------------------------- couleurs
BLACK = HexColor("#000000")
GREY = HexColor("#5a5a5a")
RULE = HexColor("#000000")
SHADE = HexColor("#f5f5f5")
BLUE = HexColor("#2222bb")
GREEN_N = HexColor("#0f8a2f")
YELLOW = HexColor("#f5e400")
RED = HexColor("#b00000")
WHITE = HexColor("#ffffff")

# ---------------------------------------------------------------- gabarit
M_L = 12.0               # marge gauche du cadre
M_R = 12.0
FRAME_R = PAGE_W - M_R

CART_Y0 = 14.0           # cartouche
CART_H = 48.0
CART_Y1 = CART_Y0 + CART_H

TAB_Y0 = 70.0            # tableau des circuits
TAB_LABEL_X0 = M_L
TAB_LABEL_W = 168.0
COL_X0 = TAB_LABEL_X0 + TAB_LABEL_W      # 180
COL_W = 105.0
NCOLS = 5
COL_X1 = COL_X0 + COL_W * NCOLS          # 705

# lignes du tableau des circuits (libelle, hauteur, cle de donnee)
TABLE_ROWS = [
    ("Identification du circuit", 11.0, "ref"),
    ("Désignation", 21.0, "designation"),
    ("", 6.0, None),
    ("Section de câble", 11.0, "section"),
    ("Type de câble", 11.0, "type_cable"),
    ("Longueur du câble", 11.0, "longueur"),
    ("Matière du câble", 11.0, "matiere"),
    ("Gamme relevée", 11.0, "gamme"),
    ("Fiabilité du relevé", 11.0, "fiabilite"),
]
TAB_H = sum(r[1] for r in TABLE_ROWS)
TAB_Y1 = TAB_Y0 + TAB_H                  # ~= 174

# barre de terre
PE_Y = TAB_Y1 + 26.0                     # ~= 200
PE_X0 = 100.0
PE_X1 = FRAME_R - 4.0

# zone schema
TOP_Y = PAGE_H - 16.0                    # 579
FEED_Y = TOP_Y - 4.0                     # accroche de l'arrivee

# niveaux de jeu de barres par profondeur
BUS_Y = [505.0, 440.0, 375.0, 312.0]
BUS_STAGGER = 15.0                       # decalage anti-collision

# fleches de renvoi de folio
ARROW_L_X = 22.0
ARROW_R_X = FRAME_R - 24.0

# polices
F = "Helvetica"
FB = "Helvetica-Bold"
FI = "Helvetica-Oblique"
FS_DEV = 6.8             # texte a cote des appareils
FS_REF = 6.0             # repere dans la bulle
FS_TAB = 5.4             # tableau des circuits
FS_CART = 9.0            # cartouche
