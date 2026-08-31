# -*- coding: utf-8 -*-
"""Folios particuliers : page de garde, origine, synoptique, reserves."""

from .style import (PAGE_W, PAGE_H, M_L, FRAME_R, TOP_Y, PE_Y, BLACK, RED,
                    GREY, SHADE, WHITE, BLUE, F, FB, FI, TAB_Y1)
from . import symbols as sym
from . import sheet


# ------------------------------------------------------------------ outils

def info_table(c, x, y, w, title, rows, col1=None, fs=6.4):
    """Petit tableau a deux colonnes ; retourne l'ordonnee du bas."""
    col1 = col1 or w * 0.42
    c.setFillColor(BLACK)
    if title:
        c.setFont(FB, 7.4)
        c.drawString(x, y, title)
        y -= 10.0
    c.setLineWidth(0.4)
    c.setStrokeColor(BLACK)
    for idx, (k, v) in enumerate(rows):
        lines = sheet.wrap(c, v, F, fs, w - col1 - 6.0)
        h = max(11.0, 4.0 + 7.6 * len(lines))
        c.setFillColor(SHADE if idx % 2 else WHITE)
        c.rect(x, y - h, w, h, stroke=0, fill=1)
        c.setStrokeColor(BLACK)
        c.rect(x, y - h, w, h, stroke=1, fill=0)
        c.line(x + col1, y - h, x + col1, y)
        c.setFillColor(BLACK)
        c.setFont(FB, fs)
        c.drawString(x + 3.0, y - 9.0, k)
        c.setFont(F, fs)
        red = v.strip().startswith("À confirmer") or v.strip().startswith("Non ")
        c.setFillColor(RED if red else BLACK)
        for i, ln in enumerate(lines):
            c.drawString(x + col1 + 3.0, y - 9.0 - i * 7.6, ln)
        c.setFillColor(BLACK)
        y -= h
    return y


# --------------------------------------------------------------- page de garde

