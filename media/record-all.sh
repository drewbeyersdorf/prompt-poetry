#!/bin/bash
# Record all YouTube Shorts as asciinema .cast files
# Then convert to GIF with agg or MP4 with ffmpeg
#
# Usage: ./media/record-all.sh
# Output: media/shorts/*.cast (terminal recordings)
#
# To convert to GIF: agg shorts/01-intro.cast shorts/01-intro.gif --cols 60 --rows 30
# To convert to MP4: ffmpeg -i shorts/01-intro.gif -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" shorts/01-intro.mp4

set -e
cd "$(dirname "$0")"

echo "Recording 5 YouTube Shorts..."
echo ""

for i in 01-intro 02-pipe-operator 03-anti-hallucination 04-presets 05-cli; do
    echo "Recording $i..."
    asciinema rec \
        --cols 60 \
        --rows 30 \
        --command "cd .. && uv run python media/shorts/${i}.py" \
        --overwrite \
        "shorts/${i}.cast"
    echo "  -> shorts/${i}.cast"
    echo ""
done

echo "Done. 5 recordings at media/shorts/*.cast"
echo ""
echo "Next steps:"
echo "  1. Install agg: cargo install --git https://github.com/asciinema/agg"
echo "  2. Convert to GIF: agg shorts/01-intro.cast shorts/01-intro.gif"
echo "  3. Upload GIFs to GitHub or convert to MP4 for YouTube"
