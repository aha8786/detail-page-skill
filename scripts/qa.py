#!/usr/bin/env python3
"""렌더된 블록 PNG 자체 테스트.

PLAN.md 의 합격 기준을 기계로 대조한다.
단 이걸로 끝이 아니다 — 사진·크롭·가독성은 사람이 PNG 를 열어서 봐야 한다.

사용법
  python3 qa.py out/                       # 폴더 전체
  python3 qa.py out/ --width 610 --dpr 2
  python3 qa.py out/ --palette 292929,F5F0E6,8C867C

의존성: pillow
"""
import argparse, os, sys, glob
from collections import Counter

try:
    from PIL import Image
except ImportError:
    sys.exit("pillow 가 필요하다:  pip install pillow")


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def near(c, t, tol=12):
    return all(abs(a - b) <= tol for a, b in zip(c, t))


def run(folder, width, dpr, palette):
    files = sorted(glob.glob(os.path.join(folder, "*.png")))
    files = [f for f in files if not os.path.basename(f).startswith("_")]
    if not files:
        sys.exit(f"PNG 가 없다: {folder}")
    want_w = width * dpr
    pal = [rgb(p) for p in palette] if palette else []
    fails, total_h = [], 0

    print(f"기준: 폭 {want_w}px (={width}×DPR{dpr})   블록 최대 높이 {3000*dpr}px\n")
    print(f"{'파일':<20}{'크기':<16}{'폭':<7}{'높이':<7}{'판정'}")
    print("-" * 62)
    for f in files:
        im = Image.open(f).convert("RGB")
        W, H = im.size
        total_h += H
        ok_w = W == want_w
        ok_h = H <= 3000 * dpr
        if not ok_w:
            fails.append(f"{os.path.basename(f)} 폭 {W} ≠ {want_w}")
        if not ok_h:
            fails.append(f"{os.path.basename(f)} 높이 {H} > {3000*dpr} — 분할 필요")
        print(f"{os.path.basename(f):<20}{W}x{H:<10}{'OK' if ok_w else 'FAIL':<7}{'OK' if ok_h else 'FAIL':<7}")
    print("-" * 62)
    print(f"합계 높이 {total_h} (={total_h//dpr}px @{width})\n")

    if pal:
        print("-- 팔레트 준수 --")
        for f in files:
            im = Image.open(f).convert("RGB")
            W, H = im.size
            px = im.load()
            c = Counter()
            for y in range(0, H, 5):
                for x in range(0, W, 5):
                    c[px[x, y]] += 1
            top = c.most_common(3)
            labs = []
            for col, n in top:
                hit = next((f"#{palette[i]}" for i, p in enumerate(pal) if near(col, p, 10)), "사진/기타")
                labs.append(f"{hit}:{n}")
            print(f"  {os.path.basename(f):<18}" + "  ".join(labs))
        print()

    print("-- 이음매 (블록 경계 색 연속성) --")
    prev = None
    for f in files:
        im = Image.open(f).convert("RGB")
        W, H = im.size
        px = im.load()
        bot = [px[x, H - 1] for x in range(0, W, max(1, W // 12))]
        if prev is not None:
            d = max(sum(abs(a - b) for a, b in zip(u, v)) for u, v in zip(prev, bot and [px[x, 0] for x in range(0, W, max(1, W // 12))]))
            note = "사진/명도전환 지점이면 정상" if d > 120 else "연속"
            print(f"  {os.path.basename(f):<18} 앞 블록과 최대 색차 {d:<5} {note}")
        prev = bot
    print()

    print("=" * 62)
    if fails:
        print("FAIL")
        for x in fails:
            print("  -", x)
    else:
        print("기계 검사 전 항목 통과")
    print("""
※ 여기서 끝이 아니다. PNG 를 직접 열어 확인할 것:
   - 사진이 바로 옆 멘트와 맞는가
   - 피사체가 프레임 한가운데 있는가
   - 텍스트가 피사체를 가리지 않는가
   - 본문 줄 끊김·줄 끝 쉼표·줄 길이 편차
   - 식품이면 TOOL.md 6장 금지 표현 전수 검사""")
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description="블록 PNG 자체 테스트")
    ap.add_argument("folder")
    ap.add_argument("--width", type=int, default=610)
    ap.add_argument("--dpr", type=int, default=2)
    ap.add_argument("--palette", type=str, default="", help="쉼표로 구분한 HEX. 예: 292929,F5F0E6,8C867C")
    a = ap.parse_args()
    sys.exit(run(a.folder, a.width, a.dpr, [p.strip() for p in a.palette.split(",") if p.strip()]))


if __name__ == "__main__":
    main()