def cover(c, doc, ensembles):
    c.setFillColor(BLACK)
    c.setFont(FB, 17.0)
    c.drawString(M_L + 18.0, PAGE_H - 62.0, "SCHÉMA UNIFILAIRE — ÉTAT EXISTANT")
    c.setFont(F, 10.5)
    c.drawString(M_L + 18.0, PAGE_H - 80.0,
                 "Relevé des tableaux électriques existants — du comptage Enedis aux tableaux divisionnaires")
    c.setLineWidth(0.8)
    c.line(M_L + 18.0, PAGE_H - 90.0, FRAME_R - 18.0, PAGE_H - 90.0)

    info_table(c, M_L + 18.0, PAGE_H - 110.0, 360.0, "Affaire", [
        ("Maître d'ouvrage", "AKPINAR YUNUS"),
        ("Adresse", "8 rue Fingues — 33310 LORMONT — France"),
        ("Contact", "akpinar.yunus@outlook.fr"),
        ("Nom du projet", "Relevé tableaux électriques — état existant"),
        ("Version", doc.version),
        ("Date", doc.date),
        ("Origine des données", "Relevé photographique de l'existant"),
    ], col1=120.0)

    info_table(c, M_L + 400.0, PAGE_H - 110.0, 400.0, "Caractéristiques générales relevées", [
        ("Origine", "Réseau public BT Enedis — comptage indirect probable sur TC"),
        ("Comptage", "Itron ACE6000 — 3 × 230/400 V — 50 Hz — télérelève ACTIA"),
        ("Disjoncteur d'abonné", "Merlin Gerin Compact NS160N + STR AB 160 + Vigi MH"),
        ("Réglage Ir apparent", "≈ 110 A (plage 90-160 A) — à confirmer"),
        ("Sensibilité Vigi MH", "0,3 A apparent — à confirmer"),
        ("Régime de neutre", "À confirmer"),
        ("Icc réel aux tableaux", "À confirmer"),
    ], col1=130.0)

    y = PAGE_H - 300.0
    c.setFillColor(BLACK)
    c.setFont(FB, 8.4)
    c.drawString(M_L + 18.0, y, "Ensembles documentés")
    y -= 12.0

    heads = ["N°", "Ensemble", "Enveloppe", "Réseau", "Coupure générale locale", "Fiabilité"]
    widths = [24.0, 168.0, 190.0, 96.0, 170.0, 100.0]
    x0 = M_L + 18.0
    c.setLineWidth(0.5)
    c.setFont(FB, 6.6)
    c.setFillColor(SHADE)
    c.rect(x0, y - 13.0, sum(widths), 13.0, stroke=0, fill=1)
    c.setFillColor(BLACK)
    x = x0
    for h, w in zip(heads, widths):
        c.rect(x, y - 13.0, w, 13.0, stroke=1, fill=0)
        c.drawString(x + 3.0, y - 9.0, h)
        x += w
    y -= 13.0
    c.setFont(F, 6.4)
    for i, row in enumerate(ensembles):
        h = 13.0
        if i % 2:
            c.setFillColor(SHADE)
            c.rect(x0, y - h, sum(widths), h, stroke=0, fill=1)
        c.setFillColor(BLACK)
        x = x0
        for val, w in zip(row, widths):
            c.rect(x, y - h, w, h, stroke=1, fill=0)
            red = val.strip().startswith("À confirmer") or val.strip().startswith("Non ")
            c.setFillColor(RED if red else BLACK)
            c.drawString(x + 3.0, y - 9.0, sheet.wrap(c, val, F, 6.4, w - 6.0)[0])
            c.setFillColor(BLACK)
            x += w
        y -= h

    y -= 22.0
    c.setFont(FB, 7.4)
    c.drawString(M_L + 18.0, y, "Limites du document")
    y -= 11.0
    c.setFont(F, 6.8)
    for t in [
        "Document de relevé de l'état existant : ni étude de conformité, ni optimisation, ni dossier de dimensionnement.",
        "La position physique des appareils dans les tableaux ne prouve pas leur raccordement électrique.",
        "Liaisons internes, sections, longueurs, régimes de neutre et courants de court-circuit non visibles sur les photographies.",
        "Toute liaison seulement probable est tracée en pointillé ; toute donnée non confirmée est annotée « à confirmer » en rouge.",
    ]:
        c.drawString(M_L + 18.0, y, u"•  " + t)
        y -= 9.5

    sheet.draw_cartouche(c, doc.projet, "Page de garde", doc.version, doc.date, "", doc.n_folios)
    c.showPage()


# ------------------------------------------------------------------- origine

