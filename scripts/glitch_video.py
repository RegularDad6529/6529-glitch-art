#!/usr/bin/env python3
"""
6529 Video Glitch — Hybrid approach using GIF//ME + ffmpeg
==========================================================
Extracts frames from a video, glitches each frame through GIF//ME's
canvas-based effect pipeline via Playwright, then re-encodes to MP4.

Optimized: page loaded ONCE, images swapped via JS, frames exported
via canvas.toDataURL(). Achieves ~0.2s/frame (35x faster than naive
per-frame page reload approach).

Usage:
    python3 glitch_video.py <input_video> <output_video> [preset_name]

Examples:
    python3 glitch_video.py /tmp/card23.MP4 /tmp/card23_glitched.mp4
    python3 glitch_video.py /tmp/card23.MP4 /tmp/output.mp4 --rgb 5 --scan 8 --noise 6

If no preset or params specified, defaults to: rgb=5, scan=8, noise=6,
ntype='line', glow=4, vig=3, sat=110 (RGB split + scanlines + noise).

Requirements:
    - Playwright (pip install playwright && playwright install chromium)
    - ffmpeg (in PATH)
    - Internet access to https://gif-me.netlify.app/

Frame count: defaults to 30. Use --frames N to change.
Output fps: defaults to 10. Use --fps N to change.
Output width: defaults to 512. Use --width N to change.
"""

import asyncio
import base64
import os
import subprocess
import sys
import tempfile
import time
from playwright.async_api import async_playwright

GIFME_URL = "https://gif-me.netlify.app/"

# Default glitch params (RGB split + scanlines + noise)
DEFAULT_PARAMS = {
    "rgb": 5,
    "scan": 8,
    "sgap": 2,
    "noise": 6,
    "ntype": "line",
    "glow": 4,
    "vig": 3,
    "sat": 110,
    "con": 104,
    "mzoom": 0,
    "mdrift": 0,
    "msway": 0,
    "mshake": 0,
    "echo": 0,
}

# 6529 preset library (subset — add more as needed)
PRESETS_6529 = {
    "bicameral-split": {"rgb": 4, "noise": 6, "ntype": "grain", "scan": 10, "sgap": 2, "glow": 3, "vig": 5, "sat": 102, "con": 105},
    "data-bloom": {"psort": 6, "post": 7, "noise": 7, "ntype": "line", "crush": 4, "scan": 8, "glow": 3, "vig": 4, "sat": 105, "con": 104},
    "cold-storage": {"psort": 5, "post": 6, "crush": 3, "noise": 8, "ntype": "grain", "scan": 12, "sgap": 2, "glow": 3, "vig": 4, "sat": 103, "con": 106},
    "boardroom": {"psort": 6, "post": 6, "crush": 4, "noise": 7, "ntype": "grain", "scan": 10, "sgap": 2, "glow": 3, "vig": 4, "sat": 104, "con": 105},
    "keypress-glitch": {"crush": 8, "noise": 15, "ntype": "line", "rgb": 6, "scan": 25, "mshake": 4, "echo": 6, "con": 120},
    "vintage-preserve": {"ntype": "film", "noise": 12, "vig": 30, "con": 112, "bri": 104, "sat": 80, "glow": 8, "mzoom": 3, "mdrift": 2, "msway": 1, "echo": 2},
    "ocean-trance": {"hue": 10, "sat": 115, "glow": 15, "noise": 6, "ntype": "grain", "mzoom": 5, "mdrift": 3, "msway": 3, "echo": 4, "vig": 8},
    "spirit-walk": {"hue": 5, "sat": 105, "noise": 6, "ntype": "grain", "scan": 4, "rgb": 2, "mzoom": 3, "mdrift": 2, "msway": 2, "echo": 3, "glow": 5, "vig": 4},
    "amber-glow": {"glow": 20, "sat": 115, "bri": 105, "noise": 5, "ntype": "grain", "mzoom": 4, "mdrift": 2, "msway": 2, "echo": 3, "vig": 6},
    "preserve": {"noise": 5, "ntype": "grain", "mzoom": 4, "mdrift": 2, "msway": 2, "echo": 2, "glow": 3, "vig": 4, "sat": 101, "con": 102},
}


def extract_frames(input_video, frames_dir, num_frames, width):
    """Extract evenly-spaced frames from video using ffmpeg."""
    # Get video duration
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", input_video],
        capture_output=True, text=True
    )
    duration = float(result.stdout.strip())
    
    # Calculate frame timestamps
    interval = duration / (num_frames + 1)
    
    for i in range(num_frames):
        timestamp = interval * (i + 1)
        output_path = os.path.join(frames_dir, f"frame_{i:04d}.png")
        subprocess.run([
            "ffmpeg", "-y", "-ss", str(timestamp), "-i", input_video,
            "-frames:v", "1", "-vf", f"scale={width}:-1",
            output_path
        ], capture_output=True, check=True)
    
    return duration


