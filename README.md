# SUBMARINE HW

퇴역 장보고함 전시 기본계획을 위한 국내외 잠수함 박물관 벤치마킹 대시보드입니다. 사례, 출처, 데이터 정합성, 전시방식 비교와 현장조사 우선순위를 한 화면에서 관리합니다.

## 실행

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

macOS/Linux에서는 활성화 명령을 `source .venv/bin/activate`로 바꾸면 됩니다.

## 데이터 업데이트

- 사례 데이터: `data/cases.csv`
- 앱 기준일·설명: `data/meta.json`
- 사례를 추가하면 지도, 요약지표, 비교표, 데이터 품질 화면에 자동 반영됩니다.
- `confidence`는 `A`, `B`, `C`, `D` 중 하나를 사용합니다.
- 현재 운영 여부와 과거 운영 사례를 혼동하지 않도록 `status`를 반드시 갱신합니다.

## 구조

```text
submarine_hw/
├─ app.py
├─ data/
│  ├─ cases.csv
│  └─ meta.json
├─ research/
│  └─ methodology.md
├─ .streamlit/config.toml
└─ requirements.txt
```

## 데이터 원칙

공식 정부·해군·박물관 자료를 우선하고, 핵심 수치는 가능한 한 독립 출처로 교차검증합니다. 상충하거나 확인되지 않은 정보는 추정값으로 메우지 않고 `data_warning`에 남깁니다.

기준일: 2026-08-06. 본 프로젝트는 전시 기획 참고용이며 구조·소방·보존 자문이 아닙니다.
