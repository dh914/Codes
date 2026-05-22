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

### 프롬프트 카탈로그 기반 일괄 생성

레퍼런스 퀄리티(한국 모던 일러스트 작가 스타일 — 파스텔 색연필 텍스처·플랫 일러스트)
프롬프트가 `prompts/card_illustrations.json`에 카탈로그로 저장되어 있습니다.

```bash
# 명함용 일러스트 (앞면 배경, 뒷면 배경, 마을 풍경)
./scripts/generate_card_illustrations.sh

# 또는 카탈로그에서 원하는 키만
python scripts/generate_from_catalog.py card_front_bg rice_planting_event

# 전체 카탈로그 생성
python scripts/generate_from_catalog.py --all

# 모델 / 프로바이더 오버라이드
python scripts/generate_from_catalog.py --all -m black-forest-labs/FLUX.1-dev --provider fal-ai
```

카탈로그 키:

| 키 | 용도 | 추천 모델 |
|---|---|---|
| `card_front_bg` | 명함 앞면 배경 | FLUX.1-schnell |
| `card_back_bg` | 명함 뒷면 배경 | FLUX.1-schnell |
| `village_scene` | 마을 풍경 일러스트 | FLUX.1-schnell |
| `rice_planting_event` | 손모내기 포스터 메인 | FLUX.1-dev |
| `harvest_scene` | 수확 포스터 | FLUX.1-dev |
| `community_circle` | 청년 커뮤니티 모임 | FLUX.1-dev |

생성된 PNG는 `design/illust_<key>.png`로 저장됩니다.

### 컨테이너(클로드 코드 웹)에서 직접 실행하려면

이 레포가 클로드 코드 웹 컨테이너에서 동작하는 경우, **외부 호스트가 화이트리스트로 차단**되어
있어 별도 설정이 필요합니다. 두 가지 경로 중 선택:

**A. HF MCP 툴박스에 모델 Space 추가 (권장)**
1. <https://hf.co/settings/mcp> 접속해 HF_TOKEN 등록
2. Active Tools에 `black-forest-labs/FLUX.1-schnell`, `black-forest-labs/FLUX.1-dev`,
   `multimodalart/flux-lora-the-explorer` 추가
3. 클로드 코드 세션 재시작 → MCP 도구로 직접 호출 가능

**B. 컨테이너 outbound allowlist에 HF 도메인 추가**
- `huggingface.co`, `*.hf.space`, `api-inference.huggingface.co`, `router.huggingface.co`
- 환경 변수 `HF_TOKEN` 추가 → 세션 재시작
- 이후 `scripts/generate_poster.py` 가 컨테이너 내에서 직접 동작

### 권장 모델

| 모델 | 용도 | 비고 |
|---|---|---|
| `black-forest-labs/FLUX.1-schnell` | 일반 포스터·일러스트 | 4 step, 무료 |
| `black-forest-labs/FLUX.1-dev` | 더 정교한 디테일 | gated, 토큰 권한 필요 |
| `black-forest-labs/FLUX.2-klein-9B` | 최신 (FLUX.2) | 큰 모델 |
| `stabilityai/stable-diffusion-xl-base-1.0` | 클래식 SDXL | guidance 7.5 권장 |
