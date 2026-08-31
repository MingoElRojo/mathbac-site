# -*- coding: utf-8 -*-
"""Donnees du releve photographique des tableaux electriques — etat existant.

Source : « Releve des tableaux electriques existants » (releve photographique).
Chaque appareil porte son niveau de fiabilite : Confirme / Probable / A confirmer.
Toute liaison seulement probable est marquee `dashed=True` et sera tracee en
pointille, conformement a la consigne de dessin du releve.
"""

from unifilaire.model import Device, Tableau, CONFIRME, PROBABLE, A_CONFIRMER

PROJET = "Relevé tableaux électriques — état existant"
VERSION = "1.0"
DATE = "31.08.2026"


def D(ref, designation, lines=(), poles=2, kind="breaker", gamme="",
      fiab=CONFIRME, load=None, dashed=False, bus_label="", children=()):
    return Device(ref=ref, designation=designation, kind=kind, poles=poles,
                  lines=list(lines), gamme=gamme, fiabilite=fiab, load=load,
                  dashed_feed=dashed, bus_label=bus_label,
                  children=list(children))


# =====================================================================
# 1. TGBT
# =====================================================================
_dpn = "Multi 9 DPN"

TGBT = Tableau(
    code="TGBT",
    titre="Tableau Général Basse Tension",
    meta=[
        ("Enveloppe", "Armoire modulaire ancienne, marque Merlin Gerin"),
        ("Rangées", "4 rangées utiles ; 1re rangée obturée"),
        ("Réseau", "Triphasé + neutre (probable)"),
        ("Icc", "À confirmer"),
        ("Régime de neutre", "À confirmer"),
        ("Parafoudre", "Aucun appareil identifiable"),
    ],
    notes=[
        "Disjoncteur général non intégré à l'enveloppe : Compact NS160N + Vigi MH déporté près du comptage (folio 2).",
        "Câblage interne non visible : aucune liaison interne n'est démontrée.",
    ],
    alerte=("Alerte de schéma — la répartition D1-D5 sous DF1, D7-D11 sous DF2 et D13-D17 sous DF3 "
            "est cohérente visuellement mais le câblage n'est pas visible. Ces liaisons sont tracées "
            "en pointillé et restent à confirmer sur site."),
    arrivee=D("Q0", "Arrivée depuis disjoncteur d'abonné", kind="none", poles=4,
              lines=["Arrivée TGBT — 3P+N", "Depuis Compact NS160N (folio 2)",
                     "(organe de coupure d'arrivée non identifié)"],
              gamme="Non identifié", fiab=A_CONFIRMER, dashed=True,
              bus_label="Jeu de barres TGBT — 3P+N — répartition interne non visible"),
    circuits=[
        D("X1", "Porte automatique", ["Disjoncteur C16 1P+N", "Schneider Electric",
                                      "(référence à confirmer)"],
          poles=2, gamme="Schneider Electric", fiab=PROBABLE, load="motor"),

        D("DF1", "Général éclairage", ["Interrupteur différentiel 4P 25 A",
                                       "Schneider Electric ID",
                                       "(IΔn et type illisibles)"],
          poles=4, kind="rcd", gamme="Schneider ID", fiab=PROBABLE, children=[
              D("D1", "Destination manuscrite illisible", [_dpn + " C10 1P+N", "(destination illisible)"],
                gamme=_dpn, fiab=A_CONFIRMER, dashed=True, load="lamp"),
              D("D2", "Vestiaire (probable)", [_dpn + " C10 1P+N", "(destination à confirmer)"],
                gamme=_dpn, fiab=A_CONFIRMER, dashed=True, load="lamp"),
              D("D3", "Extérieur (probable)", [_dpn + " C10 1P+N", "(destination à confirmer)"],
                gamme=_dpn, fiab=A_CONFIRMER, dashed=True, load="lamp"),
              D("D4", "Cuisine (probable)", [_dpn + " C10 1P+N", "(destination à confirmer)"],
                gamme=_dpn, fiab=A_CONFIRMER, dashed=True, load="lamp"),
              D("D5", "Destination non exploitable", [_dpn + " C10 1P+N", "(destination illisible)"],
                gamme=_dpn, fiab=A_CONFIRMER, dashed=True, load="lamp"),
          ]),

        D("DF2", "Général PC 1", ["Interrupteur différentiel 4P",
                                  "Schneider Electric",
                                  "(calibre, IΔn et type à confirmer)"],
          poles=4, kind="rcd", gamme="Schneider ID", fiab=A_CONFIRMER, children=[
              D("D7", "Prises de courant", [_dpn + " 1P+N", "(calibre illisible)"],
                gamme=_dpn, fiab=A_CONFIRMER, dashed=True, load="socket"),
              D("D8", "Prises de courant", [_dpn + " 1P+N", "(calibre illisible)"],
                gamme=_dpn, fiab=A_CONFIRMER, dashed=True, load="socket"),
              D("D9", "Prises de courant", [_dpn + " 1P+N", "(calibre illisible)"],
                gamme=_dpn, fiab=A_CONFIRMER, dashed=True, load="socket"),
              D("D10", "Prise cuisine (probable)", [_dpn + " 1P+N", "(calibre illisible)"],
                gamme=_dpn, fiab=A_CONFIRMER, dashed=True, load="socket"),
              D("D11", "Destination partiellement lisible", [_dpn + " 1P+N", "(calibre illisible)"],
                gamme=_dpn, fiab=A_CONFIRMER, dashed=True, load="socket"),
          ]),

        D("DF3", "Général PC 2", ["Interrupteur différentiel 4P 40 A",
                                  "Schneider Electric",
                                  "(calibre, IΔn et type à confirmer)"],
          poles=4, kind="rcd", gamme="Schneider ID", fiab=A_CONFIRMER, children=[
              D("D13", "Prises de courant", [_dpn + " 1P+N", "(calibre illisible)"],
                gamme=_dpn, fiab=A_CONFIRMER, dashed=True, load="socket"),
              D("D14", "Prises de courant", [_dpn + " 1P+N", "(calibre illisible)"],
                gamme=_dpn, fiab=A_CONFIRMER, dashed=True, load="socket"),
              D("D15", "Prises de courant", [_dpn + " 1P+N", "(calibre illisible)"],
                gamme=_dpn, fiab=A_CONFIRMER, dashed=True, load="socket"),
              D("D16", "Prises de courant", [_dpn + " 1P+N", "(calibre illisible)"],
                gamme=_dpn, fiab=A_CONFIRMER, dashed=True, load="socket"),
              D("D17", "Prises de courant", [_dpn + " 1P+N", "(calibre illisible)"],
                gamme=_dpn, fiab=A_CONFIRMER, dashed=True, load="socket"),
          ]),

        D("Q1", "Magasin / Atelier", ["Disjoncteur C50 4P", "Schneider Electric",
                                      "(destination aval à confirmer)"],
          poles=4, gamme="Schneider Electric", fiab=PROBABLE, load="panel"),
        D("KM1", "Cumulus", ["Contacteur ~2 modules", "Merlin Gerin (probable)",
                             "(fonction exacte à confirmer)"],
          poles=2, kind="contactor", gamme="Merlin Gerin", fiab=A_CONFIRMER, load="heater"),
        D("Q2", "Bornes IRVE", ["Disjoncteur C32 4P", "Schneider Electric",
                                "(protection différentielle dédiée non identifiée)"],
          poles=4, gamme="Schneider Electric", fiab=PROBABLE, load="panel"),
        D("X2", "Appareil adjacent IRVE", ["Appareil modulaire 1 module",
                                           "Merlin Gerin", "(fonction non identifiée)"],
          poles=1, kind="aux", gamme="Merlin Gerin", fiab=A_CONFIRMER),
        D("T1", "Vestiaire / salle de formation", ["Disjoncteur différentiel C16",
                                                   "1P+N ou 2P — bouton test apparent",
                                                   "(IΔn à confirmer)"],
          poles=2, kind="rcbo", gamme="Schneider Electric", fiab=PROBABLE, load="panel"),
        D("D19", "Destination à confirmer", ["Disjoncteur 4P", "Merlin Gerin",
                                             "(calibre illisible)"],
          poles=4, gamme="Merlin Gerin", fiab=A_CONFIRMER),
        D("X3", "Télécommande BAES", ["Luminox TLU", "2 boutons de commande",
                                      "(alimentation à confirmer)"],
          poles=1, kind="aux", gamme="Luminox TLU", fiab=A_CONFIRMER),
        D("Q3", "Abri à véhicules", ["Disjoncteur 4P", "Merlin Gerin",
                                     "(calibre et référence à confirmer)"],
          poles=4, gamme="Merlin Gerin", fiab=A_CONFIRMER, load="panel"),
        D("Q4", "Salle de réunion", ["Disjoncteur C32 4P", "Legrand",
                                     "(pouvoir de coupure à confirmer)"],
          poles=4, gamme="Legrand", fiab=PROBABLE, load="panel"),
        D("Q5", "Général panneaux droite — salle de formation",
          ["Disjoncteur C63 4P", "Schneider Electric", "(référence à confirmer)"],
          poles=4, gamme="Schneider Electric", fiab=PROBABLE, load="panel"),
        D("DF4", "Destination non démontrée", ["Interrupteur différentiel 4P",
                                               "30 mA apparent — Merlin Gerin",
                                               "(calibre illisible, aval inconnu)"],
          poles=4, kind="rcd", gamme="Merlin Gerin", fiab=A_CONFIRMER),
    ],
)


