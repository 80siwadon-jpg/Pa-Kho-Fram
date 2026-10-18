#!/usr/bin/env bash
# สร้างคลิปทั้งหมดตั้งแต่ต้น: เสียงพากย์ -> ภาพ -> เสียงประกอบ -> mp4
set -euo pipefail
cd "$(dirname "$0")"
MODEL=${MODEL:-models/vits-mms-tha}

pip install -q -r requirements.txt
if [ ! -f "$MODEL/model.onnx" ]; then
  mkdir -p models
  curl -L -o models/vits-mms-tha.tar.bz2 \
    https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-mms-tha.tar.bz2
  tar xjf models/vits-mms-tha.tar.bz2 -C models
fi

mkdir -p build output
python3 src/tts.py --model "$MODEL" --target 89     # build/narration.wav + timeline.json
python3 src/render.py                               # build/video.mp4 + cues.json
python3 src/audio.py                                # build/mix.wav
ffmpeg -y -loglevel error -i build/video.mp4 -i build/mix.wav \
  -map 0:v -map 1:a -c:v libx264 -preset medium -b:v 8M -maxrate 11M -bufsize 16M -pix_fmt yuv420p -c:a aac -b:a 192k \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11" -shortest -movflags +faststart \
  output/alaska_18oct_1080p60.mp4
echo "done -> output/alaska_18oct_1080p60.mp4"
