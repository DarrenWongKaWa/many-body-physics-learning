#!/bin/bash
# usage: tools_sheet.sh video.mp4 out.png [n=12]
v=$1; out=$2; n=${3:-12}
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v")
tmp=$(mktemp -d)
for i in $(seq 0 $((n-1))); do
  t=$(python3 -c "print($d*($i+0.5)/$n)")
  ffmpeg -v error -ss $t -i "$v" -frames:v 1 -vf scale=480:-1 "$tmp/f$(printf %02d $i).png"
done
ffmpeg -v error -y -pattern_type glob -i "$tmp/f*.png" -vf "tile=4x$(( (n+3)/4 ))" "$out"
rm -rf "$tmp"; echo "$d s"
