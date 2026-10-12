#!/bin/bash
# 610px 캔버스 · DPR2 → PNG 1220px 폭
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT="${1:-out}"
mkdir -p "$OUT"
render(){  # $1=html  $2=height  $3=name
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars \
    --force-device-scale-factor=2 --window-size=610,$2 \
    --allow-file-access-from-files --default-background-color=ffffffff \
    --virtual-time-budget=6000 \
    --screenshot="$OUT/$3.png" "file://$PWD/$1" 2>/dev/null
  printf "%-16s " "$3.png"; sips -g pixelWidth -g pixelHeight "$OUT/$3.png" 2>/dev/null | tail -2 | tr -d '\n '; echo
}
render 01_hook.html    1000 01_hook
render 02_opener.html   603 02_opener
render 03_point1.html  1286 03_point1
render 04_point2.html  1240 04_point2
render 05_package.html  645 05_package