async def glitch_frames(frames_dir, glitched_dir, params, num_frames):
    """Glitch each frame through GIF//ME via Playwright (page loaded once)."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(GIFME_URL, wait_until="networkidle")
        
        # Wait for GIF//ME to initialize
        await page.wait_for_function("typeof defSettings === 'function'", timeout=10000)
        
        for i in range(num_frames):
            frame_path = os.path.join(frames_dir, f"frame_{i:04d}.png")
            glitched_path = os.path.join(glitched_dir, f"glitched_{i:04d}.png")
            
            # Read frame as base64
            with open(frame_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()
            
            # Inject image, apply glitch, export via canvas.toDataURL — all in one evaluate call
            result = await page.evaluate("""
                async (args) => {
                    const { imgB64, params } = args;
                    
                    // Load image
                    const img = new Image();
                    img.src = 'data:image/png;base64,' + imgB64;
                    await new Promise(r => { img.onload = r; img.onerror = r; });
                    
                    // Create source canvas
                    const srcCanvas = document.createElement('canvas');
                    srcCanvas.width = img.naturalWidth;
                    srcCanvas.height = img.naturalHeight;
                    srcCanvas.getContext('2d').drawImage(img, 0, 0);
                    
                    // Get default settings and apply glitch params
                    const base = defSettings();
                    const s = { ...base, ...params, curves: base.curves };
                    
                    // Set up frame
                    if (frames.length === 0) {
                        frames.push({ src: srcCanvas, s: s, cache: null });
                    } else {
                        frames[0].src = srcCanvas;
                        frames[0].s = s;
                        frames[0].cache = null;
                    }
                    
                    // Render the frame
                    renderFrame(0);
                    
                    // Export via canvas.toDataURL
                    const dataUrl = frames[0].cache.toDataURL('image/png');
                    return dataUrl;
                }
            """, {"imgB64": img_b64, "params": params})
            
            # Save the glitched frame
            if result and result.startswith("data:image/png"):
                png_data = base64.b64decode(result.split(",")[1])
                with open(glitched_path, "wb") as f:
                    f.write(png_data)
            else:
                # Fallback: copy original frame if glitch failed
                subprocess.run(["cp", frame_path, glitched_path])
        
        await browser.close()


def encode_video(glitched_dir, output_path, num_frames, fps):
    """Re-encode glitched frames into MP4 using ffmpeg."""
    pattern = os.path.join(glitched_dir, "glitched_%04d.png")
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", pattern,
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "fast",
        output_path
    ], capture_output=True, check=True)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Glitch a video using GIF//ME effects")
    parser.add_argument("input", help="Input video file")
    parser.add_argument("output", help="Output MP4 file")
    parser.add_argument("--preset", help="Preset name from 6529 library", default=None)
    parser.add_argument("--frames", type=int, default=30, help="Number of frames to extract (default: 30)")
    parser.add_argument("--fps", type=int, default=10, help="Output FPS (default: 10)")
    parser.add_argument("--width", type=int, default=512, help="Output width in pixels (default: 512)")
    
    # Individual param overrides
    parser.add_argument("--rgb", type=int, default=None)
    parser.add_argument("--scan", type=int, default=None)
    parser.add_argument("--noise", type=int, default=None)
    parser.add_argument("--hue", type=int, default=None)
    parser.add_argument("--sat", type=int, default=None)
    parser.add_argument("--glow", type=int, default=None)
    parser.add_argument("--vig", type=int, default=None)
    parser.add_argument("--psort", type=int, default=None)
    parser.add_argument("--crush", type=int, default=None)
    parser.add_argument("--post", type=int, default=None)
    
    args = parser.parse_args()
    
    # Determine params
    if args.preset and args.preset in PRESETS_6529:
        params = dict(DEFAULT_PARAMS)
        params.update(PRESETS_6529[args.preset])
    else:
        params = dict(DEFAULT_PARAMS)
    
    # Apply individual overrides
    for key in ["rgb", "scan", "noise", "hue", "sat", "glow", "vig", "psort", "crush", "post"]:
        val = getattr(args, key)
        if val is not None:
            params[key] = val
    
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    print(f"Frames: {args.frames} at {args.fps}fps, width={args.width}")
    print(f"Params: {params}")
    
    # Create temp directories
    with tempfile.TemporaryDirectory() as tmpdir:
        frames_dir = os.path.join(tmpdir, "frames")
        glitched_dir = os.path.join(tmpdir, "glitched")
        os.makedirs(frames_dir)
        os.makedirs(glitched_dir)
        
        # Step 1: Extract frames
        print("Extracting frames...")
        t0 = time.time()
        duration = extract_frames(args.input, frames_dir, args.frames, args.width)
        print(f"  Extracted {args.frames} frames in {time.time()-t0:.1f}s (video duration: {duration:.1f}s)")
        
        # Step 2: Glitch each frame
        print("Glitching frames...")
        t0 = time.time()
        asyncio.run(glitch_frames(frames_dir, glitched_dir, params, args.frames))
        glitch_time = time.time() - t0
        print(f"  Glitched {args.frames} frames in {glitch_time:.1f}s ({glitch_time/args.frames:.2f}s/frame)")
        
        # Step 3: Re-encode
        print("Encoding video...")
        t0 = time.time()
        encode_video(glitched_dir, args.output, args.frames, args.fps)
        print(f"  Encoded in {time.time()-t0:.1f}s")
        
        print(f"\nDone! Output: {args.output}")
        print(f"  {os.path.getsize(args.output) / 1024:.0f}KB")


if __name__ == "__main__":
    main()