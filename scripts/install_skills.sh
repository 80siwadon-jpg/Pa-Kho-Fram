#!/usr/bin/env bash
# ติดตั้งสกิลแอนิเมชันจาก GitHub เข้า ~/.claude/skills (Claude Code โหลดอัตโนมัติ)
#   bash scripts/install_skills.sh
# โคลนแบบตื้นไว้ที่ $SKILL_REPOS/<owner>/<repo> (ค่าเริ่มต้น ~/.claude/skill-repos) แล้วลิงก์โฟลเดอร์สกิล
# ไม่รันสคริปต์ติดตั้งของแต่ละ repo (เช่น kit/setup.sh) — ให้รันเองเมื่อจะใช้สกิลนั้นจริง
#
# ใบอนุญาต (ตรวจแล้ว):
#   artemnovitckii/claude-animation-skills  MIT
#   diffusionstudio/lottie                  MIT
#   vincentsch/explainroo                   MIT
#   lemomo-ai/lemo-opuscar                  โค้ด MIT, เอกสาร/SKILL.md CC BY-NC 4.0, หนังที่สร้างเป็นของผู้ใช้ (ใช้เชิงพาณิชย์ได้)
#   feitangyuan/onetake                     PolyForm Noncommercial 1.0 — ใช้ได้เฉพาะงานไม่แสวงกำไร
#   alchaincyf/huashu-art-motion, alchaincyf/huashu-motion, Leonxlnx/earshot, NiazMorshed2007/reanimate,
#   rossark0/rossark-motion-skill, win4r/video-director, talsiach/take-one, shreyaskarnik/argo   MIT
#   Barty-Bart/motion-graphics, charlie947/motion-graphics-skills                                  MIT
#   mattypark/Motion-graphics-skill   ไม่มีไฟล์ใบอนุญาต (สงวนสิทธิ์โดยปริยาย) — ติดตั้งใช้ส่วนตัวเท่านั้น ห้ามแจกจ่ายต่อ
set -euo pipefail
REPOS="${SKILL_REPOS:-$HOME/.claude/skill-repos}"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
mkdir -p "$REPOS" "$DEST"

fetch() {   # owner/repo
  local dir="$REPOS/$1"
  if git -C "$dir" rev-parse HEAD >/dev/null 2>&1; then
    git -C "$dir" pull -q --ff-only || echo "warning: could not update $1"
  else
    mkdir -p "$(dirname "$dir")"
    GIT_LFS_SKIP_SMUDGE=1 git clone -q --depth 1 "https://github.com/$1" "$dir"
  fi
}

link() {    # folder-that-has-SKILL.md  skill-name
  local src="$1" name="$2"
  [ -f "$src/SKILL.md" ] || { echo "skip $name: no SKILL.md in $src"; return; }
  if [ -e "$DEST/$name" ] && [ ! -L "$DEST/$name" ]; then
    echo "skip $name: $DEST/$name exists and is not a link"; return
  fi
  ln -sfn "$src" "$DEST/$name"
  echo "linked $name"
}

for r in artemnovitckii/claude-animation-skills diffusionstudio/lottie feitangyuan/onetake \
         vincentsch/explainroo lemomo-ai/lemo-opuscar \
         alchaincyf/huashu-art-motion alchaincyf/huashu-motion Leonxlnx/earshot NiazMorshed2007/reanimate \
         rossark0/rossark-motion-skill win4r/video-director talsiach/take-one shreyaskarnik/argo \
         Barty-Bart/motion-graphics mattypark/Motion-graphics-skill charlie947/motion-graphics-skills; do
  fetch "$r"
done

for d in "$REPOS"/artemnovitckii/claude-animation-skills/skills/*/; do
  link "${d%/}" "$(basename "$d")"
done
link "$REPOS/diffusionstudio/lottie/skills/text-to-lottie" text-to-lottie
link "$REPOS/feitangyuan/onetake" onetake
link "$REPOS/vincentsch/explainroo/skills/explainroo" explainroo
link "$REPOS/lemomo-ai/lemo-opuscar/plugin/skills/lemo-opuscar" lemo-opuscar
link "$REPOS/alchaincyf/huashu-art-motion" huashu-art-motion
link "$REPOS/alchaincyf/huashu-motion/skills/huashu-motion" huashu-motion
link "$REPOS/Leonxlnx/earshot/skills/earshot" earshot
link "$REPOS/Leonxlnx/earshot/skills/real-sound" real-sound
link "$REPOS/NiazMorshed2007/reanimate/skills/reanimate" reanimate
link "$REPOS/rossark0/rossark-motion-skill" rossark-motion-skill
link "$REPOS/win4r/video-director/video-director" video-director
link "$REPOS/talsiach/take-one" take-one
link "$REPOS/shreyaskarnik/argo/skills/argo-guide" argo-guide
for base in Barty-Bart/motion-graphics mattypark/Motion-graphics-skill charlie947/motion-graphics-skills; do
  for d in "$REPOS/$base"/skills/*/; do
    link "${d%/}" "$(basename "$d")"
  done
done