# =====================================================================
# 2. TD entrepot - batiment annexe
# =====================================================================
TD_ENTREPOT = Tableau(
    code="TD ENTREPÔT",
    titre="TD entrepôt — bâtiment annexe",
    meta=[
        ("Enveloppe", "Armoire Schneider récente, 3 rangées utiles"),
        ("Réseau", "Triphasé + neutre"),
        ("Répartiteur", "Schneider Linergy Distribution Block"),
        ("Coupure locale", "IG 4P 63 A (Acti9 iSW-NA)"),
        ("Repérage", "Étiquettes détaillées"),
    ],
    notes=[
        "D0 (auxiliaires) est raccordé en amont de l'interrupteur général : il reste sous tension après ouverture de l'IG.",
        "Accessoire MX + contact auxiliaire OF associés à l'IG ; référence illisible.",
    ],
    arrivee=D("Q0", "Arrivée entrepôt", kind="none", poles=4,
              lines=["Arrivée depuis le TGBT", "3P+N",
                     "(section et protection amont à confirmer)"],
              gamme="—", fiab=A_CONFIRMER, dashed=True),
    circuits=[
        D("D0", "Auxiliaires — amont général", ["Disjoncteur + Vigi C10", "Vigi 30 mA — Acti9",
                                                "(alimenté en amont de l'IG)"],
          poles=2, kind="rcbo", gamme="Schneider Acti9", fiab=CONFIRME),
        D("IG", "Interrupteur général tableau", ["Acti9 iSW-NA 4P 63 A", "415 V — MX + OF associés"],
          poles=4, kind="switch", gamme="Acti9 iSW-NA", fiab=CONFIRME,
          bus_label="Répartiteur Schneider Linergy — 3P+N", children=[
              D("D1", "Général éclairage", ["Disjoncteur + Vigi C25 4P", "400 V — Vigi 300 mA"],
                poles=4, kind="rcbo", gamme="Schneider Acti9", fiab=CONFIRME, children=[
                    D("D1.2", "Éclairage atelier zone 1", ["Disjoncteur C10 1P+N"],
                      gamme="Schneider Acti9", fiab=PROBABLE, load="lamp"),
                    D("D1.3", "Éclairage atelier / BAES zone 2", ["Disjoncteur C10 1P+N"],
                      gamme="Schneider Acti9", fiab=PROBABLE, load="lamp"),
                ]),
              D("D2", "Général prises de courant entrepôt", ["Disjoncteur + Vigi C25 4P",
                                                             "400 V — Vigi 30 mA"],
                poles=4, kind="rcbo", gamme="Schneider Acti9", fiab=CONFIRME, children=[
                    D("D2.1", "Prises de courant entrepôt", ["Disjoncteur C16 1P+N"],
                      gamme="Schneider Acti9", fiab=PROBABLE, load="socket"),
                    D("D2.2", "Prises de courant entrepôt", ["Disjoncteur C16 1P+N"],
                      gamme="Schneider Acti9", fiab=PROBABLE, load="socket"),
                    D("D2.3", "Prises de courant entrepôt", ["Disjoncteur C16 1P+N"],
                      gamme="Schneider Acti9", fiab=PROBABLE, load="socket"),
                ]),
              D("D3", "Général divers", ["Disjoncteur + Vigi C40 4P", "400 V — Vigi 300 mA"],
                poles=4, kind="rcbo", gamme="Schneider Acti9", fiab=CONFIRME, children=[
                    D("D3.1", "Porte sectionnelle", ["Disjoncteur C16 4P", "400 V"],
                      poles=4, gamme="Schneider Acti9", fiab=CONFIRME, load="motor"),
                    D("D3.2", "Alimentation Fenwick", ["Disjoncteur C16 4P", "400 V"],
                      poles=4, gamme="Schneider Acti9", fiab=CONFIRME, load="socket"),
                    D("D3.3", "Éclairage extérieur", ["Disjoncteur C10 1P+N"],
                      gamme="Schneider Acti9", fiab=PROBABLE, load="lamp"),
                    D("D3.4", "Alimentation portail", ["Disjoncteur C16 1P+N"],
                      gamme="Schneider Acti9", fiab=PROBABLE, load="motor"),
                    D("D3.5", "Porte Sud (mention manuscrite)", ["Disjoncteur C10 1P+N",
                                                                 "(destination à confirmer)"],
                      gamme="Schneider Acti9", fiab=A_CONFIRMER, load="motor"),
                ]),
              D("D4", "Coffret prises atelier", ["Disjoncteur C40 4P", "400 V",
                                                 "(référence à confirmer)"],
                poles=4, gamme="Schneider Acti9", fiab=PROBABLE, load="panel"),
          ]),
        D("TBS", "Télécommande BAES", ["Eaton TL 500", "2 boutons et voyants",
                                       "(alimentation à confirmer)"],
          poles=1, kind="aux", gamme="Eaton TL 500", fiab=A_CONFIRMER),
    ],
)


