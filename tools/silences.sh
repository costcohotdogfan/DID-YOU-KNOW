#!/usr/bin/env bash
# List the pauses in a narration file, so cuts can land on them.
# Usage: tools/silences.sh narration.mp3 [noise_dB] [min_seconds]
# Defaults (-32 dB, 0.22 s) found every sentence break in the Marcus reads.
set -euo pipefail
f="${1:?usage: silences.sh narration.mp3 [noise_dB] [min_seconds]}"
noise="${2:--32}"
min="${3:-0.22}"
echo "duration: $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")"
ffmpeg -hide_banner -i "$f" -af "silencedetect=noise=${noise}dB:d=${min}" -f null - 2>&1 \
  | grep -oE "silence_(start|end): [0-9.]+" \
  | paste - - \
  | awk '{printf "pause %6.2f -> %6.2f\n", $2, $4}'
