#!/usr/bin/env python3
"""Pull one clean frame per screen out of a screen recording.

Usage:
  python3 extract_frames.py recording.mp4 --out-dir <scratch>/candidates [--fps 3] [--new 6] [--settle 2] [--max 80]

How it works (needs ffmpeg and ffprobe, no other packages):
  1. Samples the video at --fps into tiny grey thumbnails.
  2. A frame is "settled" when it barely differs from the one before it (the screen stopped moving).
  3. A settled frame is kept when it differs enough (--new) from the last kept frame, so repeats are dropped.
  4. Each kept frame is cut at full size from the video as a JPEG, and a manifest lists the times.
Write the output OUTSIDE the project folder first. The owner approves frames before they go into work/assets/.
"""
import argparse, json, os, shutil, subprocess, sys

W, H = 48, 96  # thumbnail size used only for comparing frames


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, **kw)


def duration(video):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video]).stdout
    return float(out.decode().strip())


def thumbs(video, fps):
    raw = run(["ffmpeg", "-v", "error", "-i", video, "-vf", f"fps={fps},scale={W}:{H},format=gray", "-f", "rawvideo", "-"]).stdout
    n = len(raw) // (W * H)
    return [raw[i * W * H:(i + 1) * W * H] for i in range(n)]


def diff(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


def pick(frames, new, settle):
    kept = []  # indexes
    for i in range(1, len(frames)):
        if diff(frames[i - 1], frames[i]) > settle:
            continue  # still moving
        if not kept or diff(frames[kept[-1]], frames[i]) > new:
            kept.append(i)
    return kept


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--fps", type=float, default=3, help="samples per second (default 3)")
    ap.add_argument("--new", type=float, default=6, help="how different a frame must be from the last kept one, 0 to 255 (default 6; lower keeps more)")
    ap.add_argument("--settle", type=float, default=2, help="how still the screen must be, 0 to 255 (default 2; higher accepts slower animations)")
    ap.add_argument("--max", type=int, default=80, help="stop with an error if more frames than this are found")
    a = ap.parse_args()
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            sys.exit(f"{tool} not found. Install it first, for example: brew install ffmpeg")
    if not os.path.exists(a.video):
        sys.exit(f"video not found: {a.video}")
    os.makedirs(a.out_dir, exist_ok=True)
    frames = thumbs(a.video, a.fps)
    kept = pick(frames, a.new, a.settle)
    if len(kept) > a.max:
        sys.exit(f"{len(kept)} frames found (limit {a.max}). Raise --new (for example {a.new * 2:g}) and run again.")
    manifest = []
    for k, i in enumerate(kept, 1):
        t = i / a.fps
        name = f"cand-{k:03d}-t{t:06.1f}s.jpg"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", a.video, "-frames:v", "1", "-q:v", "2", os.path.join(a.out_dir, name)])
        manifest.append({"file": name, "time_s": round(t, 1)})
    json.dump({"video": os.path.basename(a.video), "duration_s": round(duration(a.video), 1), "fps": a.fps, "new": a.new, "settle": a.settle,
               "frames": manifest}, open(os.path.join(a.out_dir, "manifest.json"), "w"), indent=1)
    print(f"{len(manifest)} candidate frames from {len(frames)} samples -> {a.out_dir}")
    print("Next: look at every frame, drop duplicates and transitions, blur personal details, then name and move the keepers.")


if __name__ == "__main__":
    main()
