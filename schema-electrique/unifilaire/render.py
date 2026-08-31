# -*- coding: utf-8 -*-
"""Trace d'un tableau sur un ou plusieurs folios."""

from .style import (NCOLS, TOP_Y, FEED_Y, PE_Y, ARROW_L_X, ARROW_R_X,
                    BLACK, RED, GREY, F, FB, FI, FS_DEV, TAB_Y1, COL_W)
from . import symbols as sym
from . import sheet
from .model import layout, A_CONFIRMER

# geometrie interne d'un appareil, en ecart au point d'accroche
DY_POLES = -12.0
DY_PIVOT = -24.0
DY_CONTACT_TOP = -27.0
DY_CONTACT_BOT = -41.0
DY_TOROID = -52.0
DY_TEXT = -21.0
DEV_H = 60.0


def _feed(c, x, y0, y1, dashed):
    """Conducteur amont entre le jeu de barres et l'appareil."""
    if dashed:
        c.setDash(3.2, 2.2)
    else:
        c.setDash()
    c.setLineWidth(0.9)
    c.setStrokeColor(BLACK)
    c.line(x, y0, x, y1)
    c.setDash()


def draw_device(c, dev, y_bus, y_end):
    """Trace un appareil complet : symbole, textes, repere et conducteurs."""
    x = dev.x
    differential = dev.kind in ("rcd", "rcbo")

    # conducteur amont (pointille si la liaison n'est que probable)
    _feed(c, x, y_bus, y_bus + DY_PIVOT, dev.dashed_feed)

    # organe de coupure
    if dev.kind not in ("none", "block", "ups"):
        sym.pole_marks(c, x, y_bus + DY_POLES, dev.poles)
    if dev.kind in ("breaker", "rcbo"):
        sym.trip_cross(c, x, y_bus + DY_PIVOT)
    elif dev.kind in ("switch", "rcd"):
        sym.pivot_circle(c, x, y_bus + DY_PIVOT)
    elif dev.kind == "contactor":
        sym.coil(c, x + 26.0, y_bus + DY_PIVOT)
    if dev.kind == "ups":
        sym.ups(c, x, y_bus + DY_PIVOT - 6.0)
    elif dev.kind == "block":
        sym.block_bar(c, x, y_bus + DY_PIVOT)
    elif dev.kind == "none":
        pass
    elif dev.kind == "contactor":
        sym.contactor_contact(c, x, y_bus + DY_CONTACT_TOP, y_bus + DY_CONTACT_BOT)
    elif dev.kind == "aux":
        sym.module_box(c, x, y_bus + DY_CONTACT_TOP, y_bus + DY_CONTACT_BOT)
    else:
        sym.moving_contact(c, x, y_bus + DY_CONTACT_TOP, y_bus + DY_CONTACT_BOT)

    if differential:
        sym.toroid(c, x, y_bus + DY_TOROID)
        sym.vigi_link(c, x, y_bus + DY_CONTACT_TOP - 7.0, y_bus + DY_TOROID)

    # conducteur aval
    if dev.kind in ("none", "block", "ups"):
        _feed(c, x, y_bus + DY_PIVOT, y_bus + DY_CONTACT_BOT, dev.dashed_feed)
    c.setDash()
    c.setLineWidth(0.9)
    c.setStrokeColor(BLACK)
    c.line(x, y_bus + DY_CONTACT_BOT, x, y_end)

    # designation technique
    c.setFillColor(BLACK)
    ty = y_bus + DY_TEXT
    for i, ln in enumerate(dev.lines):
        alert = ln.strip().startswith("(")
        c.setFont(FI if alert else F, FS_DEV)
        c.setFillColor(RED if alert else BLACK)
        c.drawString(x + 20.0, ty, ln)
        ty -= 9.4
    c.setFillColor(BLACK)

    # bulle de repere
    by = min(ty - 2.0, y_bus - 33.0)
    if differential:
        by = min(by, y_bus + DY_TOROID + 0.5)
    sym.ref_bubble(c, x + 20.0, by, dev.ref)


def draw_load(c, dev):
    """Symbole d'utilisation en pied de depart."""
    if not dev.load:
        return
    fn = sym.LOAD_SYMBOLS.get(dev.load)
    if fn is None:
        return
    fn(c, dev.x, PE_Y + 30.0)
    c.setFillColor(BLACK)


