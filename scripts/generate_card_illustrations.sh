#!/usr/bin/env bash
# Generate front/back illustration backgrounds + a poster-style hero illustration
# for the 동훈 / 청년마을 business card, using the reference Korean folk
# illustration aesthetic catalogued in prompts/card_illustrations.json.
#
# Requires:
#   - .env with HF_TOKEN
#   - pip install -e ".[poster]"
set -euo pipefail
cd "$(dirname "$0")/.."

python scripts/generate_from_catalog.py \
  card_front_bg \
  card_back_bg \
  village_scene

echo
echo "Generated:"
echo "  design/illust_card_front_bg.png"
echo "  design/illust_card_back_bg.png"
echo "  design/illust_village_scene.png"
echo
echo "Next: composite SVG text layers (design/card_dongheon_{front,back}.svg)"
echo "      over these PNGs in your design tool of choice."
