#!/usr/bin/env bash
# Compile GNU LibreDWG (dwgwrite / dwgread) pour la conversion DXF -> DWG.
# Le DWG etant un format proprietaire ferme, aucune bibliotheque Python ne
# l'ecrit : un convertisseur externe est indispensable.
#
# Alternative : ODA File Converter (gratuit, inscription requise) —
# https://www.opendesign.com/guestfiles/oda_file_converter
set -euo pipefail

VERSION="${LIBREDWG_VERSION:-0.13.3}"
DEST="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/libredwg"
URL="https://github.com/LibreDWG/libredwg/releases/download/${VERSION}/libredwg-${VERSION}.tar.gz"

mkdir -p "$DEST"
cd "$DEST"

if [ ! -d "libredwg-${VERSION}" ]; then
  echo "Téléchargement de LibreDWG ${VERSION}..."
  curl -sSL -o "libredwg-${VERSION}.tar.gz" "$URL"
  tar xzf "libredwg-${VERSION}.tar.gz"
fi

cd "libredwg-${VERSION}"
# --disable-bindings evite la dependance a SWIG ; --enable-write active dwgwrite
[ -f Makefile ] || ./configure --disable-bindings --disable-python \
                               --disable-shared --enable-write
make -j"$(nproc 2>/dev/null || echo 2)"

echo
echo "Convertisseur compilé :"
echo "  $PWD/programs/dwgwrite"
echo "  $PWD/programs/dwgread"
echo
echo "Il est trouvé automatiquement par generate_schema.py --format dwg."
