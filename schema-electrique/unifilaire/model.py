# -*- coding: utf-8 -*-
"""Modele de donnees d'un tableau et calcul de mise en folio.

Un tableau est un arbre d'appareils. Chaque appareil occupe une colonne du
folio ; un appareil de groupe (interrupteur differentiel de tete, disjoncteur
general d'un groupe de departs) cree un jeu de barres fille sur lequel se
raccordent ses circuits terminaux.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from .style import BUS_Y, BUS_STAGGER, NCOLS

# fiabilite de la donnee relevee (cf. methode du releve photographique)
CONFIRME = "Confirmé"
PROBABLE = "Probable"
A_CONFIRMER = "À confirmer"


@dataclass
class Device:
    """Un appareil du tableau.

    kind : 'breaker'   disjoncteur
           'rcbo'      disjoncteur + bloc Vigi (ou disjoncteur differentiel)
           'switch'    interrupteur-sectionneur
           'rcd'       interrupteur differentiel
           'contactor' contacteur / telerupteur
           'aux'       appareil auxiliaire (telecommande BAES, relais...)
    """

    ref: str
    designation: str
    kind: str = "breaker"
    poles: int = 2
    lines: List[str] = field(default_factory=list)
    gamme: str = ""
    fiabilite: str = CONFIRME
    note: str = ""
    load: Optional[str] = None          # symbole d'utilisation en pied
    dashed_feed: bool = False           # liaison amont seulement probable
    bus_label: str = ""                 # libelle du jeu de barres aval
    children: List["Device"] = field(default_factory=list)

    # --- calcule au moment de la mise en folio
    col: int = -1
    page: int = -1
    x: float = 0.0
    bus_in: int = -1
    bus_out: int = -1

    @property
    def is_group(self) -> bool:
        return bool(self.children)


@dataclass
class Bus:
    """Jeu de barres : niveau, ordonnee, appareil source et etendue."""

    index: int
    level: int
    y: float
    source: Optional[Device]
    first_col: int
    last_col: int


@dataclass
class Tableau:
    """Un ensemble (tableau general ou divisionnaire)."""

    code: str
    titre: str
    meta: List[tuple] = field(default_factory=list)
    alimentation: str = ""
    arrivee: Optional[Device] = None
    circuits: List[Device] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    alerte: str = ""


# ------------------------------------------------------------------ layout

def layout(tab: Tableau):
    """Affecte colonnes, folios et jeux de barres a tous les appareils.

    Retourne (devices, buses, n_pages).
    """
    devices: List[Device] = []
    buses: List[Bus] = []
    stagger_count = {}

    def new_bus(level, source, col):
        # decalage alterne pour distinguer deux jeux de barres de meme niveau
        k = stagger_count.get(level, 0)
        stagger_count[level] = k + 1
        y = BUS_Y[min(level, len(BUS_Y) - 1)]
        if level >= 2:
            y -= BUS_STAGGER * (k % 2)
        b = Bus(len(buses), level, y, source, col, col)
        buses.append(b)
        return b

    def place(dev: Device, bus: Bus):
        dev.col = len(devices)
        dev.bus_in = bus.index
        devices.append(dev)
        bus.last_col = max(bus.last_col, dev.col)
        if dev.is_group:
            child = new_bus(bus.level + 1, dev, dev.col)
            dev.bus_out = child.index
            for ch in dev.children:
                place(ch, child)

    # jeu de barres principal : niveau 1, issu de l'arrivee
    if tab.arrivee is not None:
        main = new_bus(1, tab.arrivee, 0)
        tab.arrivee.col = -1            # l'arrivee occupe la colonne 0 aussi
        tab.arrivee.bus_out = main.index
        # l'arrivee consomme la premiere colonne du folio 1
        devices.append(tab.arrivee)
        tab.arrivee.col = 0
        main.first_col = 0
        main.last_col = 0
    else:
        main = new_bus(1, None, 0)

    for dev in tab.circuits:
        place(dev, main)

    for i, d in enumerate(devices):
        d.col = i
        d.page = i // NCOLS
    n_pages = max(1, (len(devices) + NCOLS - 1) // NCOLS)

    # etendue reelle des jeux de barres (au moins jusqu'a leur source)
    for b in buses:
        if b.source is not None:
            b.first_col = b.source.col
            b.last_col = max(b.last_col, b.source.col)
    return devices, buses, n_pages