# =====================================================================
# 3. TDS prises entrepot - batiment annexe
# =====================================================================
TDS_PRISES = Tableau(
    code="TDS PRISES",
    titre="TDS prises entrepôt — bâtiment annexe",
    meta=[
        ("Enveloppe", "Coffret étanche à porte transparente, 1 rangée"),
        ("Appareillage", "Schneider Electric Acti9"),
        ("Départs", "3 circuits de prises"),
        ("Répartition", "Répartition L1/L2/L3 possible, non visible"),
    ],
    notes=["Protection amont du coffret non visible : arrivée tracée en pointillé."],
    arrivee=D("Q0", "Arrivée TDS prises", kind="none", poles=4,
              lines=["Arrivée 3P+N (probable)", "(origine et protection amont à confirmer)"],
              gamme="—", fiab=A_CONFIRMER, dashed=True),
    circuits=[
        D("ID1", "Général prises", ["Acti9 iID 4P 40 A", "400 V — 30 mA type AC"],
          poles=4, kind="rcd", gamme="Acti9 iID", fiab=CONFIRME, children=[
              D("D1", "PC1 — prise sous capot IP65", ["Acti9 iC40N — A9P54616", "C16 — 230 V"],
                gamme="Acti9 iC40N", fiab=CONFIRME, load="socket"),
              D("D2", "PC2 — prise industrielle 16 A", ["Acti9 iC40N — A9P54616", "C16 — 230 V",
                                                        "Prise PKY16F423 — IP44"],
                gamme="Acti9 iC40N", fiab=CONFIRME, load="socket"),
              D("D3", "PC3 — prise industrielle 32 A", ["Acti9 iC40N — A9P54632", "C32 — 230 V",
                                                        "Prise PKY32F423 — IP44"],
                gamme="Acti9 iC40N", fiab=CONFIRME, load="socket"),
          ]),
    ],
)


