#!/usr/bin/env bash
# สร้างคลิป: เสียงพากย์ -> ภาพ + ซับ -> mp4
#   ./make.sh                    ใช้เสียง AI (ชั่วคราว)
#   ./make.sh my_voice.m4a 1.1   ใช้เสียงอัดเอง (เร่งความเร็ว 1.1 เท่า)
set -euo pipefail
cd "$(dirname "$0")"
OUT=${OUT:-output/alaska_18oct_1080p60.mp4}
mkdir -p build output

if [ $# -ge 1 ]; then
  python3 src/voice.py "$1" --tempo "${2:-1.0}"
else
  MODEL=${MODEL:-models/vits-mms-tha}
  if [ ! -f "$MODEL/model.onnx" ]; then
    mkdir -p models
    curl -L -o models/vits-mms-tha.tar.bz2 \
      https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-mms-tha.tar.bz2
    tar xjf models/vits-mms-tha.tar.bz2 -C models
  fi
  python3 src/tts.py --model "$MODEL"
fi
python3 src/render.py --out "$OUT"
