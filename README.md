# Codes

데이터 사이언스 실험·분석·모델링을 위한 코드 컬렉션 레포지토리입니다.
재현 가능한(reproducible) 파이프라인을 기본으로, 노트북 탐색 → 모듈화 → 실험 추적의 흐름을 지원합니다.

## 프로젝트 구조

```
.
├── data/
│   ├── raw/          # 원본 데이터 (불변, git 미추적)
│   ├── processed/    # 학습용 가공 데이터 (git 미추적)
│   └── external/     # 외부 참조 데이터
├── notebooks/        # 탐색적 분석(EDA) 노트북
├── src/codes/
│   ├── data/         # 로딩·검증·분할
│   ├── features/     # 피처 엔지니어링
│   ├── models/       # 학습·평가·예측
│   └── visualization/# 시각화 유틸
├── tests/            # 단위 테스트
├── configs/          # 실험 설정 (YAML)
└── scripts/          # CLI 진입점
```

## 설치

```bash
pip install -e .
```

## 빠른 시작

```bash
python scripts/train.py --config configs/baseline.yaml
pytest
```

## 워크플로

1. `data/raw/`에 원본 데이터 배치
2. `notebooks/`에서 EDA 후, 안정화된 로직을 `src/codes/`로 이관
3. `configs/*.yaml`로 실험 정의 → `scripts/train.py` 실행
4. `tests/`로 핵심 로직 회귀 방지

## 포스터/일러스트 생성 (Hugging Face)

`scripts/generate_poster.py`는 Hugging Face Inference API로 포스터급 일러스트를 생성합니다.
기본 모델은 `black-forest-labs/FLUX.1-schnell` (무료·고속·고화질).

### 설치

```bash
pip install -e ".[poster]"
```

### 토큰 설정

`.env` 파일에 다음을 추가하거나 셸에 export:

```bash
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

토큰 발급: <https://huggingface.co/settings/tokens> (권한 Read)

### 단일 생성

```bash
python scripts/generate_poster.py \
  --prompt "Korean rural gouache illustration, rice plants, warm pastel" \
  --output design/poster.png \
  --aspect landscape
```

옵션:

| 옵션 | 설명 | 기본값 |
|---|---|---|
| `-p, --prompt` | 프롬프트 (필수) | — |
| `-o, --output` | 출력 PNG 경로 (필수) | — |
| `-m, --model` | HF 모델 ID | `black-forest-labs/FLUX.1-schnell` |
| `-a, --aspect` | `landscape` / `portrait` / `square` / `card_front` / `card_back` | `landscape` |
| `--width`, `--height` | 픽셀 직접 지정 (aspect 덮어씀) | aspect 프리셋 |
| `--steps` | 추론 스텝 (FLUX.1-schnell: 1~4) | `4` |
| `--seed` | 재현용 시드 | 랜덤 |
| `--provider` | `auto` / `hf-inference` / `fal-ai` / `replicate` / `together` | `auto` |

### 명함 일러스트 일괄 생성

```bash
./scripts/generate_card_illustrations.sh
```

→ `design/card_dongheon_{front,back}_bg.png` 생성. 이후 SVG 텍스트 레이어와 합성.

### 권장 모델

| 모델 | 용도 | 비고 |
|---|---|---|
| `black-forest-labs/FLUX.1-schnell` | 일반 포스터·일러스트 | 4 step, 무료 |
| `black-forest-labs/FLUX.1-dev` | 더 정교한 디테일 | gated, 토큰 권한 필요 |
| `black-forest-labs/FLUX.2-klein-9B` | 최신 (FLUX.2) | 큰 모델 |
| `stabilityai/stable-diffusion-xl-base-1.0` | 클래식 SDXL | guidance 7.5 권장 |