# =====================================================================
# 4. TD rideaux hangar - batiment annexe
# =====================================================================
TD_RIDEAUX = Tableau(
    code="TD RIDEAUX",
    titre="TD rideaux hangar — bâtiment annexe",
    meta=[
        ("Enveloppe", "Coffret étanche gris, porte transparente, 2 rangées"),
        ("Alimentation", "Triphasée (probable)"),
        ("Coupure générale", "Non visible dans le coffret"),
        ("Répartiteur", "Legrand 048 88 — 125 A / 400 V"),
    ],
    notes=[
        "Le répartiteur Legrand alimente probablement les trois départs D10 + Vigi 300 mA.",
        "Protection amont du coffret non visible.",
    ],
    arrivee=D("RP", "Répartiteur Legrand 048 88", kind="block", poles=4,
              lines=["Bloc de répartition 4P 125 A", "400 V — Ui 500 V — Uimp 14,5 kV",
                     "(protection amont non visible)"],
              gamme="Legrand 048 88", fiab=PROBABLE, dashed=True),
    circuits=[
        D("Q1", "Rideaux 1 et 2", ["Acti9 iDT40N D10 4P", "400 V — 6 kA (probable)",
                                   "Vigi 300 mA"],
          poles=4, kind="rcbo", gamme="Acti9 iDT40N", fiab=PROBABLE, load="motor"),
        D("Q2", "Rideaux 3 et 4", ["Acti9 iDT40N D10 4P", "400 V — 6 kA (probable)",
                                   "Vigi 300 mA"],
          poles=4, kind="rcbo", gamme="Acti9 iDT40N", fiab=PROBABLE, load="motor"),
        D("Q3", "Rideaux 5 et 6", ["Acti9 iDT40N D10 4P", "400 V — 6 kA (probable)",
                                   "Vigi 300 mA"],
          poles=4, kind="rcbo", gamme="Acti9 iDT40N", fiab=PROBABLE, load="motor"),
    ],
)


