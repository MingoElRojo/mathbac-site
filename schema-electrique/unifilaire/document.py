# -*- coding: utf-8 -*-
"""Assemblage du dossier : page de garde, folios speciaux et tableaux."""

from reportlab.pdfgen import canvas

from .style import PAGE_W, PAGE_H
from .model import layout
from . import pages, render


class Document(object):
    """Contexte de generation : cartouche commun et compteur de folios."""

    def __init__(self, path, projet, version, date, backend="pdf"):
        self.path = path
        self.projet = projet
        self.version = version
        self.date = date
        self.backend = backend
        self.folio = 1
        self.n_folios = 0
        self.layout_names = []
        if backend == "dxf":
            from .dxf_canvas import DxfCanvas
            self.c = DxfCanvas(path)
        else:
            self.c = canvas.Canvas(path, pagesize=(PAGE_W, PAGE_H))
        self.c.setTitle(projet)
        self.c.setAuthor("Relevé de l'état existant")
        self.c.setSubject("Schéma unifilaire — état existant")

    # ------------------------------------------------------------------
    def count_folios(self, tableaux, extra=3):
        """Nombre total de folios numerotes (hors page de garde)."""
        n = extra
        for t in tableaux:
            n += layout(t)[2]
        self.n_folios = n
        return n

    def folio_map(self, tableaux, first):
        """Folio de debut et de fin de chaque tableau."""
        out, f = {}, first
        for t in tableaux:
            n = layout(t)[2]
            out[t.code] = (f, f + n - 1)
            f += n
        return out

    def synthese(self, tableaux, fmap):
        """Denombrement des appareils par niveau de fiabilite."""
        from .model import CONFIRME, PROBABLE, A_CONFIRMER
        rows = []
        tot = [0, 0, 0, 0]
        for t in tableaux:
            devs = layout(t)[0]
            n = len(devs)
            cnt = {CONFIRME: 0, PROBABLE: 0, A_CONFIRMER: 0}
            for d in devs:
                cnt[d.fiabilite] = cnt.get(d.fiabilite, 0) + 1
            a, b = fmap[t.code]
            rows.append([t.titre, "%d" % a if a == b else "%d à %d" % (a, b),
                         str(n), str(cnt[CONFIRME]), str(cnt[PROBABLE]),
                         str(cnt[A_CONFIRMER])])
            tot[0] += n
            tot[1] += cnt[CONFIRME]
            tot[2] += cnt[PROBABLE]
            tot[3] += cnt[A_CONFIRMER]
        rows.append(["TOTAL", "", str(tot[0]), str(tot[1]), str(tot[2]), str(tot[3])])
        return rows

    def sheet_names(self, tableaux, fmap):
        """Nom de chaque feuille, dans l'ordre de sortie."""
        names = ["Page de garde", "F01 Synoptique general",
                 "F02 Origine - comptage"]
        for t in tableaux:
            a, b = fmap[t.code]
            for i in range(b - a + 1):
                names.append("F%02d %s (%d-%d)" % (a + i, t.code, i + 1,
                                                   b - a + 1))
        names.append("F%02d Reserves" % self.n_folios)
        return names

    def build(self, tableaux, ensembles, reserves_items):
        self.count_folios(tableaux)
        fmap = self.folio_map(tableaux, 3)
        self.layout_names = self.sheet_names(tableaux, fmap)
        pages.cover(self.c, self, ensembles)
        pages.synoptique(self.c, self, self.folio, tableaux, fmap)
        self.folio += 1
        pages.origine(self.c, self, self.folio)
        self.folio += 1
        for t in tableaux:
            render.render_tableau(self.c, self, t)
        pages.reserves(self.c, self, self.folio, reserves_items,
                       self.synthese(tableaux, fmap))
        self.folio += 1
        if self.backend == "dxf":
            self.c.save(self.layout_names)
        else:
            self.c.save()
        return self.path
