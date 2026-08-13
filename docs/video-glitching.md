# Video Glitching with GIF//ME (Hybrid Approach)

## Overview

GIF//ME is built for images, not video. But we can glitch video by:
1. **Extract frames** from an MP4 using ffmpeg
2. **Glitch each frame** through GIF//ME's canvas pipeline via Playwright
3. **Re-encode** glitched frames back into MP4 using ffmpeg

## Performance

| Approach | Per-frame | 30 frames | 300 frames (10s @ 30fps) |
|---|---|---|---|
| Naive (page reload per frame) | 6.9s | ~207s | ~35 min |
| Optimized (page loaded once) | 0.2s | ~6s | ~60s |

The optimized script (`scripts/glitch_video.py`) keeps the GIF//ME page loaded
and swaps images via JavaScript, then exports via `canvas.toDataURL()` instead
of download-based PNG export.

## Usage

```bash
# Basic usage with default style (RGB split + scanlines + noise)
python3 scripts/glitch_video.py input.mp4 output.mp4

# Use a 6529 preset
python3 scripts/glitch_video.py input.mp4 output.mp4 --preset bicameral-split

# Custom params
python3 scripts/glitch_video.py input.mp4 output.mp4 --rgb 8 --scan 20 --noise 10

# More frames, higher fps
python3 scripts/glitch_video.py input.mp4 output.mp4 --frames 60 --fps 30

# Larger output
python3 scripts/glitch_video.py input.mp4 output.mp4 --width 720
```

## Available Presets

From the 6529 preset library (subset included in the script):
- `bicameral-split` — RGB split + scanlines + grain (no motion)
- `data-bloom` — pixel sort + posterize + crush (no motion)
- `cold-storage` — pixel sort + posterize + crush + scanlines (no motion)
- `boardroom` — pixel sort + posterize + crush (no motion)
- `keypress-glitch` — crush + line noise + RGB + shake
- `vintage-preserve` — film grain + vignette + faded palette
- `ocean-trance` — hue shift + glow + gentle motion
- `spirit-walk` — psychedelic hue cycling + scanlines
- `amber-glow` — warm glow + gentle drift
- `preserve` — subtle grain, palette-preserving

## How It Works

### Frame Extraction
ffmpeg extracts evenly-spaced frames from the video, scaled to the target width:
```
ffmpeg -ss {timestamp} -i input.mp4 -frames:v 1 -vf scale=512:-1 frame_NNNN.png
```

### Per-Frame Glitching (Optimized)
The Playwright script:
1. Loads GIF//ME page **once** (1.5s startup)
2. For each frame:
   - Reads PNG as base64
   - Injects into GIF//ME via `new Image()` + `data:image/png;base64,...`
   - Applies glitch params to `frames[0].s`
   - Calls `renderFrame(0)` to render to canvas
   - Returns `frames[0].cache.toDataURL('image/png')` — base64 PNG
   - Saves to disk
3. Closes browser

### Re-encoding
ffmpeg stitches glitched PNGs back into MP4:
```
ffmpeg -framerate 10 -i glitched_%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4
```

## GIF//ME Frame API (from source code)

Key internals used:
- `frames` — global array of frame objects
- `frames[i].src` — source canvas (input image)
- `frames[i].s` — settings object (glitch params)
- `frames[i].cache` — rendered output canvas
- `defSettings()` — returns default settings
- `renderFrame(i)` — renders frame i to its cache canvas
- `setSetting(key, val)` — sets a param on current frame

## Limitations

- **No audio** — the output MP4 is video-only (audio is stripped)
- **Frame count affects smoothness** — 30 frames at 10fps = 3s output regardless of input duration
- **Motion params (mzoom, mdrift, etc.) have no effect** — they work across multiple frames in GIF//ME's GIF pipeline, but here each frame is independent
- **Resolution** — output width defaults to 512px. Higher = slower per frame

## Adding Audio Back

To merge the original audio with the glitched video:
```bash
ffmpeg -i glitched.mp4 -i original.mp4 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest output_with_audio.mp4
```

## Sending to Telegram

```bash
source /home/prenode/.hermes/profiles/themanager/.env
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendAnimation" \
  -F "chat_id=8798065130" \
  -F "animation=@output.mp4" \
  -F "caption=Glitched video clip"
```

## Uploading to GIPHY

GIPHY accepts MP4 uploads:
```python
import requests
GIPHY_KEY = open("/home/prenode/.hermes/profiles/themanager/.giphy_key").read().strip()
with open("output.mp4", "rb") as f:
    resp = requests.post(
        "https://upload.giphy.com/v1/gifs",
        data={"api_key": GIPHY_KEY, "tags": "tag1,tag2,...", "title": "Title"},
        files={"file": ("output.mp4", f, "video/mp4")},
        timeout=60
    )
```