# =====================================================================
# 5. TD hangar - batiment annexe
# =====================================================================
_mg = "Merlin Gerin Multi 9"

TD_HANGAR = Tableau(
    code="TD HANGAR",
    titre="TD hangar — bâtiment annexe",
    meta=[
        ("Enveloppe", "Grande armoire métallique ancienne"),
        ("Rangées", "3 rangées actives"),
        ("Fabricants", "Schneider, Merlin Gerin, Finder, non identifiés"),
        ("Réseau", "Triphasé + neutre (probable)"),
        ("Appareil général", "Aucun appareil unique identifié"),
        ("Parafoudre", "Aucun identifiable"),
    ],
    notes=[
        "Aucun organe de coupure générale n'est identifié : l'arrivée est tracée en pointillé.",
        "L'affectation des circuits terminaux aux quatre généraux n'est pas démontrée par le relevé.",
    ],
    alerte=("Alerte de schéma — le rattachement des circuits terminaux aux appareils généraux "
            "(éclairage, prises, rideau) est déduit du repérage visible et non du câblage : "
            "toutes ces liaisons sont tracées en pointillé et restent à confirmer."),
    arrivee=D("Q0", "Arrivée TD hangar", kind="none", poles=4,
              lines=["Arrivée 3P+N (probable)", "(aucun appareil général identifié)",
                     "(origine et protection amont à confirmer)"],
              gamme="—", fiab=A_CONFIRMER, dashed=True),
    circuits=[
        D("Q1", "Général éclairage", ["Schneider Acti9 — DJ + Vigi", "C16 4P — 400 V",
                                      "Vigi 300 mA"],
          poles=4, kind="rcbo", gamme="Schneider Acti9", fiab=PROBABLE, children=[
              D("D1", "Détecteur / éclairage", [_mg + " Déclic", "C10 1P+N — 230 V"],
                gamme=_mg + " Déclic", fiab=PROBABLE, dashed=True, load="lamp"),
              D("D2", "Éclairage radar", [_mg + " DPN", "C10 1P+N"],
                gamme=_mg + " DPN", fiab=PROBABLE, dashed=True, load="lamp"),
              D("D3", "Éclairage radar", [_mg + " DPN", "C10 1P+N"],
                gamme=_mg + " DPN", fiab=PROBABLE, dashed=True, load="lamp"),
              D("D4", "Éclairage radar", [_mg + " DPN", "C10 1P+N"],
                gamme=_mg + " DPN", fiab=PROBABLE, dashed=True, load="lamp"),
              D("K1", "Relais H.G / H.D / H.?", ["Finder série 55.32 — 3 relais",
                                                 "Bobines 230 V AC (probables)",
                                                 "(fonction exacte à confirmer)"],
                poles=1, kind="aux", gamme="Finder 55.32", fiab=A_CONFIRMER, dashed=True),
              D("K2", "Relais / télérupteur", ["Module étroit — marque masquée",
                                               "230 V — 16 A apparents",
                                               "(fonction à confirmer)"],
                poles=1, kind="aux", gamme="Non identifié", fiab=A_CONFIRMER, dashed=True),
              D("K3", "Minuteries / temporisateurs", ["2 modules transparents",
                                                      "(marque et fonctions à confirmer)"],
                poles=1, kind="aux", gamme="Non identifié", fiab=A_CONFIRMER, dashed=True),
          ]),
        D("Q2", "Général prises", ["Schneider Acti9 — DJ + Vigi", "C32 4P — 400 V",
                                   "Vigi 30 mA"],
          poles=4, kind="rcbo", gamme="Schneider Acti9", fiab=PROBABLE, children=[
              D("D5", "PC 220 V", ["Schneider Electric", "C20 1P+N"],
                gamme="Schneider Electric", fiab=PROBABLE, dashed=True, load="socket"),
              D("D6", "PC 220 V", ["Schneider Electric", "C20 1P+N"],
                gamme="Schneider Electric", fiab=PROBABLE, dashed=True, load="socket"),
              D("D7", "PC 220 V", ["Schneider Electric", "C20 1P+N"],
                gamme="Schneider Electric", fiab=PROBABLE, dashed=True, load="socket"),
              D("D8", "PC1", ["Schneider Acti9", "C20 1P+N"],
                gamme="Schneider Acti9", fiab=PROBABLE, dashed=True, load="socket"),
              D("D9", "PC2", ["Schneider Acti9", "C20 1P+N"],
                gamme="Schneider Acti9", fiab=PROBABLE, dashed=True, load="socket"),
              D("D10", "PC3", ["Schneider Acti9", "C20 1P+N"],
                gamme="Schneider Acti9", fiab=PROBABLE, dashed=True, load="socket"),
              D("D11", "PC4", ["Schneider Acti9", "C20 1P+N"],
                gamme="Schneider Acti9", fiab=PROBABLE, dashed=True, load="socket"),
              D("D12", "PC5", ["Schneider Acti9", "C20 1P+N"],
                gamme="Schneider Acti9", fiab=PROBABLE, dashed=True, load="socket"),
              D("D13", "PC6", [_mg, "C20 1P+N"],
                gamme=_mg, fiab=PROBABLE, dashed=True, load="socket"),
          ]),
        D("Q3", "Général rideau", ["Schneider Acti9", "C20 4P — 400 V",
                                   "6 kA (probable)"],
          poles=4, gamme="Schneider Acti9", fiab=PROBABLE, load="motor"),
        D("Q4", "PC 32 A", ["Schneider Acti9 — DJ + Vigi", "C32 — Vigi 30 mA",
                            "(nombre de pôles à confirmer)"],
          poles=4, kind="rcbo", gamme="Schneider Acti9", fiab=A_CONFIRMER, load="socket"),
        D("Q5", "Cumulus", [_mg + " C60N", "C20 4P — 400 V", "6 kA apparent"],
          poles=4, gamme=_mg + " C60N", fiab=PROBABLE, load="heater"),
        D("Q6", "PC 380 V", [_mg + " C60N", "C20 4P"],
          poles=4, gamme=_mg + " C60N", fiab=PROBABLE, load="socket"),
        D("Q7", "PC 380 V", [_mg + " C60N", "C20 4P"],
          poles=4, gamme=_mg + " C60N", fiab=PROBABLE, load="socket"),
        D("Q8", "PC 380 V", [_mg + " C60N", "C20 4P"],
          poles=4, gamme=_mg + " C60N", fiab=PROBABLE, load="socket"),
    ],
)


