#!/usr/bin/env python3
"""상세페이지 블록 픽셀 측정기.

눈대중을 없애기 위한 도구. 잉크 박스·여백·색·사진 비율을 실측한다.

사용법
  python3 measure.py ref.png                    # 기본 측정
  python3 measure.py ref.png --target-width 610 # 목표 캔버스로 환산
  python3 measure.py page.png --segment         # 블록 경계 추정
  python3 measure.py page.png --colors          # 색 분포만

의존성: pillow
"""
import argparse, sys
from collections import Counter

try:
    from PIL import Image
except ImportError:
    sys.exit("pillow 가 필요하다:  pip install pillow\n"
             "막히면:  python3 -m venv .venv && ./.venv/bin/pip install pillow")


def hexs(c):
    return "#%02X%02X%02X" % c


def load(path):
    im = Image.open(path).convert("RGB")
    return im, im.size[0], im.size[1], im.load()


def bands(px, W, y0, y1, test, minc=3):
    out, cur = [], None
    for y in range(y0, y1):
        c = sum(1 for x in range(W) if test(px[x, y]))
        if c >= minc:
            cur = [y, y] if cur is None else [cur[0], y]
        else:
            if cur:
                out.append(tuple(cur))
                cur = None
    if cur:
        out.append(tuple(cur))
    return out


def xext(px, W, a, b, test):
    xs = [x for x in range(W) for y in range(a, b + 1) if test(px[x, y])]
    return (min(xs), max(xs)) if xs else None


def char_runs(px, W, a, b, test, gap=3):
    """글자별 열 런. 인접 런의 시작 간 거리가 글자 pitch(advance)."""
    cols = [x for x in range(W) if any(test(px[x, y]) for y in range(a, b + 1))]
    runs, cur = [], None
    for x in cols:
        if cur is None:
            cur = [x, x]
        elif x - cur[1] <= gap:
            cur[1] = x
        else:
            runs.append(tuple(cur)); cur = [x, x]
    if cur:
        runs.append(tuple(cur))
    return runs


def bg_color(px, W, H):
    c = Counter()
    for y in list(range(0, 6)) + list(range(H - 6, H)):
        for x in range(0, W, 3):
            c[px[x, y]] += 1
    return c.most_common(1)[0][0]


def measure(path, target_w=None, show_colors=False, segment=False):
    im, W, H, px = load(path)
    k = (target_w / W) if target_w else 1.0
    unit = f"(→{target_w}px 환산)" if target_w else "(원본 px)"
    print(f"== {path}")
    print(f"   원본 {W} x {H}" + (f"   배율 k = {k:.4f}   환산 {target_w} x {round(H*k)}" if target_w else ""))

    bg = bg_color(px, W, H)
    dark_bg = sum(bg) < 330
    print(f"   배경색 {hexs(bg)}  ({'다크' if dark_bg else '라이트'})")

    if show_colors:
        c = Counter()
        for y in range(0, H, 4):
            for x in range(0, W, 4):
                c[tuple(v // 8 * 8 for v in px[x, y])] += 1
        print("\n-- 색 분포 상위 8 --")
        for col, n in c.most_common(8):
            print(f"   {hexs(col)}  {n:>7}  {n*100/sum(c.values()):.1f}%")
        return

    if segment:
        print("\n-- 블록 경계 추정 (배경색만 있는 행) --")
        pure = [y for y in range(H)
                if sum(1 for x in range(0, W, 2) if max(abs(a - b) for a, b in zip(px[x, y], bg)) < 10) > (W // 2) * 0.95]
        rr, cur = [], None
        for y in pure:
            if cur is None:
                cur = [y, y]
            elif y - cur[1] <= 1:
                cur[1] = y
            else:
                rr.append(tuple(cur)); cur = [y, y]
        if cur:
            rr.append(tuple(cur))
        for a, b in rr:
            if b - a > 8:
                print(f"   y {a}-{b}  두께 {(b-a+1)*k:.1f} {unit}")
        return

    # 텍스트: 배경과 반대 극성
    ink = (lambda c: min(c) > 215) if dark_bg else (lambda c: max(c) < 110)
    print(f"\n-- 잉크 밴드 ({'밝은 글자' if dark_bg else '어두운 글자'}) {unit} --")
    bs = bands(px, W, 0, H, ink, minc=4)
    prev_top = None
    for a, b in bs:
        e = xext(px, W, a, b, ink)
        if not e:
            continue
        runs = char_runs(px, W, a, b, ink)
        pitch = None
        if len(runs) >= 3:
            starts = [r[0] for r in runs]
            gaps = [starts[i + 1] - starts[i] for i in range(len(starts) - 1)]
            gaps = [g for g in gaps if g > 3]
            if gaps:
                gaps.sort()
                pitch = gaps[len(gaps) // 2]
        h = (b - a + 1) * k
        line = (f"   y {a*k:7.1f}-{b*k:7.1f}  잉크높이 {h:6.1f}"
                f"  x {e[0]*k:6.1f}-{e[1]*k:6.1f}  폭 {(e[1]-e[0]+1)*k:6.1f}"
                f"  중심 {(e[0]+e[1])*k/2:6.1f}")
        if pitch:
            line += f"  pitch {pitch*k:5.1f}  잉크/pitch {h/(pitch*k):.3f}"
        print(line)
        if prev_top is not None:
            print(f"        └ 앞 밴드와 행 pitch {(a-prev_top)*k:.1f}")
        prev_top = a

    print("\n   잉크/pitch 해석:  ~0.72 일반 고딕   0.95+ 헤비 스퀘어 고딕")
    print(f"   캔버스 중심 {W*k/2:.1f}  (중심값이 이와 ±5 안이면 가운데 정렬)")


def main():
    ap = argparse.ArgumentParser(description="상세페이지 블록 픽셀 측정")
    ap.add_argument("image")
    ap.add_argument("--target-width", type=int, default=None, help="목표 캔버스 폭으로 환산 (예: 610)")
    ap.add_argument("--colors", action="store_true", help="색 분포만 출력")
    ap.add_argument("--segment", action="store_true", help="블록 경계 추정")
    a = ap.parse_args()
    measure(a.image, a.target_width, a.colors, a.segment)


if __name__ == "__main__":
    main()
