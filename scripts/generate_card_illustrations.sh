#!/usr/bin/env bash
# Generate front/back illustration backgrounds for the 동훈 business card.
# Requires .env with HF_TOKEN and `pip install -e ".[poster]"`.
set -euo pipefail

cd "$(dirname "$0")/.."

FRONT_PROMPT="Korean rural countryside business card background illustration, horizontal landscape, warm gouache watercolor painting style on cream beige paper texture. Top-left and top-right corners decorated with rice plants: golden yellow rice grains, sage green leaves, hand-drawn soft style. Bottom edge: soft impressionistic Korean village silhouette with rolling hills, thatched-roof farmhouse, pine trees, distant misty mountains in muted olive green, mustard yellow, terracotta orange, sage green tones. Children's book illustration aesthetic, soft brushstrokes, cozy nostalgic warmth. NO TEXT, NO LETTERS, NO PEOPLE. Large empty cream space in the center for typography overlay. Flat poster illustration."

BACK_PROMPT="Korean rural village scene illustration for business card back, horizontal landscape, warm gouache watercolor on cream beige paper. Soft impressionistic landscape: rolling green hills, traditional thatched-roof Korean farmhouse, persimmon tree with orange fruits, pine trees, golden rice field in foreground, misty mountains in distance. Muted olive green, mustard yellow, terracotta orange, sage green palette. Children's book illustration style, soft hand-painted brushstrokes, cozy nostalgic warmth. NO TEXT, NO LETTERS, NO PEOPLE. Centered composition with breathing room. Flat poster illustration."

python scripts/generate_poster.py \
  --prompt "$FRONT_PROMPT" \
  --output design/card_dongheon_front_bg.png \
  --aspect card_front \
  --seed 214 \
  --steps 4

python scripts/generate_poster.py \
  --prompt "$BACK_PROMPT" \
  --output design/card_dongheon_back_bg.png \
  --aspect card_back \
  --seed 215 \
  --steps 4

echo "Done. Composite with SVG text overlays in design/card_dongheon_{front,back}.svg"