def origine(c, doc, folio):
    """Folio d'origine : comptage Enedis et disjoncteur d'abonne."""
    x = 150.0

    c.setFillColor(BLACK)
    c.setFont(FB, 8.4)
    c.drawString(18.0, TOP_Y - 10.0, "ORIGINE DE L'INSTALLATION")
    c.setFont(F, 6.8)
    c.drawString(18.0, TOP_Y - 21.0, "Comptage Enedis et disjoncteur d'abonné")

    # --- reseau public
    y = TOP_Y - 46.0
    sym.supply_arrow(c, x, y)
    c.setFont(FB, 7.2)
    c.drawString(x + 22.0, y - 6.0, "Réseau public BT — Enedis / ERDF")
    c.setFont(F, 6.8)
    c.drawString(x + 22.0, y - 15.0, "3 × 230/400 V — 50 Hz")

    c.setDash()
    c.setLineWidth(1.0)
    c.setStrokeColor(BLACK)
    c.line(x, y - 11.0, x, y - 46.0)

    # --- transformateurs de courant (comptage indirect)
    y2 = y - 58.0
    c.setLineWidth(0.9)
    c.line(x, y2 + 20.0, x, y2 - 26.0)
    sym.current_transformer(c, x, y2)
    c.setFont(FB, 6.8)
    c.setFillColor(BLACK)
    c.drawString(x + 30.0, y2 + 2.0, "Transformateurs de courant (3 TC)")
    c.setFont(FI, 6.6)
    c.setFillColor(RED)
    c.drawString(x + 30.0, y2 - 7.0, "(non visibles — comptage indirect probable ; rapport à confirmer)")
    c.setFillColor(BLACK)

    # --- boitiers ESSAILEC (circuits de mesure)
    y3 = y2 - 52.0
    c.setDash(2.0, 2.0)
    c.setLineWidth(0.7)
    c.line(x + 13.0, y2 - 22.0, x + 61.0, y2 - 22.0)
    c.line(x + 61.0, y2 - 22.0, x + 61.0, y3 + 6.0)
    c.setDash()
    c.setFillColor(WHITE)
    c.rect(x + 40.0, y3 - 12.0, 42.0, 18.0, stroke=1, fill=1)
    c.setFillColor(BLACK)
    c.setFont(F, 5.8)
    c.drawCentredString(x + 61.0, y3 - 5.0, "ESSAILEC ×2")
    c.setFont(F, 6.6)
    c.drawString(x + 90.0, y3 - 2.0, "Boîtiers d'essai et de sectionnement des circuits")
    c.drawString(x + 90.0, y3 - 10.0, "de comptage — Entralec — scellés présents")

    # --- compteur
    y4 = y3 - 44.0
    c.setLineWidth(1.0)
    c.line(x, y2 - 26.0, x, y4 + 12.0)
    c.setFillColor(WHITE)
    c.circle(x, y4, 11.0, stroke=1, fill=1)
    c.setFillColor(BLACK)
    c.setFont(F, 5.8)
    c.drawCentredString(x, y4 - 2.0, "kWh")
    c.setFont(FB, 7.0)
    c.drawString(x + 22.0, y4 + 4.0, "Compteur Itron ACE6000")
    c.setFont(F, 6.6)
    c.drawString(x + 22.0, y4 - 5.0, "Triphasé 3 × 230/400 V — 50 Hz — année 2010 — mesure indirecte probable")
    # telereleve
    c.setDash(2.0, 2.0)
    c.setLineWidth(0.7)
    c.line(x + 8.0, y4 - 9.0, x + 8.0, y4 - 32.0)
    c.line(x + 8.0, y4 - 32.0, x + 222.0, y4 - 32.0)
    c.setDash()
    c.setFillColor(WHITE)
    c.rect(x + 222.0, y4 - 42.0, 92.0, 20.0, stroke=1, fill=1)
    c.setFillColor(BLACK)
    c.setFont(F, 6.0)
    c.drawCentredString(x + 268.0, y4 - 30.0, "Télérelève ACTIA")
    c.drawCentredString(x + 268.0, y4 - 38.0, "2G/3G/4G — art. 4088047")

    # --- disjoncteur d'abonne
    y5 = y4 - 62.0
    c.setLineWidth(1.0)
    c.line(x, y4 - 11.0, x, y5)
    sym.pole_marks(c, x, y5 - 12.0, 4)
    sym.trip_cross(c, x, y5 - 24.0)
    sym.moving_contact(c, x, y5 - 27.0, y5 - 41.0)
    sym.toroid(c, x, y5 - 52.0)
    sym.vigi_link(c, x, y5 - 34.0, y5 - 52.0)
    c.setLineWidth(1.0)
    c.setStrokeColor(BLACK)
    c.setDash()
    c.line(x, y5 - 41.0, x, y5 - 96.0)
    sym.ref_bubble(c, x + 20.0, y5 - 66.0, "Q1")
    c.setFont(FB, 7.2)
    c.setFillColor(BLACK)
    c.drawString(x + 56.0, y5 - 22.0, "Disjoncteur d'abonné — Merlin Gerin Compact NS160N")
    c.setFont(F, 6.8)
    c.drawString(x + 56.0, y5 - 31.0, "4P — déclencheur STR AB 160 — bloc différentiel Vigi MH")
    c.drawString(x + 56.0, y5 - 40.0, "Ir ≈ 110 A (plage 90-160 A) — Im ≈ 4 × Ir — IΔn 0,3 A")
    c.setFillColor(RED)
    c.setFont(FI, 6.6)
    c.drawString(x + 56.0, y5 - 49.0, "(réglages relevés visuellement — à confirmer)")
    c.setFillColor(BLACK)
    c.setFont(F, 6.6)
    c.drawString(x + 56.0, y5 - 58.0, "Implantation murale déportée à proximité du comptage — scellés amont")

    # --- vers TGBT
    y6 = y5 - 96.0
    sym.terminal_panel(c, x, y6)
    c.setFont(FB, 7.4)
    c.drawString(x + 22.0, y6 - 2.5, "TGBT — Tableau Général Basse Tension  (folio %d)" % (folio + 1))
    c.setFillColor(RED)
    c.setFont(FI, 6.6)
    c.drawString(x + 22.0, y6 - 12.0, "(section, longueur et cheminement de la liaison à confirmer)")
    c.setFillColor(BLACK)

    # --- tableaux de plaque
    info_table(c, 520.0, TOP_Y - 46.0, 300.0, "Plaque NS160N — pouvoir de coupure", [
        ("Ui", "750 V"), ("Uimp", "8 kV"),
        ("Norme", "IEC 947-2 — catégorie A"), ("Ics", "100 % Icu"),
        ("Icu 220/240 V", "85 kA"), ("Icu 380/415 V", "36 kA"),
        ("Icu 440 V", "35 kA"), ("Icu 500 V", "30 kA"),
        ("Icu 525 V", "22 kA"), ("Icu 660/690 V", "8 kA"),
        ("Icu 250 V DC", "50 kA"),
    ], col1=110.0, fs=6.2)

    info_table(c, 520.0, TOP_Y - 226.0, 300.0, "Réglages et commandes relevés", [
        ("STR AB 160 — Ir", "Plage 90 à 160 A"),
        ("Réglage Ir apparent", "≈ 110 A — à confirmer"),
        ("Réglage Im apparent", "≈ 4 × Ir — à confirmer"),
        ("Vigi MH — IΔn", "0,3 A apparent — à confirmer"),
        ("Vigi MH — temporisation", "Réglable — position à confirmer"),
        ("Commandes Vigi", "T = test ; R = réarmement"),
        ("Commande mécanique", "Bouton rouge push-to-trip"),
    ], col1=110.0, fs=6.2)

    c.setFillColor(RED)
    c.setFont(FI, 6.8)
    c.drawString(520.0, TOP_Y - 348.0,
                 "Attention — 36 kA est le pouvoir de coupure Icu du NS160N à 380/415 V,")
    c.drawString(520.0, TOP_Y - 357.0,
                 "et non l'Icc réel de l'installation, qui reste à déterminer.")
    c.setFillColor(BLACK)

    sheet.draw_cartouche(c, doc.projet, "Origine — comptage et disjoncteur d'abonné",
                         doc.version, doc.date, folio, doc.n_folios)
    c.showPage()


