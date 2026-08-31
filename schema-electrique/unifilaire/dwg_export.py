# -*- coding: utf-8 -*-
"""Conversion DXF -> DWG.

Le DWG est un format proprietaire fermé : aucune bibliotheque Python ne
l'ecrit. La conversion passe donc par un convertisseur externe, cherche dans
cet ordre :

  1. la variable d'environnement ``DWGWRITE`` ;
  2. ``dwgwrite`` (GNU LibreDWG) dans le PATH ;
  3. ``ODAFileConverter`` (ODA File Converter) dans le PATH ;
  4. une compilation locale sous ``tools/libredwg``.

``tools/build_libredwg.sh`` compile LibreDWG si aucun convertisseur n'est
disponible.
"""

import os
import shutil
import subprocess
import tempfile

import ezdxf

# LibreDWG ecrit de facon fiable jusqu'a R2000 ; ce format est lu par tous les
# AutoCAD depuis 2000 et par la quasi-totalite des logiciels de CAO.
DWG_VERSION = "r2000"
DXF_FOR_CONVERSION = "AC1015"      # DXF R2000, entree la plus sure du convertisseur

_LOCAL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "tools", "libredwg")


class ConverterNotFound(RuntimeError):
    """Aucun convertisseur DWG utilisable sur cette machine."""


def find_converter():
    """Retourne (chemin, type) du convertisseur, ou leve ConverterNotFound."""
    env = os.environ.get("DWGWRITE")
    if env and os.path.isfile(env) and os.access(env, os.X_OK):
        return env, "libredwg"
    for name in ("dwgwrite", "dxf2dwg"):
        p = shutil.which(name)
        if p:
            return p, "libredwg"
    for name in ("ODAFileConverter", "TeighaFileConverter"):
        p = shutil.which(name)
        if p:
            return p, "oda"
    for root, _dirs, files in os.walk(_LOCAL):
        if "dwgwrite" in files:
            p = os.path.join(root, "dwgwrite")
            if os.access(p, os.X_OK):
                return p, "libredwg"
    raise ConverterNotFound(
        "Aucun convertisseur DWG trouvé.\n"
        "  • compiler LibreDWG :  bash tools/build_libredwg.sh\n"
        "  • ou installer l'ODA File Converter, puis le placer dans le PATH\n"
        "  • ou définir DWGWRITE=/chemin/vers/dwgwrite\n"
        "Le fichier DXF produit reste ouvrable tel quel : AutoCAD l'ouvre et "
        "l'enregistre en DWG sans perte.")


def dxf_to_dwg(dxf_path, dwg_path, version=DWG_VERSION):
    """Convertit un DXF en DWG. Retourne le chemin du DWG produit."""
    exe, kind = find_converter()

    # LibreDWG lit le DXF R2000 de facon beaucoup plus sure que les versions
    # recentes : on lui presente toujours cette version intermediaire.
    doc = ezdxf.readfile(dxf_path)
    tmp = tempfile.NamedTemporaryFile(suffix=".dxf", delete=False)
    tmp.close()
    doc.dxfversion = DXF_FOR_CONVERSION
    doc.saveas(tmp.name)

    try:
        if kind == "libredwg":
            cmd = [exe, "--as", version, "-o", dwg_path, tmp.name]
        else:
            cmd = [exe, os.path.dirname(tmp.name) or ".",
                   os.path.dirname(dwg_path) or ".", "ACAD2000", "DWG", "0", "1"]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        if not os.path.isfile(dwg_path) or os.path.getsize(dwg_path) < 1024:
            raise RuntimeError(
                "La conversion DWG a échoué (%s).\n%s"
                % (exe, (res.stderr or res.stdout or "")[-800:]))
    finally:
        os.unlink(tmp.name)
    return dwg_path


def verify_dwg(dwg_path, reference_dxf):
    """Controle d'aller-retour : relit le DWG et compare au DXF de reference.

    Retourne un dict de comptages ; leve AssertionError si le DWG ne restitue
    pas la geometrie. Necessite ``dwgread`` (fourni avec LibreDWG).
    """
    exe = shutil.which("dwgread")
    if not exe:
        cand = None
        for root, _d, files in os.walk(_LOCAL):
            if "dwgread" in files:
                cand = os.path.join(root, "dwgread")
                break
        env = os.environ.get("DWGWRITE", "")
        if not cand and env:
            guess = os.path.join(os.path.dirname(env), "dwgread")
            cand = guess if os.path.isfile(guess) else None
        if not cand:
            return {"verifie": False, "motif": "dwgread indisponible"}
        exe = cand

    tmp = tempfile.NamedTemporaryFile(suffix=".dxf", delete=False)
    tmp.close()
    try:
        subprocess.run([exe, "-O", "DXF", "-o", tmp.name, dwg_path],
                       capture_output=True, timeout=900)
        src, back = ezdxf.readfile(reference_dxf), ezdxf.readfile(tmp.name)
    finally:
        os.unlink(tmp.name)

    def count(doc):
        out = {}
        for e in doc.modelspace():
            out[e.dxftype()] = out.get(e.dxftype(), 0) + 1
        return out

    a, b = count(src), count(back)
    assert a == b, "Le DWG ne restitue pas les mêmes entités : %s != %s" % (a, b)
    return {"verifie": True, "entites": sum(a.values()), "detail": a}
