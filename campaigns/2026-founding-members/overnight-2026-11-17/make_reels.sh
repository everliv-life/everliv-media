#!/bin/bash
# Reels: still frames -> 1080x1920 H.264 with crossfades and a slow push-in. No audio (add licensed in-app music).
cd "$(dirname "$0")/assets"; mkdir -p video
mk(){ out=$1; shift; n=$#; d=3.4; x=0.6; args=(); fc=""; i=0
  for f in "$@"; do args+=(-i "$f"); fc+="[$i:v]scale=1188:2112,zoompan=z='min(zoom+0.0008,1.06)':d=$(python3 -c "print(int($d*30))"):s=1080x1920:fps=30,setsar=1,format=yuv420p[v$i];"; i=$((i+1)); done
  prev="v0"; off=$(python3 -c "print($d-$x)")
  for ((k=1;k<n;k++)); do fc+="[$prev][v$k]xfade=transition=fade:duration=$x:offset=$off[x$k];"; prev="x$k"; off=$(python3 -c "print($off+$d-$x)"); done
  ffmpeg -y -loglevel error "${args[@]}" -filter_complex "${fc%;}" -map "[$prev]" -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -movflags +faststart "video/$out.mp4"; echo "video/$out.mp4"; }
mk A02-teaser-reel A02-teaser-reel_f1.png A02-teaser-reel_f2.png A02-teaser-reel_f3.png A02-teaser-reel_f4.png
mk A04R-reveal-reel A04R-reveal-reel_f1.png A04R-reveal-reel_f2.png A04R-reveal-reel_f3.png A04R-reveal-reel_f4.png
mk B01R-bf-reel B01R-bf-reel_f1.png B01R-bf-reel_f2.png B01R-bf-reel_f3.png B01R-bf-reel_f4.png
mk C19-math-reel C19-math-reel_f1.png C19-math-reel_f2.png C19-math-reel_f3.png C19-math-reel_f4.png
mk C02R-gift-reel C02R-gift-reel_f1.png C02R-gift-reel_f2.png C02R-gift-reel_f3.png C02R-gift-reel_f4.png
mk C16-last-minute-reel C16-last-minute-reel_f1.png C16-last-minute-reel_f2.png C16-last-minute-reel_f3.png
mk D03-morning-ritual-reel D03-morning-ritual-reel_f1.png D03-morning-ritual-reel_f2.png D03-morning-ritual-reel_f3.png D03-morning-ritual-reel_f4.png
