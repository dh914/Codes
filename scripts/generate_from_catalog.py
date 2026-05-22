"""Generate illustrations from prompts/card_illustrations.json.

Reads the prompt catalog, composes full prompts (style_token + subject), and
calls the HF Inference API for each requested key. Saves PNGs to design/.

Examples
--------
    # Generate all entries
    python scripts/generate_from_catalog.py --all

    # Generate specific entries
    python scripts/generate_from_catalog.py card_front_bg rice_planting_event

    # Override model / provider
    python scripts/generate_from_catalog.py --all -m black-forest-labs/FLUX.1-dev
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ASPECTS = {
    "landscape": (1280, 720),
    "portrait": (720, 1280),
    "square": (1024, 1024),
    "card_front": (1050, 600),
    "card_back": (1050, 600),
}

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "prompts" / "card_illustrations.json"
OUT_DIR = ROOT / "design"


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("keys", nargs="*", help="Catalog keys to generate (omit with --all).")
    ap.add_argument("--all", action="store_true", help="Generate every entry in the catalog.")
    ap.add_argument("-m", "--model", help="Override model id for all entries.")
    ap.add_argument("--provider", default="auto",
                    help="HF provider: auto / hf-inference / fal-ai / replicate / together.")
    ap.add_argument("--catalog", type=Path, default=CATALOG_PATH,
                    help=f"Path to prompts JSON (default: {CATALOG_PATH}).")
    return ap.parse_args()


def compose_prompt(style_token: str, subject: str) -> str:
    return f"{style_token}. Subject: {subject}."


def main() -> int:
    args = parse_args()
    load_env(ROOT / ".env")

    token = os.environ.get("HF_TOKEN")
    if not token:
        print("ERROR: HF_TOKEN not set. Add it to .env or export it.", file=sys.stderr)
        return 2

    try:
        from huggingface_hub import InferenceClient
    except ImportError:
        print("ERROR: huggingface_hub not installed. Run: pip install -e '.[poster]'",
              file=sys.stderr)
        return 2

    catalog = json.loads(args.catalog.read_text())
    meta = catalog.pop("_meta")
    style_token = meta["style_token"]
    negative = meta["negative_default"]

    keys = list(catalog.keys()) if args.all else args.keys
    if not keys:
        print("ERROR: pass catalog keys or --all. Available:",
              ", ".join(catalog.keys()), file=sys.stderr)
        return 2

    client = InferenceClient(token=token, provider=args.provider)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for key in keys:
        if key not in catalog:
            print(f"[skip] {key}: not in catalog")
            continue
        entry = catalog[key]
        width, height = ASPECTS[entry["aspect"]]
        model = args.model or entry["model"]
        prompt = compose_prompt(style_token, entry["subject"])
        kwargs = dict(model=model, width=width, height=height,
                      num_inference_steps=entry.get("steps", 4),
                      guidance_scale=entry.get("guidance", 0.0),
                      negative_prompt=negative)
        if "seed" in entry:
            kwargs["seed"] = entry["seed"]

        print(f"[{key}] model={model} size={width}x{height} steps={kwargs['num_inference_steps']}")
        image = client.text_to_image(prompt, **kwargs)
        out = OUT_DIR / f"illust_{key}.png"
        image.save(out)
        print(f"  -> {out}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
