# Compteur de légendes CFO / CFA

Comptage des occurrences de symboles et de libellés de légende sur un plan PDF
de courants forts / courants faibles, avec export CSV et DXF AutoCAD.

Tout le traitement a lieu dans le navigateur : aucun plan n'est transmis à un
serveur.

## Les trois cibles

| Fichier | Usage |
|---|---|
| `index.html` + `vendor/` | version servie par le site, à l'adresse `/outils/compteur-cfo-cfa/` |
| `../../dist/compteur-legendes-cfo-cfa.html` | fichier HTML unique de 1,5 Mo, tout embarqué : s'ouvre par double-clic, sans réseau. C'est la version à envoyer par courriel |
| `build/artifact.html` | corps de page seul, pour publication en artefact (non versionné) |

Les trois sont générées depuis une source unique :

```sh
node outils/compteur-cfo-cfa/build.mjs
```

`src/app.src.html` contient le jeton `<!--PDFJS_LOADER-->` que le script
remplace, selon la cible, par des balises `<script src>` vers `vendor/` ou par
pdf.js embarqué en ligne.

## Comment ça compte

**Libellés** — `getTextContent` de pdf.js donne la couche texte du PDF. Sur un
plan vectoriel, le comptage est alors exact. L'inventaire liste tous les
libellés du folio par fréquence.

**Symboles** — appariement de formes binaires :

1. rendu de la page, niveaux de gris, seuil d'Otsu → masque d'encre ;
2. masque dilaté en 3×3, pour tolérer un décalage d'un pixel ;
3. balayage à résolution réduite (facteur `F`), avec image intégrale pour
   écarter d'emblée les fenêtres dont la quantité d'encre est incompatible ;
4. affinage au pixel autour de chaque candidat, en deux passes — pas de `F/2`
   puis pas de 1. La fenêtre couvre ±2F : la suppression des non-maxima
   grossière peut retenir une cellule voisine de la bonne, et une fenêtre plus
   étroite rate alors la position exacte environ une fois sur deux ;
5. deux mesures renvoyées par candidat — le **rappel** (encre du gabarit
   retrouvée) et la **précision** (encre de la fenêtre expliquée par le
   gabarit). Le score final les combine côté interface, ce qui permet de régler
   le seuil sans relancer le calcul.

Le calcul tourne dans un *web worker*. Si le navigateur les refuse — pages
`file://` sur certaines configurations — le même code bascule sur le thread
principal.

## Limites connues

Deux symboles partageant leur contour dominant (un cercle, un carré) se
ressemblent beaucoup pour un appariement binaire. La courbe **stabilité du
comptage** rend la séparation visible : un palier large est un comptage
robuste. C'est au seuil de trancher, pas à l'outil de deviner.

## Tiers

pdf.js 3.11.174 (Mozilla, Apache 2.0) — voir `vendor/LICENSE-pdfjs`.