# =====================================================================
# 6. TD etabli
# =====================================================================
TD_ETABLI = Tableau(
    code="TD ÉTABLI",
    titre="TD établi — « COFFRET ÉTABLI »",
    meta=[
        ("Enveloppe", "Coffret modulaire blanc Schneider, 1 rangée"),
        ("Réseau", "Triphasé — circuits tri et mono"),
        ("Différentiel", "Aucun différentiel visible dans le coffret"),
        ("Coupure locale", "Non visible"),
    ],
    notes=["Origine, protection amont et protection différentielle du TD établi à confirmer."],
    arrivee=D("Q0", "Arrivée coffret établi", kind="none", poles=4,
              lines=["Arrivée 3P+N (probable)",
                     "(protection amont et protection différentielle à confirmer)"],
              gamme="—", fiab=A_CONFIRMER, dashed=True),
    circuits=[
        D("Q1", "PC triphasée", ["Acti9 iDT40T — A9P22720", "C20 3P — 400 V — 4,5 kA"],
          poles=3, gamme="Acti9 iDT40T", fiab=CONFIRME, load="socket"),
        D("Q2", "Colonne", ["Acti9 iDT40T — A9P22306", "C6 3P — 400 V — 4,5 kA"],
          poles=3, gamme="Acti9 iDT40T", fiab=CONFIRME, load="motor"),
        D("Q3", "PC monophasée", ["Acti9 iDT40T — A9P22616", "C16 1P+N — 230 V — 4,5 kA"],
          poles=2, gamme="Acti9 iDT40T", fiab=CONFIRME, load="socket"),
        D("Q4", "Éclairage", ["Acti9 iDT40T — A9P22610", "C10 1P+N — 230 V — 4,5 kA"],
          poles=2, gamme="Acti9 iDT40T", fiab=CONFIRME, load="lamp"),
        D("Q5", "Touret", ["Acti9 iDT40T — A9P22604", "C4 1P+N — 230 V — 4,5 kA"],
          poles=2, gamme="Acti9 iDT40T", fiab=CONFIRME, load="motor"),
    ],
)