def render_tableau(c, doc, tab):
    """Trace le tableau `tab` sur autant de folios que necessaire."""
    devices, buses, n_pages = layout(tab)
    first_folio = doc.folio

    for p in range(n_pages):
        folio = first_folio + p
        page_devs = [d for d in devices if d.page == p]
        for d in page_devs:
            d.x = sheet.col_axis(d.col % NCOLS)

        sheet.draw_columns(c, len(page_devs))

        # ------------------------------------------------ jeux de barres
        for b in buses:
            p0, p1 = b.first_col // NCOLS, b.last_col // NCOLS
            if p < p0 or p > p1:
                continue
            if p == p0:
                x0 = sheet.col_axis(b.first_col % NCOLS)
            else:
                x0 = ARROW_L_X + 17.0
                sym.folio_arrow(c, ARROW_L_X, b.y, first_folio + p - 1, False)
            if p == p1:
                x1 = sheet.col_axis(b.last_col % NCOLS)
            else:
                x1 = ARROW_R_X
                sym.folio_arrow(c, ARROW_R_X, b.y, first_folio + p + 1, True)
            c.setDash()
            c.setLineWidth(1.0)
            c.setStrokeColor(BLACK)
            if x1 > x0:
                c.line(x0, b.y, x1, b.y)
            if b.source is not None and b.source.bus_label:
                c.setFont(FI, 5.8)
                c.setFillColor(GREY)
                c.drawString(x0 + 6.0, b.y + 3.6, b.source.bus_label)
                c.setFillColor(BLACK)

        # ------------------------------------------------ appareils
        taps = []
        for d in page_devs:
            bus_y = None
            if d is tab.arrivee:
                # arrivee : triangle d'origine puis descente vers le JdB
                sym.supply_arrow(c, d.x, FEED_Y)
                c.setDash()
                c.setLineWidth(0.9)
                c.line(d.x, FEED_Y - 11.0, d.x, FEED_Y - 18.0)
                bus_y = FEED_Y - 18.0
                y_end = buses[d.bus_out].y
                draw_device(c, d, bus_y, y_end)
                continue
            bus_y = buses[d.bus_in].y
            if d.is_group:
                y_end = buses[d.bus_out].y
            else:
                y_end = PE_Y
                taps.append(d.x)
            draw_device(c, d, bus_y, y_end)
            if not d.is_group:
                draw_load(c, d)

        # ------------------------------------------------ terre et tableau
        sheet.draw_pe(c, taps)

        cells = [None] * NCOLS
        for d in page_devs:
            cells[d.col % NCOLS] = {
                "ref": d.ref,
                "designation": d.designation,
                "gamme": d.gamme,
                "fiabilite": d.fiabilite,
                "section": "", "type_cable": "", "longueur": "", "matiere": "",
            }
        sheet.draw_circuit_table(c, cells)

        # ------------------------------------------------ habillage folio 1
        if p == 0:
            sheet.draw_legend(c)
            _draw_meta(c, tab)
        if tab.alerte and p == 0:
            c.setFillColor(RED)
            c.setFont(FI, 6.6)
            for i, ln in enumerate(sheet.wrap(c, tab.alerte, FI, 6.6, 152.0)):
                c.drawString(18.0, 300.0 - i * 8.0, ln)
            c.setFillColor(BLACK)

        sheet.draw_cartouche(c, doc.projet, tab.titre, doc.version, doc.date,
                             folio, doc.n_folios)
        c.showPage()

    doc.folio += n_pages


def _draw_meta(c, tab):
    """Bloc d'identification du tableau (zone libre en haut a gauche)."""
    x, y = 18.0, TOP_Y - 100.0
    c.setFillColor(BLACK)
    c.setFont(FB, 8.4)
    c.drawString(x, y, tab.code)
    y -= 11.0
    c.setFont(F, 6.8)
    for ln in sheet.wrap(c, tab.titre, F, 6.8, 150.0):
        c.drawString(x, y, ln)
        y -= 8.4
    y -= 4.0
    for k, v in tab.meta:
        c.setFont(FB, 6.2)
        c.drawString(x, y, "%s :" % k)
        c.setFont(F, 6.2)
        lines = sheet.wrap(c, v, F, 6.2, 92.0)
        for j, ln in enumerate(lines):
            c.drawString(x + 66.0, y - j * 7.4, ln)
        y -= 7.4 * max(1, len(lines))
    if tab.notes:
        y -= 6.0
        c.setFont(FB, 6.2)
        c.drawString(x, y, "Observations")
        y -= 8.0
        c.setFont(F, 6.0)
        for n in tab.notes:
            for ln in sheet.wrap(c, u"• " + n, F, 6.0, 150.0):
                c.drawString(x, y, ln)
                y -= 7.2
