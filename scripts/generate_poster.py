"""Generate poster-grade illustrations via the Hugging Face Inference API.

Loads HF_TOKEN from .env, calls a text-to-image model, saves PNG to design/.

Examples
--------
    python scripts/generate_poster.py \\
        --prompt "Korean rural countryside, gouache illustration, rice plants, ..." \\
        --output design/poster_front.png \\
        --aspect landscape

    python scripts/generate_poster.py \\
        -p "warm village scene" -o design/test.png -m black-forest-labs/FLUX.1-schnell

Models that work well for poster illustration
---------------------------------------------
    black-forest-labs/FLUX.1-schnell   default, fastest, free
    black-forest-labs/FLUX.1-dev       higher fidelity (gated)
    stabilityai/stable-diffusion-xl-base-1.0
"""

from __future__ import annotations

import argparse
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
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-p", "--prompt", required=True, help="Text prompt for the illustration.")
    ap.add_argument("-o", "--output", required=True, type=Path, help="Output PNG path.")
    ap.add_argument("-m", "--model", default="black-forest-labs/FLUX.1-schnell",
                    help="HF model id (default: FLUX.1-schnell).")
    ap.add_argument("-a", "--aspect", choices=list(ASPECTS), default="landscape",
                    help="Preset aspect ratio.")
    ap.add_argument("--width", type=int, help="Override width (px).")
    ap.add_argument("--height", type=int, help="Override height (px).")
    ap.add_argument("--steps", type=int, default=4, help="Inference steps (FLUX.1-schnell: 1-4).")
    ap.add_argument("--guidance", type=float, default=0.0,
                    help="CFG scale (FLUX.1-schnell ignores; SDXL uses ~7.5).")
    ap.add_argument("--seed", type=int, help="Random seed for reproducibility.")
    ap.add_argument("--negative", default="", help="Negative prompt (SDXL only).")
    ap.add_argument("--provider", default="auto",
                    help="Inference provider: auto, hf-inference, fal-ai, replicate, together.")
    return ap.parse_args()


def main() -> int:
    args = parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    load_env(repo_root / ".env")

    token = os.environ.get("HF_TOKEN")
    if not token:
        print("ERROR: HF_TOKEN not set. Add it to .env or export it.", file=sys.stderr)
        return 2

    try:
        from huggingface_hub import InferenceClient
    except ImportError:
        print("ERROR: huggingface_hub not installed. Run: pip install 'huggingface_hub>=0.26'",
              file=sys.stderr)
        return 2

    width, height = ASPECTS[args.aspect]
    if args.width:
        width = args.width
    if args.height:
        height = args.height

    client = InferenceClient(token=token, provider=args.provider)

    kwargs = {"model": args.model, "width": width, "height": height,
              "num_inference_steps": args.steps, "guidance_scale": args.guidance}
    if args.seed is not None:
        kwargs["seed"] = args.seed
    if args.negative:
        kwargs["negative_prompt"] = args.negative

    print(f"[poster] model={args.model} size={width}x{height} steps={args.steps} "
          f"provider={args.provider}")
    image = client.text_to_image(args.prompt, **kwargs)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.output)
    print(f"[poster] saved -> {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
