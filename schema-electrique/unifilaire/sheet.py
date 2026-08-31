# -*- coding: utf-8 -*-
"""Gabarit de folio : cadre, colonnes, tableau des circuits et cartouche."""

from .style import (PAGE_W, PAGE_H, M_L, FRAME_R, CART_Y0, CART_H, CART_Y1,
                    TAB_Y0, TAB_Y1, TAB_LABEL_X0, TAB_LABEL_W, COL_X0, COL_W,
                    NCOLS, COL_X1, TABLE_ROWS, TOP_Y, PE_Y, PE_X0, PE_X1,
                    BLACK, GREY, SHADE, WHITE, RED, F, FB, FI, FS_TAB, FS_CART)
from . import symbols as sym


# ------------------------------------------------------------------ helpers

def col_left(i):
    return COL_X0 + COL_W * i


def col_axis(i):
    """Abscisse du conducteur de la colonne i (0..NCOLS-1)."""
    return col_left(i) + 22.0


def wrap(c, text, font, size, width):
    """Decoupe un texte sur plusieurs lignes pour tenir dans `width`."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if c.stringWidth(trial, font, size) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------------------- fond

def draw_columns(c, used_cols):
    """Trame de colonnes : fond alterne et filets verticaux."""
    for i in range(NCOLS):
        x = col_left(i)
        if i % 2 == 1:
            c.setFillColor(SHADE)
            c.rect(x, TAB_Y0, COL_W, TOP_Y - TAB_Y0, stroke=0, fill=1)
    c.setStrokeColor(GREY)
    c.setLineWidth(0.25)
    c.setDash()
    for i in range(NCOLS + 1):
        x = col_left(i)
        c.line(x, TAB_Y0, x, TOP_Y)
    c.setStrokeColor(BLACK)


# --------------------------------------------------------- tableau circuits

def draw_circuit_table(c, cells):
    """Tableau des circuits. `cells` : liste de dicts par colonne (ou None)."""
    c.setLineWidth(0.45)
    c.setStrokeColor(BLACK)
    c.setDash()

    # fond alterne des colonnes de donnees
    for i in range(NCOLS):
        if i % 2 == 1:
            c.setFillColor(SHADE)
            c.rect(col_left(i), TAB_Y0, COL_W, TAB_Y1 - TAB_Y0, stroke=0, fill=1)

    y = TAB_Y1
    c.setFillColor(BLACK)
    for label, h, key in TABLE_ROWS:
        c.line(TAB_LABEL_X0, y, COL_X1, y)
        if label:
            c.setFont(F, FS_TAB)
            c.drawString(TAB_LABEL_X0 + 3.0, y - 7.6, label)
        if key:
            for i in range(NCOLS):
                data = cells[i] if i < len(cells) else None
                if not data:
                    continue
                val = data.get(key) or ""
                if not val:
                    continue
                is_alert = (key == "fiabilite" and val.startswith("À"))
                c.setFillColor(RED if is_alert else BLACK)
                c.setFont(F, FS_TAB)
                lines = wrap(c, val, F, FS_TAB, COL_W - 6.0)[:2]
                ty = y - 7.6
                for ln in lines:
                    c.drawString(col_left(i) + 3.0, ty, ln)
                    ty -= 6.2
                c.setFillColor(BLACK)
        y -= h
    c.line(TAB_LABEL_X0, TAB_Y0, COL_X1, TAB_Y0)

    # filets verticaux du tableau
    c.line(TAB_LABEL_X0, TAB_Y0, TAB_LABEL_X0, TAB_Y1)
    for i in range(NCOLS + 1):
        x = col_left(i)
        c.line(x, TAB_Y0, x, TAB_Y1)


# ----------------------------------------------------------------- cartouche

CART_CELLS = [150.0, 240.0, 200.0, 90.0, 90.0, 47.89]


def fit(c, text, font, maxw, size, mini=5.6):
    """Reduit la taille de police jusqu'a ce que le texte tienne dans maxw."""
    while size > mini and c.stringWidth(text, font, size) > maxw:
        size -= 0.4
    return size


def draw_cartouche(c, projet, tableau, version, date, folio, nfolios):
    c.setDash()
    c.setLineWidth(0.7)
    c.setStrokeColor(BLACK)
    c.setFillColor(WHITE)
    c.rect(M_L, CART_Y0, FRAME_R - M_L, CART_H, stroke=1, fill=1)
    c.setFillColor(BLACK)

    x = M_L
    xs = []
    for w in CART_CELLS:
        xs.append(x)
        x += w
    for x0 in xs[1:]:
        c.line(x0, CART_Y0, x0, CART_Y1)

    ty = CART_Y0 + CART_H / 2.0 - 3.0
    c.setFont(FB, 7.2)
    c.drawString(xs[0] + 8.0, CART_Y0 + 28.0, "RELEVÉ DE L'ÉTAT EXISTANT")
    c.setFont(F, 6.2)
    c.drawString(xs[0] + 8.0, CART_Y0 + 18.0, "Schéma unifilaire — sans étude")
    c.drawString(xs[0] + 8.0, CART_Y0 + 10.0, "de conformité ni dimensionnement")

    c.setFont(F, fit(c, projet, F, CART_CELLS[1] - 20.0, FS_CART))
    c.drawString(xs[1] + 10.0, ty, projet)
    c.setFont(F, fit(c, tableau, F, CART_CELLS[2] - 20.0, FS_CART))
    c.drawString(xs[2] + 10.0, ty, tableau)
    c.drawString(xs[3] + 8.0, ty, "Version: %s" % version)
    c.drawString(xs[4] + 8.0, ty + 4.0, date)
    c.setFont(F, 7.0)
    c.drawString(xs[4] + 8.0, ty - 6.0, "(DD.MM.YYYY)")
    c.setFont(F, FS_CART)
    if folio:
        c.drawString(xs[5] + 6.0, ty, "%s / %s" % (folio, nfolios))


# ------------------------------------------------------------------ legende

def draw_legend(c, x=20.0, y=TOP_Y - 8.0, extra=True):
    c.setFillColor(BLACK)
    c.setFont(F, 7.4)
    c.drawString(x, y, "Légende")
    c.setFont(F, 6.8)
    y -= 10.0
    for t in ("Q- Dispositifs de protection",
              "I- Interrupteurs",
              "X- Autres appareils"):
        c.drawString(x, y, t)
        y -= 9.0
    sym.terminal_panel(c, x + 5.0, y - 1.0)
    c.setFillColor(BLACK)
    c.setFont(F, 6.8)
    c.drawString(x + 15.0, y - 3.0, "Tableau raccordé aux borniers")
    y -= 14.0
    if extra:
        c.setDash(3.2, 2.2)
        c.setLineWidth(0.9)
        c.line(x, y - 1.0, x + 11.0, y - 1.0)
        c.setDash()
        c.setFont(F, 6.8)
        c.drawString(x + 15.0, y - 3.0, "Liaison probable — à confirmer sur site")
        y -= 11.0
        c.setFillColor(RED)
        c.drawString(x, y - 3.0, "Rouge : donnée non confirmée par le relevé")
        c.setFillColor(BLACK)


# --------------------------------------------------------------- barre PE

def draw_pe(c, taps):
    sym.pe_bar(c, PE_X0, PE_X1, PE_Y)
    sym.earth_symbol(c, PE_X0 + 8.0, PE_Y)
    for x in taps:
        sym.pe_tap(c, x, PE_Y)