# =====================================================================
# 7. TD 138601-ELE-ARDV-0003 - baie informatique + onduleur
# =====================================================================
TD_BAIE = Tableau(
    code="TD BAIE INFO",
    titre="TD 138601-ELE-ARDV-0003 — baie informatique + onduleur",
    meta=[
        ("Enveloppe", "Armoire métallique murale"),
        ("Installateur", "BD Bobineau"),
        ("Zones", "Circuits normaux et circuits ondulés"),
        ("Réseau", "Monophasé 230 V (2P apparents)"),
    ],
    notes=["Séparation exacte normal / ondulé à confirmer.",
           "Plaque signalétique et puissance de l'onduleur non relevées."],
    alerte=("Sécurité — les circuits ondulés peuvent rester sous tension après coupure du "
            "général du coffret. Consigner et vérifier avant toute intervention."),
    arrivee=D("Q0", "Arrivée baie informatique", kind="none", poles=2,
              lines=["Arrivée 230 V (probable)", "(origine et protection amont à confirmer)"],
              gamme="—", fiab=A_CONFIRMER, dashed=True),
    circuits=[
        D("ID1", "Général armoire", ["Schneider Electric ID K", "2P — 40 A — 30 mA"],
          poles=2, kind="rcd", gamme="Schneider ID K", fiab=PROBABLE, children=[
              D("D1", "Intrusion / chargeur", [_mg + " C60N", "C3 2P (apparent)"],
                gamme=_mg + " C60N", fiab=PROBABLE),
              D("D2", "Autocom / téléphone", [_mg, "2P — (calibre illisible)"],
                gamme=_mg, fiab=A_CONFIRMER),
              D("D3", "Réserve", [_mg + " C60N", "C6 2P (apparent)"],
                gamme=_mg + " C60N", fiab=PROBABLE),
              D("D4", "Chargeur", [_mg + " C60N", "C16 2P"],
                gamme=_mg + " C60N", fiab=PROBABLE),
              D("D5", "Modem", [_mg + " C60", "C10 2P"],
                gamme=_mg + " C60", fiab=PROBABLE),
              D("D6", "Coffret PC onduleur", [_mg, "C16 2P"],
                gamme=_mg, fiab=PROBABLE, load="ups"),
          ]),
        D("X1", "Onduleur + bypass", ["Onduleur externe — modèle illisible",
                                      "Sortie max visible 10 A",
                                      "(puissance et fabricant à confirmer)"],
          poles=2, kind="ups", gamme="Non identifié", fiab=A_CONFIRMER,
          bus_label="Circuits ondulés — sous tension après coupure du général coffret",
          children=[
              D("D7", "Réserve ondulée", [_mg + " C60N", "C25 2P (apparent)"],
                gamme=_mg + " C60N", fiab=PROBABLE, dashed=True),
              D("D8", "Baie de brassage — départ ondulé", ["Merlin Gerin DPN N Vigi",
                                                           "1P+N ou 2P",
                                                           "(calibre et IΔn à confirmer)"],
                kind="rcbo", gamme="Merlin Gerin DPN N Vigi", fiab=A_CONFIRMER, dashed=True),
              D("D9", "Baie PC — normal", ["Schneider Acti9 — DJ + Vigi", "C16 1P+N",
                                           "Vigi 30 mA (apparent)"],
                kind="rcbo", gamme="Schneider Acti9", fiab=PROBABLE, dashed=True, load="socket"),
          ]),
    ],
)


TABLEAUX = [TGBT, TD_ENTREPOT, TDS_PRISES, TD_RIDEAUX, TD_HANGAR, TD_ETABLI, TD_BAIE]
