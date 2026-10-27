#!/usr/bin/env bash
# MotoNAV - prepara archivio vettoriale Lombardia.
# Richiede pmtiles CLI: https://docs.protomaps.com/pmtiles/cli
# Uso: ./tools/prepara-lombardia.sh https://build.protomaps.com/AAAAmmgg.pmtiles
# Il file sorgente va scelto tra i build realmente disponibili su https://maps.protomaps.com/builds
set -euo pipefail
SOURCE="${1:-}"
if [[ -z "$SOURCE" || "$SOURCE" != https://*.pmtiles ]]; then
  echo "Uso: $0 https://build.protomaps.com/AAAAmmgg.pmtiles" >&2
  exit 2
fi
command -v pmtiles >/dev/null || { echo "Installare pmtiles CLI" >&2; exit 2; }
mkdir -p dist
# Bounding box approssimativo con margine per l'intera Lombardia.
# Verificare confini e copertura prima della pubblicazione.
pmtiles extract "$SOURCE" dist/lombardia-z12.pmtiles --bbox=8.45,44.65,11.55,46.75 --maxzoom=12
pmtiles verify dist/lombardia-z12.pmtiles
pmtiles show dist/lombardia-z12.pmtiles --header-json
ls -lh dist/lombardia-z12.pmtiles
echo "Archivio generato: dist/lombardia-z12.pmtiles"
echo "Non pubblicare come mappa completa: maxzoom=12, rendering e test offline ancora necessari."