# ----------------------------------------------------------------- synoptique

def _folio_tag(fmap, code):
    """Renvoi « (folios n-m) » vers les folios du tableau."""
    if not fmap or code not in fmap:
        return ""
    a, b = fmap[code]
    return "  (folio %d)" % a if a == b else "  (folios %d à %d)" % (a, b)


def synoptique(c, doc, folio, tableaux, fmap=None):
    """Architecture generale reconstituee de l'installation."""
    c.setFillColor(BLACK)
    c.setFont(FB, 8.4)
    c.drawString(18.0, TOP_Y - 10.0, "ARCHITECTURE GÉNÉRALE RECONSTITUÉE")
    c.setFont(F, 6.8)
    c.drawString(18.0, TOP_Y - 21.0,
                 "Représentation fonctionnelle la plus cohérente avec l'ensemble des photographies")

    def box(x, y, w, h, title, sub="", dashed=False):
        c.setDash(3.2, 2.2) if dashed else c.setDash()
        c.setLineWidth(0.9)
        c.setStrokeColor(BLACK)
        c.setFillColor(WHITE)
        c.rect(x, y, w, h, stroke=1, fill=1)
        c.setDash()
        c.setFillColor(BLACK)
        c.setFont(FB, 7.0)
        tl = sheet.wrap(c, title, FB, 7.0, w - 8.0)
        for i, ln in enumerate(tl):
            c.drawString(x + 5.0, y + h - 10.0 - i * 8.4, ln)
        if sub:
            c.setFont(F, 6.0)
            yy = y + h - 10.0 - 8.4 * len(tl) - 1.0
            for ln in sheet.wrap(c, sub, F, 6.0, w - 8.0):
                c.drawString(x + 5.0, yy, ln)
                yy -= 7.2

    def link(x1, y1, x2, y2, dashed=False, w=0.9):
        c.setDash(3.2, 2.2) if dashed else c.setDash()
        c.setLineWidth(w)
        c.setStrokeColor(BLACK)
        c.line(x1, y1, x2, y2)
        c.setDash()

    # ---------------------------------------------- chaine d'alimentation
    cx, W, H = 40.0, 300.0, 34.0
    chain = [
        ("Réseau public BT — Enedis / ERDF", "3 × 230/400 V — 50 Hz", False),
        ("Comptage indirect probable — TC non visibles",
         "ESSAILEC ×2 → compteur Itron ACE6000 → télérelève ACTIA 2G/3G/4G", True),
        ("Disjoncteur d'abonné — Compact NS160N",
         "STR AB 160 — Ir ≈ 110 A — Vigi MH 0,3 A — Icu 36 kA à 415 V", False),
        ("TGBT — armoire Merlin Gerin, 4 rangées%s" % _folio_tag(fmap, "TGBT"),
         "Organe de coupure d'arrivée non identifié dans l'enveloppe", False),
    ]
    ytop = TOP_Y - 56.0
    gap = 30.0
    mids = []
    for i, (title, sub, dashed) in enumerate(chain):
        y = ytop - i * (H + gap) - H
        box(cx, y, W, H, title, sub, dashed)
        mids.append(y + H / 2.0)
        if i:
            link(cx + W / 2.0, y + H + gap, cx + W / 2.0, y + H, dashed)
    y_tgbt_mid = mids[-1]

    # ---------------------------------------------- tableaux divisionnaires
    divs = [t for t in tableaux if t.code != "TGBT"]
    xs, bw, bh, bg = 470.0, 330.0, 30.0, 9.0
    x_bus = 430.0
    ys = TOP_Y - 56.0
    centers = []
    for i, t in enumerate(divs):
        by = ys - i * (bh + bg) - bh
        box(xs, by, bw, bh, t.titre + _folio_tag(fmap, t.code),
            t.meta[0][1] if t.meta else "", dashed=True)
        cy = by + bh / 2.0
        centers.append(cy)
        link(x_bus, cy, xs, cy, True)

    if centers:
        link(x_bus, centers[0], x_bus, centers[-1], True)
        # depart du TGBT vers le jeu de barres des divisionnaires
        link(cx + W, y_tgbt_mid, x_bus, y_tgbt_mid, False, 1.1)
        c.setFont(FI, 6.2)
        c.setFillColor(RED)
        c.drawString(cx + W + 6.0, y_tgbt_mid + 4.0, "liaisons non relevées")
        c.setFillColor(BLACK)

    c.setFillColor(RED)
    c.setFont(FI, 6.8)
    c.drawString(18.0, 150.0,
                 "Limite — le compteur peut être en mesure indirecte : les conducteurs de puissance ne traversent")
    c.drawString(18.0, 141.0,
                 "alors pas directement le compteur. Les TC et leur rapport ne sont pas visibles.")
    c.drawString(18.0, 129.0,
                 "Les liaisons TGBT → tableaux divisionnaires sont tracées en pointillé : cheminement, sections et")
    c.drawString(18.0, 120.0,
                 "protections de départ ne sont pas démontrés par le relevé photographique.")
    c.setFillColor(BLACK)

    sheet.draw_cartouche(c, doc.projet, "Synoptique général", doc.version, doc.date,
                         folio, doc.n_folios)
    c.showPage()


