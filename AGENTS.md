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

  /상세페이지 만들기     기획부터 블록별 PNG 출력까지 전 과정
  /블록카피하기          레퍼런스 블록을 픽셀 측정해 내 규격으로 복제
  /상세페이지 분석하기    완성된 페이지의 구조·법규·가독성 진단

번호나 명령어로 골라 주세요.
```

## 명령 → 읽을 파일

```
/상세페이지 만들기    skill/TOOL.md + skill/01-create.md
/블록카피하기         skill/TOOL.md + skill/02-block-copy.md
/상세페이지 분석하기   skill/TOOL.md + skill/03-analyze.md
```

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
