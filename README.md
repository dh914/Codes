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