# ------------------------------------------------------------------ reserves

def reserves(c, doc, folio, items, synthese=None):
    c.setFillColor(BLACK)
    c.setFont(FB, 8.4)
    c.drawString(18.0, TOP_Y - 10.0, "DONNÉES RESTANT À CONFIRMER AVANT SCHÉMA DÉFINITIF")
    c.setFont(F, 6.8)
    c.drawString(18.0, TOP_Y - 21.0,
                 "Points à lever sur site : tant qu'ils ne le sont pas, le schéma reste un relevé de l'existant.")

    y = TOP_Y - 44.0
    col_x = [18.0, 430.0]
    half = (len(items) + 1) // 2
    for ci, group in enumerate((items[:half], items[half:])):
        yy = y
        for it in group:
            c.setFillColor(RED)
            c.setFont(F, 7.6)
            c.drawString(col_x[ci], yy, u"■")
            c.setFillColor(BLACK)
            c.setFont(F, 7.2)
            for ln in sheet.wrap(c, it, F, 7.2, 372.0):
                c.drawString(col_x[ci] + 12.0, yy, ln)
                yy -= 9.4
            yy -= 5.0

    # ---------------------------------------------- synthese quantitative
    if synthese:
        y3 = TOP_Y - 200.0
        c.setFillColor(BLACK)
        c.setFont(FB, 7.8)
        c.drawString(18.0, y3, "Synthèse quantitative du relevé")
        y3 -= 14.0
        heads = ["Ensemble", "Folios", "Appareils relevés", "Confirmé", "Probable",
                 "À confirmer"]
        widths = [250.0, 60.0, 90.0, 62.0, 62.0, 70.0]
        c.setLineWidth(0.5)
        c.setFillColor(SHADE)
        c.rect(18.0, y3 - 13.0, sum(widths), 13.0, stroke=0, fill=1)
        c.setFillColor(BLACK)
        c.setFont(FB, 6.6)
        x = 18.0
        for h, w in zip(heads, widths):
            c.rect(x, y3 - 13.0, w, 13.0, stroke=1, fill=0)
            c.drawString(x + 3.0, y3 - 9.0, h)
            x += w
        y3 -= 13.0
        c.setFont(F, 6.4)
        for i, row in enumerate(synthese):
            if i % 2:
                c.setFillColor(SHADE)
                c.rect(18.0, y3 - 12.0, sum(widths), 12.0, stroke=0, fill=1)
            c.setFillColor(BLACK)
            x = 18.0
            for j, (val, w) in enumerate(zip(row, widths)):
                c.rect(x, y3 - 12.0, w, 12.0, stroke=1, fill=0)
                c.setFillColor(RED if (j == 5 and val not in ("0", "")) else BLACK)
                c.drawString(x + 3.0, y3 - 8.5, val)
                c.setFillColor(BLACK)
                x += w
            y3 -= 12.0

    y2 = 150.0
    c.setFont(FB, 7.4)
    c.drawString(18.0, y2, "Consigne de dessin appliquée dans ce dossier")
    c.setFont(F, 7.0)
    for i, t in enumerate([
        "Toute donnée non confirmée est annotée « à confirmer » et imprimée en rouge.",
        "Toute liaison seulement probable est tracée en pointillé.",
        "La ligne « Fiabilité du relevé » du tableau des circuits porte le niveau Confirmé / Probable / À confirmer de chaque départ.",
        "Les lignes Section, Type, Longueur et Matière de câble sont volontairement laissées vides : ces données ne sont pas relevables en photo.",
    ]):
        c.drawString(18.0, y2 - 12.0 - i * 9.6, u"•  " + t)

    sheet.draw_cartouche(c, doc.projet, "Réserves et données à confirmer",
                         doc.version, doc.date, folio, doc.n_folios)
    c.showPage()
