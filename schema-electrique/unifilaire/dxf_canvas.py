# -*- coding: utf-8 -*-
"""Sortie CAO : un canvas compatible ReportLab qui ecrit du DXF.

`DxfCanvas` expose la meme API que `reportlab.pdfgen.canvas.Canvas` pour les
primitives utilisees par le generateur. Le code de trace (symbols, sheet,
render, pages) est donc rejoue tel quel et produit un dessin CAO coherent avec
le PDF, au lieu d'etre reecrit une seconde fois.

Conventions du fichier produit :
  * unites : millimetres (1 unite DXF = 1 mm), echelle 1:1 ;
  * les points PDF sont convertis en mm (25,4 / 72) ;
  * chaque folio est place dans l'espace objet sur une grille, et recoit une
    presentation (layout) A4 paysage avec sa fenetre a l'echelle 1:1 ;
  * les entites sont reparties par calques metier (voir LAYERS).
"""

import math

import ezdxf
from ezdxf.enums import TextEntityAlignment
from reportlab.pdfbase import pdfmetrics

PT_MM = 25.4 / 72.0          # 1 point PostScript en millimetres
PAGE_W_MM = 297.0            # A4 paysage
PAGE_H_MM = 210.0
GRID_COLS = 5                # folios par rangee dans l'espace objet
GAP_X = 20.0
GAP_Y = 20.0

# couleurs ACI
ACI_BLACK, ACI_RED, ACI_YELLOW, ACI_GREEN, ACI_BLUE, ACI_GREY = 7, 1, 2, 3, 5, 8
ACI_LGREY = 253

# calque : (couleur ACI, type de ligne, epaisseur 1/100 mm)
LAYERS = {
    "0": (ACI_BLACK, "CONTINUOUS", 25),
    "SCHEMA": (ACI_BLACK, "CONTINUOUS", 35),
    "SCHEMA_PROBABLE": (ACI_BLACK, "DASHED", 35),
    "SYMBOLES": (ACI_BLACK, "CONTINUOUS", 25),
    "TEXTE": (ACI_BLACK, "CONTINUOUS", 13),
    "TEXTE_A_CONFIRMER": (ACI_RED, "CONTINUOUS", 13),
    "TERRE": (ACI_GREEN, "CONTINUOUS", 50),
    "RENVOIS_FOLIO": (ACI_BLUE, "CONTINUOUS", 25),
    "CARTOUCHE": (ACI_BLACK, "CONTINUOUS", 25),
    "TABLEAU_CIRCUITS": (ACI_BLACK, "CONTINUOUS", 13),
    "TRAME": (ACI_LGREY, "CONTINUOUS", 9),
}

# styles de texte
STYLES = {
    "SCHEMA": "arial.ttf",
    "SCHEMA_GRAS": "arialbd.ttf",
    "SCHEMA_ITAL": "ariali.ttf",
}
FONT_STYLE = {
    "Helvetica": "SCHEMA",
    "Helvetica-Bold": "SCHEMA_GRAS",
    "Helvetica-Oblique": "SCHEMA_ITAL",
}

# epaisseurs de trait normalisees admises par le format DXF
LW_STEPS = [0, 5, 9, 13, 15, 18, 20, 25, 30, 35, 40, 50, 53, 60, 70, 80, 90, 100]


def _snap_lw(mm100):
    return min(LW_STEPS, key=lambda v: abs(v - mm100))


class _Path(object):
    """Chemin minimal compatible avec l'API `canvas.beginPath()`."""

    def __init__(self):
        self.pts = []

    def moveTo(self, x, y):
        self.pts.append((x, y))

    def lineTo(self, x, y):
        self.pts.append((x, y))

    def close(self):
        pass


