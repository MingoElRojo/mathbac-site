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
python3 generate_schema.py                 # -> out/Schema_Unifilaire_Etat_Existant.pdf
python3 generate_schema.py /tmp/autre.pdf  # chemin de sortie personnalisé
```

Aucune dépendance en dehors de ReportLab : tout le tracé (symboles, gabarit,
mise en folio, pagination) est calculé par le code.

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
generate_schema.py        point d'entrée : assemble le dossier
data_installation.py      données du relevé (arbre d'appareils par tableau)
unifilaire/
  style.py                format de folio, gabarit, couleurs, niveaux de jeux de barres
  symbols.py              symboles CEI : disjoncteur, Vigi, interrupteur, tore, TC,
                          contacteur, onduleur, prise, moteur, barre PE, renvois de folio
  model.py                Device / Bus / Tableau + mise en folio (colonnes, pagination)
  sheet.py                gabarit : trame de colonnes, tableau des circuits, cartouche, légende
  render.py               tracé d'un tableau sur n folios
  pages.py                folios particuliers : garde, synoptique, origine, réserves
  document.py             assemblage et numérotation des folios
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
