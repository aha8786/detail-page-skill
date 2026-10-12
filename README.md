# 상세페이지 스킬 (detail-page-skill)

이커머스 상세페이지를 **블록 단위로 기획·제작·분석**하는 AI 에이전트 스킬.

레퍼런스를 눈대중하지 않고 **픽셀로 측정**해서 규격을 뽑고, HTML/CSS 로 조립해
블록별 PNG 로 뽑고, 식품 광고 법규까지 검사한다.

분석해 둔 블록 구조를 **프리셋**으로 쌓아 두고, 새 상품을 만들 때 골라 쓴다.
Claude · Codex · Cursor · ChatGPT 등 어디서나 쓸 수 있다.

<p align="center">
  <img src="examples/woolenggi/01_hook.png" width="200">
  <img src="examples/woolenggi/03_point1.png" width="200">
  <img src="examples/woolenggi/05_package.png" width="200">
</p>

---

## 무엇을 하나

스킬이 켜지면 메뉴가 뜬다.

```
상세페이지 스킬이 켜졌습니다. 무엇을 할까요?

  /상세페이지 만들기     기획부터 블록별 PNG 출력까지 전 과정
  /블록카피하기          블록 1장을 픽셀 측정해 기존 구조에 추가
  /상세페이지 분석하기    레퍼런스 페이지를 분석해 새 블록 구조로 등록

번호나 명령어로 골라 주세요.
```

## 프리셋 — 이 스킬의 핵심

**하나의 프리셋 = 하나의 블록 구조 세트.**
레퍼런스에서 뽑아낸 레이아웃·색·타이포·블록 시퀀스가 한 묶음이다.

```
skill/TOOL.md        고정 규격. 프리셋이 바뀌어도 항상 적용
                     여백 균등 · 줄맞춤 · 사진 선택 · 크롭 · 대비비 하한 · 식품 법규

presets/_index.md    등록된 블록 구조 카탈로그
presets/<id>/
  PRESET.md          캔버스 · 색 · 폰트 · 타이포 수치 · 블록 y 좌표 · 시퀀스
  blocks/            블록 HTML·CSS·render.sh
  references/        측정 근거 — 어느 레퍼런스에서 어떻게 뽑았는지
  preview/           미리보기

충돌하면 고정 규격이 이긴다.
```

프리셋이 쌓일수록 만들 수 있는 스타일이 늘어난다.
상품마다 처음부터 분석할 필요가 없다.

```
레퍼런스 페이지  ──/상세페이지 분석하기──▶  프리셋 등록
                                              │
블록 1장        ──/블록카피하기───────────▶  프리셋에 블록 추가
                                              │
                                              ▼
상품 정보 + 사진 ──/상세페이지 만들기──────▶  블록별 PNG
                  (1단계에서 프리셋 선택)
```

### 등록된 프리셋

| ID | 이름 | 성격 | 블록 시퀀스 | 카테고리 |
|---|---|---|---|---|
| `hana-nongsusan` | 하나농수산형 | 다크 히어로 → 라이트 정보. 사진 69% | hook → opener → point ×2~3 → package | 수산물·신선식품 |

---

## 명령

### `/상세페이지 만들기`

```
1. 프리셋 선택   ★ 먼저 고른다. 없으면 분석하기로 보낸다
2. 범위 확정     플랫폼 · 카테고리
3. 인터뷰        사실만 수집. 추측으로 채우지 않는다
4. 사진 인벤토리  전부 훑고 분류 + 해상도 판정
5. 블록 선택     소구 축 배정 (축 중복 금지)
6. 기획안        y 좌표 · 카피 전문 · 법규 검사 · 합격 기준
7. 렌더          headless Chrome → 블록별 PNG
8. 자체 테스트    합격 기준 대조 + PNG 육안 확인
```

### `/블록카피하기` — 블록 1장

기존 프리셋에 블록을 추가하거나 교체한다.

```
측정   →  잉크 박스 · 여백 · 글자 pitch · 색 · 사진 비율
기록   →  presets/<id>/references/ANALYSIS.md 에 REF-NN 누적
정합성 →  프리셋 팔레트·폰트·여백과 맞는지 검사. 어긋나면 프리셋에 맞춘다
생성   →  presets/<id>/blocks/block-*.html
검증   →  렌더 후 재측정. 원본과 ±3px 안이면 성공
등록   →  PRESET.md 5·6·9장 갱신
```

### `/상세페이지 분석하기` — 페이지 전체

레퍼런스를 분석해 **새 프리셋을 등록**한다. 진단 리포트가 같이 나온다.

```
1. 블록 쪼개기     --segment 로 경계 추정
2. 블록별 측정     9항목 기록
3. 구조 진단      길이 · 사진 비중 · 명도 리듬 · 정렬 패턴
4. 공통 패턴 추출  ★ 반복되는 값 → 토큰으로 승격 (프리셋의 뼈대)
5. 결함 걸러내기   ★ 고정 규격과 충돌하는 값은 버린다
6. 프리셋 등록     presets/<새 id>/ 생성 + 카탈로그에 추가
7. 진단 리포트     치명 / 중요 / 사소 + 그대로 둘 것
```

진단만 원하면 1~3 + 7 만 돌린다.

---

## 설치

### Claude Code

```bash
git clone https://github.com/aha8786/detail-page-skill.git \
  ~/.claude/skills/detail-page
```

`SKILL.md` 의 frontmatter 를 읽어 자동으로 발동한다.
수동 호출은 `/detail-page`.

