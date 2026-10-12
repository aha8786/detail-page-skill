# 상세페이지 스킬 (detail-page-skill)

이커머스 상세페이지를 **블록 단위로 기획·제작·분석**하는 AI 에이전트 스킬.

레퍼런스를 눈대중하지 않고 **픽셀로 측정**해서 규격을 뽑고, HTML/CSS 로 조립해
블록별 PNG 로 뽑고, 식품 광고 법규까지 검사한다.

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
  /블록카피하기          레퍼런스 블록을 픽셀 측정해 내 규격으로 복제
  /상세페이지 분석하기    완성된 페이지의 구조·법규·가독성 진단

번호나 명령어로 골라 주세요.
```

### `/상세페이지 만들기`

```
0. 범위 확정    플랫폼 · 카테고리 · 캔버스 폭
1. 레퍼런스 분석  있으면 측정, 없으면 기본 규격
2. 인터뷰       사실만 수집. 추측으로 채우지 않는다
3. 사진 인벤토리  전부 훑고 분류 + 해상도 판정
4. 블록 선택     소구 축 배정 (축 중복 금지)
5. 기획안       y 좌표 · 카피 전문 · 법규 검사 · 합격 기준
6. 렌더         headless Chrome → 블록별 PNG
7. 자체 테스트    합격 기준 대조 + PNG 육안 확인
```

### `/블록카피하기`

남의 상세페이지 블록을 픽셀 측정해 내 규격으로 가져온다.

```
측정  →  잉크 박스 · 여백 · 글자 pitch · 색 · 사진 비율
기록  →  REF-NN 으로 9항목 누적
승격  →  반복되는 값을 토큰으로 고정, 결함은 따라 하지 않음
생성  →  블록 HTML 템플릿
검증  →  렌더 후 재측정. 원본과 ±3px 안이면 성공
```

### `/상세페이지 분석하기`

완성된 페이지를 진단하고 고칠 곳을 **치명 / 중요 / 사소** 로 나눠 낸다.
잘 된 부분도 적는다 — 안 적으면 다음 개정에서 날아간다.

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

**프리셋 — 프로젝트마다 바꾼다**

```
캔버스 폭 · 색상 토큰 · 폰트 · 블록 시퀀스
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
```

---

## 라이선스

MIT
