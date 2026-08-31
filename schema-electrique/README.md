# Schéma unifilaire — état existant

Générateur de schémas unifilaires **entièrement codé**, au format et au trait des
schémas Schneider Electric (eDesign / Ecodial) : folio A4 paysage, jeux de barres
horizontaux avec renvois de folio, symboles CEI 60617, barre de terre vert/jaune,
tableau des circuits en pied de folio et cartouche.

Le dossier est produit à partir du **relevé photographique des tableaux électriques
existants** (TGBT, tableaux divisionnaires, disjoncteur d'abonné et comptage Enedis).

## Générer le dossier

```bash
pip install -r requirements.txt
python3 generate_schema.py                  # PDF  -> out/…​.pdf
python3 generate_schema.py --format dxf     # DXF  -> out/…​.dxf   (CAO, 1:1 en mm)
python3 generate_schema.py --format dwg     # DWG  -> out/…​.dwg   (AutoCAD 2000+)
python3 generate_schema.py --format all     # les trois
```

Le tracé (symboles, gabarit, mise en folio, pagination) est entièrement calculé
par le code. Le PDF et le DXF sortent du **même code de tracé** : `DxfCanvas`
expose l'API de `reportlab.pdfgen.canvas`, si bien que le dessin n'est écrit
qu'une fois et rejoué vers l'un ou l'autre format — les deux fichiers ne peuvent
pas diverger.

### Sortie CAO (DXF / DWG)

Le DXF est en **millimètres, à l'échelle 1:1** ; un folio du PDF = une page A4
paysage (297 × 210 mm) dans le fichier CAO.

- **Espace objet** : les 27 folios sont posés sur une grille de 5 colonnes.
- **Présentations** : une présentation A4 paysage par folio, fenêtre à l'échelle
  1:1, prête à tracer.
- **Calques métier** : `SCHEMA`, `SCHEMA_PROBABLE` (liaisons en pointillé),
  `SYMBOLES`, `TEXTE`, `TEXTE_A_CONFIRMER` (rouge), `TERRE`, `RENVOIS_FOLIO`,
  `CARTOUCHE`, `TABLEAU_CIRCUITS`, `TRAME`. Chacun porte sa couleur, son type de
  ligne et son épaisseur : le rendu est correct dès l'ouverture, et les réserves
  du relevé s'isolent en éteignant un calque.
- Les aplats gris du PDF ne sont pas repris en CAO : ils masqueraient le dessin.

### Le cas du DWG

Le DWG est un **format propriétaire fermé** : aucune bibliothèque Python ne
l'écrit. `generate_schema.py --format dwg` produit donc le DXF puis le convertit
avec un outil externe, cherché automatiquement (variable `DWGWRITE`, puis PATH,
puis `tools/libredwg`) :

```bash
bash tools/build_libredwg.sh      # compile dwgwrite / dwgread (GNU LibreDWG)
python3 generate_schema.py --format dwg
```

L'ODA File Converter est également reconnu s'il est présent dans le PATH.

Le DWG livré est au format **AutoCAD 2000 (AC1015)**, lu par tous les AutoCAD
depuis 2000 et par la quasi-totalité des logiciels de CAO. Après conversion, le
script relit le DWG et compare les entités au DXF source ; la production
n'est annoncée réussie que si le contrôle passe.

> À défaut de convertisseur, le DXF reste directement exploitable : AutoCAD,
> BricsCAD, DraftSight, ZWCAD ou LibreCAD l'ouvrent tel quel, et un
> « Enregistrer sous → DWG » suffit à obtenir le DWG sans aucune perte.

## Contenu du dossier produit

| Folio | Contenu |
|-------|---------|
| — | Page de garde : affaire, caractéristiques générales, ensembles documentés, limites |
| 1 | Synoptique général — architecture reconstituée, avec renvois de folio |
| 2 | Origine — comptage Enedis (TC, ESSAILEC, Itron ACE6000, ACTIA) et disjoncteur d'abonné NS160N |
| 3 → 25 | Un jeu de folios par tableau : TGBT, TD entrepôt, TDS prises, TD rideaux, TD hangar, TD établi, TD baie informatique |
| 26 | Réserves, synthèse quantitative du relevé et consignes de dessin |

## Conventions de dessin

Le relevé est un **état existant** : il impose de distinguer ce qui est lu de ce
qui est déduit. Le générateur applique donc :

- **Trait plein** : liaison démontrée par le relevé.
- **Trait pointillé** : liaison seulement probable (position physique cohérente,
  câblage non visible) — typiquement D1-D5 sous DF1 dans le TGBT.
- **Texte rouge italique entre parenthèses** : donnée non confirmée.
- Ligne **« Fiabilité du relevé »** du tableau des circuits : `Confirmé`,
  `Probable` ou `À confirmer` pour chaque départ.
- Les lignes Section / Type / Longueur / Matière de câble restent vides : ces
  données ne sont pas relevables sur photographie.

## Organisation du code

```
generate_schema.py        point d'entrée : assemble le dossier (--format pdf|dxf|dwg|all)
data_installation.py      données du relevé (arbre d'appareils par tableau)
tools/build_libredwg.sh   compile le convertisseur DXF -> DWG
unifilaire/
  style.py                format de folio, gabarit, couleurs, niveaux de jeux de barres
  symbols.py              symboles CEI : disjoncteur, Vigi, interrupteur, tore, TC,
                          contacteur, onduleur, prise, moteur, barre PE, renvois de folio
  model.py                Device / Bus / Tableau + mise en folio (colonnes, pagination)
  sheet.py                gabarit : trame de colonnes, tableau des circuits, cartouche, légende
  render.py               tracé d'un tableau sur n folios
  pages.py                folios particuliers : garde, synoptique, origine, réserves
  document.py             assemblage et numérotation des folios
  dxf_canvas.py           sortie CAO : canvas compatible ReportLab écrivant du DXF
  dwg_export.py           conversion DXF -> DWG et contrôle d'aller-retour
```

### Modèle de données

Un tableau est un arbre. Un appareil qui porte des `children` devient un
**appareil de groupe** : il crée un jeu de barres fille sur lequel se raccordent
ses circuits terminaux. La mise en folio est automatique — 5 colonnes par folio,
les jeux de barres qui débordent sont prolongés par des renvois de folio
(triangles bleus numérotés).

```python
D("D1", "Général éclairage",
  ["Disjoncteur + Vigi C25 4P", "400 V — Vigi 300 mA"],
  poles=4, kind="rcbo", gamme="Schneider Acti9", fiab=CONFIRME,
  children=[
      D("D1.2", "Éclairage atelier zone 1", ["Disjoncteur C10 1P+N"],
        gamme="Schneider Acti9", fiab=PROBABLE, load="lamp"),
  ])
```

Types de symboles (`kind`) : `breaker`, `rcbo` (disjoncteur + Vigi), `switch`,
`rcd` (interrupteur différentiel), `contactor`, `ups`, `block` (répartiteur),
`aux` (appareil auxiliaire), `none` (aucun organe identifié).

Symboles d'utilisation (`load`) : `socket`, `lamp`, `motor`, `heater`, `ups`,
`panel` (tableau raccordé aux borniers).

### Ajouter ou corriger un appareil

Tout se modifie dans `data_installation.py` : ajouter un `D(...)` dans la liste
`circuits` du tableau concerné, ou dans les `children` d'un groupe. La
pagination, les renvois de folio, le tableau des circuits et la synthèse
quantitative se recalculent seuls.

## Limites

Document de relevé de l'état existant : ni étude de conformité, ni optimisation,
ni dossier de dimensionnement. Les calibres, sensibilités différentielles,
sections et Icc portés au schéma sont ceux lus sur les photographies ; les points
listés au folio 26 doivent être levés sur site avant tout schéma définitif.
