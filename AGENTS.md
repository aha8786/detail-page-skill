# AGENTS.md — 상세페이지 스킬

Codex · Cursor · Windsurf · Devin 등 AGENTS.md 를 읽는 에이전트용 지침.
Claude 계열은 `SKILL.md` 를, ChatGPT Custom GPT 는 `platforms/chatgpt-instructions.md` 를 쓴다.

## 언제 발동하나

사용자 요청에 아래가 들어오면 이 저장소의 지침을 따른다.

```
상세페이지 · 상세 이미지 · 제품 상세 · 블록 이미지 · 스마트스토어 상세
detail page · product detail · 상세컷 · 상세 디자인
```

## 발동 시 첫 출력

다른 말을 하기 전에 이 메뉴를 그대로 낸다.
사용자가 이미 명령을 지정했으면 건너뛴다.

```
상세페이지 스킬이 켜졌습니다. 무엇을 할까요?

  /알아서 만들기         내용만 주시면 구조·디자인까지 제가 정해서 만듭니다
  /상세페이지 만들기     저장된 블록 구조를 골라서 만듭니다
  /블록카피하기          블록 1장을 분석해 바로 PNG로 만들어 드립니다
  /상세페이지 분석하기    페이지를 분석해 블록 구조 파일로 저장합니다

번호나 명령어로 골라 주세요.
```

## 명령 → 읽을 파일

```
/알아서 만들기        skill/TOOL.md + skill/04-auto.md
/상세페이지 만들기    skill/TOOL.md + presets/_index.md + skill/01-create.md
/블록카피하기         skill/TOOL.md + presets/_index.md + skill/02-block-copy.md
/상세페이지 분석하기   skill/TOOL.md + skill/03-analyze.md
```

## 프리셋 구조

```
skill/TOOL.md     고정 규격. 항상 적용. 프리셋과 충돌하면 이쪽이 이긴다
presets/_index.md 블록 구조 카탈로그
presets/<id>/     PRESET.md(수치) · blocks/(템플릿) · references/(측정 근거) · preview/
```

**결과물로 구분한다**
```
자료 + 사진     ──/알아서 만들기───────▶ PNG 한 벌 (구조·색·폰트까지 설계)
상품 정보+사진  ──/상세페이지 만들기───▶ PNG 한 벌 (프리셋 선택)
블록 레퍼런스   ──/블록카피하기────────▶ PNG 1장 (끝에 프리셋 저장 여부를 물음)
레퍼런스 페이지 ──/상세페이지 분석하기──▶ presets/<id>/  ·  이미지 없음
```

`/알아서 만들기` 와 `/상세페이지 만들기` 의 차이는 **구조를 누가 정하느냐**다.

## 환경 요구사항

```
headless Chrome   렌더용. macOS 기본 경로는 render.sh 에 들어 있다
Python 3 + Pillow  측정·테스트용.  pip install pillow
```

Pillow 설치가 막히면 가상환경을 쓴다.
```bash
python3 -m venv .venv && ./.venv/bin/pip install pillow
```

## 절대 규칙

1. 치수는 추측하지 않는다. 레퍼런스는 `scripts/measure.py` 로 실측한다
2. 렌더한 PNG를 직접 열어 눈으로 확인한다
3. 식품이면 광고 법규를 기획·출력 두 단계에서 검사한다
4. 사용자가 지정한 사진·카피는 임의로 바꾸지 않는다
5. 블록은 독립 PNG로 낸다
6. `/상세페이지 만들기` 는 프리셋을 고르기 전에 제작에 들어가지 않는다
   `/상세페이지 분석하기` 는 이미지를 만들지 않는다
7. 레퍼런스를 그대로 베끼지 않는다. 고정 규격이 우선이다
8. 디자인은 알아서 정해도 되지만 사실(원산지·공정·중량·인증)은 지어내지 않는다
