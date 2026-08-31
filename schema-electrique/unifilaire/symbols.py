# -*- coding: utf-8 -*-
"""Bibliotheque de symboles unifilaires (CEI 60617) au trait Schneider.

Toutes les fonctions dessinent sur un canvas ReportLab, en coordonnees PDF
(origine en bas a gauche). Le point d'accroche d'un appareil est le point ou
son conducteur amont rejoint le jeu de barres.
"""

from .style import (BLACK, BLUE, GREEN_N, YELLOW, WHITE, GREY, F, FS_REF)

# ------------------------------------------------------------------ outils


def _solid(c, w=0.9):
    c.setDash()
    c.setLineWidth(w)
    c.setStrokeColor(BLACK)


def _dotted(c, w=0.6):
    c.setDash(1.4, 1.4)
    c.setLineWidth(w)
    c.setStrokeColor(BLACK)


def _dashed(c, w=0.9):
    c.setDash(3.2, 2.2)
    c.setLineWidth(w)
    c.setStrokeColor(BLACK)


# ----------------------------------------------------- primitives d'appareil

def pole_marks(c, x, y, poles):
    """Hachures de polarite : un trait oblique par pole protege."""
    _solid(c, 0.55)
    n = max(1, min(int(poles), 4))
    for k in range(n):
        dy = 1.9 * k
        c.line(x - 9.5, y - 1.5 - dy, x + 7.5, y + 3.0 - dy)


def trip_cross(c, x, y):
    """Croix de declenchement du disjoncteur."""
    _solid(c, 1.15)
    c.line(x - 4.2, y - 4.2, x + 4.2, y + 4.2)
    c.line(x - 4.2, y + 4.2, x + 4.2, y - 4.2)


def pivot_circle(c, x, y):
    """Pastille d'interrupteur-sectionneur, avec sa touche fixe."""
    _solid(c, 0.9)
    c.circle(x, y - 0.6, 3.3, stroke=1, fill=0)
    c.line(x - 4.6, y + 4.0, x + 4.6, y + 4.0)


def moving_contact(c, x, y_top, y_bot):
    """Contact mobile ouvert : de la touche fixe vers le conducteur aval."""
    _solid(c, 1.0)
    c.line(x - 9.0, y_top, x, y_bot)


def toroid(c, x, y):
    """Tore de detection differentielle."""
    _solid(c, 0.9)
    c.ellipse(x - 11.0, y - 4.6, x + 11.0, y + 4.6, stroke=1, fill=0)


def vigi_link(c, x, y_contact, y_tor):
    """Liaison pointillee bloc Vigi : tore -> declenchement du contact."""
    _dotted(c, 0.6)
    c.line(x - 4.4, y_contact, x + 13.0, y_contact)
    c.line(x + 13.0, y_contact, x + 13.0, y_tor)
    c.line(x + 13.0, y_tor, x + 2.0, y_tor)
    _solid(c, 0.6)
    c.line(x - 4.4, y_contact, x - 2.0, y_contact + 1.8)
    c.line(x - 4.4, y_contact, x - 2.0, y_contact - 1.8)
    c.setDash()


def coil(c, x, y):
    """Bobine de contacteur / telerupteur."""
    _solid(c, 0.9)
    c.rect(x - 5.5, y - 4.0, 11.0, 8.0, stroke=1, fill=0)
    c.line(x - 5.5, y - 4.0, x + 5.5, y + 4.0)


def contactor_contact(c, x, y_top, y_bot):
    """Contact de puissance de contacteur : contact mobile + arc."""
    moving_contact(c, x, y_top, y_bot)
    _solid(c, 0.9)
    mx, my = x - 4.5, (y_top + y_bot) / 2.0
    c.arc(mx - 3.4, my - 3.4, mx + 3.4, my + 3.4, 0, 180)


def module_box(c, x, y_top, y_bot):
    """Appareil auxiliaire non identifie : boitier modulaire."""
    _solid(c, 0.9)
    c.setFillColor(WHITE)
    c.rect(x - 9.0, y_bot, 18.0, y_top - y_bot, stroke=1, fill=1)
    c.setFillColor(BLACK)
    c.line(x - 9.0, y_bot, x + 9.0, y_top)


def block_bar(c, x, y):
    """Bloc / repartiteur vu en unifilaire."""
    _solid(c, 1.0)
    c.setFillColor(WHITE)
    c.rect(x - 16.0, y - 4.0, 32.0, 8.0, stroke=1, fill=1)
    c.setFillColor(BLACK)


def current_transformer(c, x, y, n=3):
    """Transformateurs de courant sur le conducteur de puissance."""
    _solid(c, 0.9)
    for k in range(n):
        c.circle(x + 7.0, y - 11.0 * k, 5.2, stroke=1, fill=0)


def ref_bubble(c, x, y, ref):
    """Bulle de repere (Q1, I1, D3...)."""
    if not ref:
        return
    w = max(20.0, c.stringWidth(ref, F, FS_REF) + 9.0)
    c.setDash()
    c.setLineWidth(0.7)
    c.setStrokeColor(BLACK)
    c.setFillColor(WHITE)
    c.roundRect(x, y, w, 11.0, 2.6, stroke=1, fill=1)
    c.setFillColor(BLACK)
    c.setFont(F, FS_REF)
    c.drawCentredString(x + w / 2.0, y + 3.3, ref)