class DxfCanvas(object):
    """Canvas d'ecriture DXF exposant l'API ReportLab utilisee par le tirage."""

    def __init__(self, path, pagesize=None):
        self.path = path
        self.doc = ezdxf.new("R2018", setup=True)
        self.doc.units = ezdxf.units.MM
        self.doc.header["$INSUNITS"] = ezdxf.units.MM
        self.doc.header["$MEASUREMENT"] = 1
        self.doc.header["$LTSCALE"] = 0.5      # echelle des types de ligne (mm)
        self.doc.header["$PSLTSCALE"] = 1
        self.msp = self.doc.modelspace()

        for name, font in STYLES.items():
            if name not in self.doc.styles:
                self.doc.styles.add(name, font=font)
        for name, (color, ltype, lw) in LAYERS.items():
            if name == "0":
                continue
            self.doc.layers.add(name, color=color, linetype=ltype,
                                lineweight=_snap_lw(lw))

        # etat graphique courant
        self._stroke = (0.0, 0.0, 0.0)
        self._fill = (0.0, 0.0, 0.0)
        self._lw = 0.9
        self._dash = None
        self._font = ("Helvetica", 7.0)
        self._layer = None            # calque impose par le code appelant

        self._page = 0
        self._ox = 0.0
        self._oy = 0.0
        self._page_origins = []
        self._set_page_origin()

    # ------------------------------------------------------- reperes de page
    def _set_page_origin(self):
        col = self._page % GRID_COLS
        row = self._page // GRID_COLS
        self._ox = col * (PAGE_W_MM + GAP_X)
        self._oy = -row * (PAGE_H_MM + GAP_Y)
        if len(self._page_origins) <= self._page:
            self._page_origins.append((self._ox, self._oy))

    def _p(self, x, y):
        """Point PDF (pt) -> point DXF (mm), dans le repere du folio courant."""
        return (self._ox + x * PT_MM, self._oy + y * PT_MM)

    # --------------------------------------------------------- etat graphique
    def set_layer(self, name):
        """Impose le calque des entites suivantes (None = deduction auto)."""
        self._layer = name if name in LAYERS else None

    def setStrokeColor(self, c):
        self._stroke = (c.red, c.green, c.blue)

    def setFillColor(self, c):
        self._fill = (c.red, c.green, c.blue)

    setStrokeColorRGB = setStrokeColor
    setFillColorRGB = setFillColor

    def setLineWidth(self, w):
        self._lw = w

    def setDash(self, *args):
        if not args or args[0] is None:
            self._dash = None
        elif isinstance(args[0], (list, tuple)):
            self._dash = tuple(args[0]) or None
        else:
            self._dash = tuple(a for a in args if isinstance(a, (int, float)))

    def setFont(self, name, size, leading=None):
        self._font = (name, size)

    def stringWidth(self, text, font, size):
        return pdfmetrics.stringWidth(text, font, size)

    def saveState(self):
        pass

    def restoreState(self):
        pass

    def setTitle(self, t):
        self.doc.header.custom_vars.append("TITRE", t[:250])

    def setAuthor(self, t):
        self.doc.header.custom_vars.append("AUTEUR", t[:250])

    def setSubject(self, t):
        self.doc.header.custom_vars.append("OBJET", t[:250])

    # ------------------------------------------------------ choix des calques
    def _is(self, rgb, ref, tol=0.18):
        return all(abs(a - b) < tol for a, b in zip(rgb, ref))

    def _line_layer(self):
        if self._layer:
            return self._layer
        c = self._stroke
        if self._is(c, (0.0588, 0.541, 0.184)) or self._is(c, (0.961, 0.894, 0.0)):
            return "TERRE"                       # vert ou jaune
        if self._is(c, (0.133, 0.133, 0.733)):
            return "RENVOIS_FOLIO"
        if self._is(c, (0.353, 0.353, 0.353)):
            return "TRAME"
        if self._dash and self._dash[0] >= 2.5:
            return "SCHEMA_PROBABLE"
        if self._lw <= 0.7:
            return "SYMBOLES"
        return "SCHEMA"

    def _text_layer(self):
        if self._layer:
            return self._layer
        if self._fill[0] > 0.55 and self._fill[1] < 0.35:
            return "TEXTE_A_CONFIRMER"
        return "TEXTE"

    def _attribs(self, layer=None):
        layer = layer or self._line_layer()
        att = {"layer": layer}
        if layer == "TERRE":
            att["color"] = (ACI_YELLOW if self._is(self._stroke, (0.961, 0.894, 0.0))
                            else ACI_GREEN)
        if layer in ("SCHEMA", "SYMBOLES", "SCHEMA_PROBABLE", "CARTOUCHE",
                     "TABLEAU_CIRCUITS"):
            att["lineweight"] = _snap_lw(self._lw * PT_MM * 100.0)
        if self._dash and layer != "SCHEMA_PROBABLE":
            att["linetype"] = "DASHED" if self._dash[0] >= 2.5 else "DOT"
        return att

    # -------------------------------------------------------------- primitives
    def line(self, x1, y1, x2, y2):
        self.msp.add_line(self._p(x1, y1), self._p(x2, y2), dxfattribs=self._attribs())

    def rect(self, x, y, w, h, stroke=1, fill=0):
        # les aplats de fond du PDF ne sont pas repris en CAO : ils masqueraient
        # le dessin. Les filets de colonnes assurent le meme reperage.
        if not stroke:
            return
        pts = [self._p(x, y), self._p(x + w, y), self._p(x + w, y + h),
               self._p(x, y + h)]
        self.msp.add_lwpolyline(pts, close=True, dxfattribs=self._attribs())

    def roundRect(self, x, y, w, h, r, stroke=1, fill=0):
        b = math.tan(math.pi / 8.0)      # fleche d'un arc a 90 degres
        s = PT_MM
        x0, y0 = self._ox + x * s, self._oy + y * s
        ww, hh, rr = w * s, h * s, r * s
        pts = [
            (x0 + rr, y0, 0, 0, 0), (x0 + ww - rr, y0, 0, 0, b),
            (x0 + ww, y0 + rr, 0, 0, 0), (x0 + ww, y0 + hh - rr, 0, 0, b),
            (x0 + ww - rr, y0 + hh, 0, 0, 0), (x0 + rr, y0 + hh, 0, 0, b),
            (x0, y0 + hh - rr, 0, 0, 0), (x0, y0 + rr, 0, 0, b),
        ]
        self.msp.add_lwpolyline(pts, format="xyseb", close=True,
                                dxfattribs=self._attribs())

    def circle(self, x, y, r, stroke=1, fill=0):
        if not stroke and fill:
            hatch = self.msp.add_hatch(color=ACI_BLACK,
                                       dxfattribs={"layer": self._line_layer()})
            hatch.paths.add_edge_path().add_arc(self._p(x, y), r * PT_MM, 0, 360)
            return
        self.msp.add_circle(self._p(x, y), r * PT_MM, dxfattribs=self._attribs())

    def ellipse(self, x1, y1, x2, y2, stroke=1, fill=0):
        cx, cy = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        a, b = abs(x2 - x1) / 2.0, abs(y2 - y1) / 2.0
        if a < b:
            a, b = b, a
            major = (0.0, a * PT_MM)
        else:
            major = (a * PT_MM, 0.0)
        ratio = (b / a) if a else 1.0
        self.msp.add_ellipse(self._p(cx, cy), major_axis=major, ratio=ratio,
                             dxfattribs=self._attribs())

    def arc(self, x1, y1, x2, y2, start, extent):
        cx, cy = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        r = abs(x2 - x1) / 2.0
        self.msp.add_arc(self._p(cx, cy), r * PT_MM, start, start + extent,
                         dxfattribs=self._attribs())

    def beginPath(self):
        return _Path()

    def drawPath(self, path, stroke=1, fill=0):
        pts = [self._p(x, y) for x, y in path.pts]
        if len(pts) < 2:
            return
        if fill:
            hatch = self.msp.add_hatch(
                color=ACI_BLACK, dxfattribs={"layer": self._line_layer()})
            hatch.paths.add_polyline_path(pts, is_closed=True)
        if stroke:
            self.msp.add_lwpolyline(pts, close=True, dxfattribs=self._attribs())

    # ------------------------------------------------------------------ textes
    def _text(self, x, y, s, align):
        if not s:
            return
        font, size = self._font
        style = FONT_STYLE.get(font, "SCHEMA")
        att = {"layer": self._text_layer(), "style": style,
               "height": size * PT_MM}
        if style == "SCHEMA_ITAL":
            att["oblique"] = 12.0
        t = self.msp.add_text(s, dxfattribs=att)
        t.set_placement(self._p(x, y), align=align)

    def drawString(self, x, y, s):
        self._text(x, y, s, TextEntityAlignment.LEFT)

    def drawCentredString(self, x, y, s):
        self._text(x, y, s, TextEntityAlignment.CENTER)

    def drawRightString(self, x, y, s):
        self._text(x, y, s, TextEntityAlignment.RIGHT)

    # ------------------------------------------------------------- pagination
    def showPage(self):
        self._page += 1
        self._set_page_origin()

    def _build_layouts(self, names=None):
        """Une presentation A4 paysage par folio, fenetre a l'echelle 1:1."""
        for i, (ox, oy) in enumerate(self._page_origins):
            label = names[i] if names and i < len(names) else "Folio %02d" % i
            name = "%02d - %s" % (i, label)
            name = name[:60].replace("/", "-")
            try:
                lay = self.doc.layouts.new(name)
            except Exception:
                continue
            lay.page_setup(size=(PAGE_W_MM, PAGE_H_MM), margins=(0, 0, 0, 0),
                           units="mm", scale=16)   # 16 = 1:1
            lay.add_viewport(
                center=(PAGE_W_MM / 2.0, PAGE_H_MM / 2.0),
                size=(PAGE_W_MM, PAGE_H_MM),
                view_center_point=(ox + PAGE_W_MM / 2.0, oy + PAGE_H_MM / 2.0),
                view_height=PAGE_H_MM)

    def save(self, layout_names=None):
        # le dernier showPage() a cree un folio vide : on le retire
        if self._page_origins and self._page == len(self._page_origins) - 1:
            self._page_origins.pop()
        self._build_layouts(layout_names)
        if "Layout1" in self.doc.layouts:
            self.doc.layouts.delete("Layout1")
        self.doc.saveas(self.path)
        return self.path

    def saveas_r12(self, path):
        """Variante DXF R12, lisible par tous les logiciels de CAO anciens."""
        self.doc.dxfversion = "AC1009"
        self.doc.saveas(path)
        self.doc.dxfversion = "AC1032"
        return path