### Claude.ai (웹)

저장소를 zip 으로 받아 Settings → Capabilities → Skills 에 업로드한다.

### Codex · Cursor · Windsurf · Devin

저장소를 프로젝트에 넣거나 clone 한 뒤, 루트의 `AGENTS.md` 를 읽게 한다.

```bash
git clone https://github.com/aha8786/detail-page-skill.git .detail-page-skill
```

프로젝트 `AGENTS.md` 에 한 줄 추가:
```markdown
상세페이지 작업은 `.detail-page-skill/AGENTS.md` 를 따른다.
```

### ChatGPT Custom GPT

1. `platforms/chatgpt-instructions.md` 전문을 **Instructions** 에 붙여 넣는다
2. `skill/` 과 `scripts/` 의 파일들을 **Knowledge** 에 업로드한다
3. **Code Interpreter** 를 켠다 (픽셀 측정에 필요)

> ChatGPT 에는 headless Chrome 이 없어 HTML 렌더가 안 된다.
> 측정·기획·카피·법규 검사까지 하고, 렌더는 HTML 을 받아 로컬에서 돌린다.

### 그 외 도구

`SKILL.md` + `skill/` 폴더 내용을 시스템 프롬프트에 붙여 넣으면 동작한다.

---

## 환경 요구사항

| 용도 | 필요한 것 |
|---|---|
| 렌더 | headless Chrome (macOS 기본 경로는 `render.sh` 에 포함) |
| 측정·테스트 | Python 3 + Pillow |

```bash
pip install pillow
# 막히면
python3 -m venv .venv && ./.venv/bin/pip install pillow
```

---

## 도구

### `scripts/measure.py` — 픽셀 측정

```bash
python3 scripts/measure.py ref.png --target-width 610
```

```
잉크 밴드 (y 시작·끝·높이)        글자 한 줄 = 한 밴드
x 범위 · 폭 · 중심               가운데 정렬 여부 판정
글자 pitch · 잉크/pitch 비율      폰트 종류 판별
행 pitch                        행간
배경색 · 다크/라이트
```

**잉크/pitch 비율로 폰트를 가린다.**
```
~0.72   일반 고딕 (Pretendard · Noto Sans KR)
0.95+   헤비 스퀘어 고딕 (Paperlogy · Black Han Sans · GmarketSans)
```

```bash
python3 scripts/measure.py page.png --segment   # 블록 경계 추정
python3 scripts/measure.py page.png --colors    # 색 분포
```

### `scripts/qa.py` — 자체 테스트

```bash
python3 scripts/qa.py out/ --palette 292929,F5F0E6,8C867C
```

캔버스 크기 · 최대 높이 · 팔레트 준수 · 이음매를 기계로 검사한다.
**기계가 못 잡는 것은 목록으로 알려 준다** — 사진·크롭·가독성은 사람이 봐야 한다.

---

## 규격의 뼈대

`skill/TOOL.md` 전문. 핵심만 옮기면:

**고정 규격 — 바꾸려면 측정 근거가 있어야 한다**

```
본문 블록 상하 여백을 반드시 같게 준다 (라인박스 기준)
본문 줄은 직접 끊는다. 의미 단위 > 길이 균등
사진은 1순위 멘트 연관성 → 식별성 → 해상도 → 색 정합
잘려도 상품이 프레임 한가운데 오게 크롭한다
대비비 하한 — 히어로 3:1, 본문 2:1
면책 문구는 본문과 같은 크기, 색만 낮춘다
```

**프리셋 — `presets/<id>/PRESET.md`**

```
캔버스 폭 · 색상 토큰 · 폰트와 배치 계수 · 타이포 수치 · 블록 y 좌표 · 시퀀스
```

**카테고리 모듈**

```
6장  식품 광고 금지 표현 (식품표시광고법 제8조)
     질병·효능 / 의약품 오인 / 건강기능식품 오인 / 거짓과장 /
     소비자 기만 / 무인증 단어 / 후기 효능 암시 / 타사 비방 /
     배송물류 정보 / 영양강조표시 + 안전한 대체 표현표
```

---

## 예제

`examples/woolenggi/` — 실제로 만든 상세페이지 전 과정.

```
INTERVIEW.md   참고 자료 → 사실 추출 → 사진 26장 인벤토리 → 결정 기록
ANALYSIS.md    레퍼런스 4종 픽셀 측정 + 공통 패턴 추출
PLAN.md        기획안 + 합격 기준
0*.png         완성 블록 5장 (축소판)
```

법규 때문에 소구 축을 바꾼 과정, 사진이 2번 탈락한 기록,
레퍼런스의 결함을 따라 하지 않은 지점이 전부 남아 있다.

---

## 왜 이렇게 만들었나

상세페이지 작업에서 반복되는 손해 세 가지를 막는다.

```
1. 눈대중    "이 정도면 되겠지" 로 잡은 여백이 블록마다 어긋난다
             → 전부 픽셀로 측정하고 숫자로 기록한다

2. 법규      식품은 쓰면 안 되는 말이 많은데 다 쓰고 나서 안다
             → 기획 단계와 출력 단계에서 두 번 검사한다

3. 재작업    한 군데 고치려고 통짜 이미지를 다시 뽑는다
             → 블록별 독립 PNG. 한 장만 다시 뽑는다

4. 매번 처음  상품이 바뀔 때마다 구조를 새로 짠다
             → 분석한 구조를 프리셋으로 쌓아 두고 골라 쓴다
```

---

## 라이선스

MIT