# -------------------------------------------------------------- alimentation

def supply_arrow(c, x, y):
    """Triangle plein d'arrivee (origine de l'installation)."""
    c.setDash()
    c.setFillColor(BLACK)
    c.setStrokeColor(BLACK)
    p = c.beginPath()
    p.moveTo(x - 7.0, y)
    p.lineTo(x + 7.0, y)
    p.lineTo(x, y - 11.0)
    p.close()
    c.drawPath(p, stroke=1, fill=1)


def folio_arrow(c, x, y, folio, to_right=True):
    """Renvoi de folio : triangle bleu + numero de folio en vert."""
    c.setDash()
    c.setLineWidth(0.8)
    c.setStrokeColor(BLUE)
    c.setFillColor(WHITE)
    p = c.beginPath()
    if to_right:
        p.moveTo(x, y + 7.5)
        p.lineTo(x + 17.0, y)
        p.lineTo(x, y - 7.5)
    else:
        p.moveTo(x + 17.0, y + 7.5)
        p.lineTo(x, y)
        p.lineTo(x + 17.0, y - 7.5)
    p.close()
    c.drawPath(p, stroke=1, fill=1)
    c.setFillColor(GREEN_N)
    c.setFont(F, 5.4)
    c.drawCentredString(x + (5.5 if to_right else 11.5), y - 1.8, str(folio))
    c.setFillColor(BLACK)
    c.setStrokeColor(BLACK)


# ------------------------------------------------------------------- terre

def pe_bar(c, x0, x1, y):
    """Barre de terre : trait continu vert double d'un pointille jaune."""
    c.setDash()
    c.setLineWidth(1.5)
    c.setStrokeColor(GREEN_N)
    c.line(x0, y, x1, y)
    c.setDash(9, 9)
    c.setStrokeColor(YELLOW)
    c.setLineWidth(1.5)
    c.line(x0 + 4, y, x1, y)
    c.setDash()
    c.setStrokeColor(BLACK)


def earth_symbol(c, x, y):
    """Prise de terre."""
    _solid(c, 1.0)
    c.line(x, y, x, y - 5.0)
    c.line(x - 6.5, y - 5.0, x + 6.5, y - 5.0)
    c.line(x - 4.2, y - 7.4, x + 4.2, y - 7.4)
    c.line(x - 2.0, y - 9.8, x + 2.0, y - 9.8)


def pe_tap(c, x, y):
    """Reprise du conducteur PE d'un depart sur la barre de terre."""
    _solid(c, 0.9)
    c.circle(x, y, 1.1, stroke=0, fill=1)
    c.line(x, y, x - 6.0, y - 9.0)


# ----------------------------------------------------------- charges / aval

def terminal_panel(c, x, y):
    """Tableau raccorde aux borniers (symbole de la legende)."""
    _solid(c, 0.8)
    c.circle(x, y, 4.6, stroke=1, fill=0)
    c.line(x - 7.0, y, x + 7.0, y)
    c.line(x, y + 7.0, x, y - 7.0)


def socket(c, x, y):
    """Prise de courant."""
    _solid(c, 0.9)
    c.arc(x - 6.0, y - 6.0, x + 6.0, y + 6.0, 0, 180)
    c.line(x - 6.0, y, x + 6.0, y)


def lamp(c, x, y):
    """Point lumineux."""
    _solid(c, 0.9)
    c.circle(x, y, 5.0, stroke=1, fill=0)
    c.line(x - 3.5, y - 3.5, x + 3.5, y + 3.5)
    c.line(x - 3.5, y + 3.5, x + 3.5, y - 3.5)


def motor(c, x, y):
    """Moteur (rideau, portail, porte sectionnelle)."""
    _solid(c, 0.9)
    c.circle(x, y, 6.0, stroke=1, fill=0)
    c.setFont(F, 6.0)
    c.setFillColor(BLACK)
    c.drawCentredString(x, y - 2.1, "M")


def heater(c, x, y):
    """Chauffe-eau / cumulus."""
    _solid(c, 0.9)
    c.rect(x - 6.0, y - 5.0, 12.0, 10.0, stroke=1, fill=0)
    for k in (-2.5, 0.0, 2.5):
        c.line(x - 3.5, y + k, x + 3.5, y + k)


def ups(c, x, y):
    """Onduleur."""
    _solid(c, 0.9)
    c.rect(x - 11.0, y - 8.0, 22.0, 16.0, stroke=1, fill=0)
    c.line(x, y + 8.0, x, y - 8.0)
    c.setFont(F, 5.6)
    c.setFillColor(BLACK)
    c.drawCentredString(x - 5.5, y - 2.0, "~")
    c.drawCentredString(x + 5.5, y - 2.0, "=")


def dist_block(c, x0, x1, y, label=""):
    """Bloc / repartiteur de puissance."""
    _solid(c, 1.0)
    c.setFillColor(WHITE)
    c.rect(x0, y - 4.5, x1 - x0, 9.0, stroke=1, fill=1)
    c.setFillColor(BLACK)
    if label:
        c.setFont(F, 5.6)
        c.drawString(x0 + 3.0, y - 2.0, label)


LOAD_SYMBOLS = {
    "panel": terminal_panel,
    "socket": socket,
    "lamp": lamp,
    "motor": motor,
    "heater": heater,
    "ups": ups,
}
