---
name: video-input
description: Analyze a local video file by extracting frames at a chosen fps, extracting audio, transcribing it with whisper.cpp, and correlating frames with transcript timestamps so Claude can review the video as images plus text. Use when the user asks to "analyze", "watch", "review", or "transcribe" a video file, or wants to feed video content to Claude for understanding. Requires ffmpeg, ffprobe, and whisper-cpp installed locally.
---

# video-input

Claude cannot natively view video, but can view images and read text. This skill bridges that gap by decomposing a video file into:

- **Frames** (PNG stills at a configurable fps) — readable via the Read tool as images
- **Audio transcription** (SRT with timestamps) — produced by whisper.cpp
- **Frame ↔ transcript map** — correlates each sampled frame to what was being said at that moment
- **`analysis.md`** — a summary index of everything generated

Everything lands in an isolated, timestamped workspace under `$CLAUDE_PROJECT_DIR/.video-input/analysis_<timestamp>/` so multiple runs don't collide.

## When to use

Invoke this skill when the user:

- Hands you a path to a video file (`.mp4`, `.mov`, `.mkv`, `.webm`, …) and wants you to understand its content
- Asks to "watch", "analyze", "summarize", "transcribe", or "review" a video
- Wants frame-accurate references to what was said at a specific moment

Do **not** invoke for audio-only files (use whisper directly) or for videos already decomposed into frames.

## How to run

The skill ships two equivalent implementations — pick the one that matches the host:

- **Windows (PowerShell 7+)** — preferred on native Windows:
  ```powershell
  pwsh ~/.claude/skills/video-input/analyze-video.ps1 <path-to-video> [fps] [whisper-model]
  ```
- **macOS / Linux / WSL / Git Bash**:
  ```bash
  bash ~/.claude/skills/video-input/analyze-video.sh <path-to-video> [fps] [whisper-model]
  ```

Arguments (positional, identical in both versions):

| Arg | Default | Meaning |
|---|---|---|
| `<path-to-video>` | required | Absolute or relative path to the video file |
| `[fps]` | `1` | Frames extracted per second. Raise for fast-motion content; lower for talking-head videos |
| `[whisper-model]` | `base` | whisper.cpp model name. One of `tiny`, `base`, `small`, `medium`, `large`. Larger = more accurate, slower |

Environment:

- `CLAUDE_PROJECT_DIR` — workspace root. If unset, the script uses the current working directory.
- `WHISPER_MODEL_DIR` — directory containing `ggml-<model>.bin`. Defaults to `~/.cache/whisper` or `~/.local/share/whisper-cpp`.

## Prerequisites

The script checks these and exits with a clear error if any are missing:

- `ffmpeg` and `ffprobe` on `PATH`
- `whisper`, `whisper-cli`, or `whisper.cpp` on `PATH`
  - macOS: `brew install whisper-cpp`
  - Windows: build from https://github.com/ggerganov/whisper.cpp or install via a package manager that puts `whisper` / `whisper-cli` on PATH

The whisper model file (`ggml-<model>.bin`) is **auto-downloaded on first run** from https://huggingface.co/ggerganov/whisper.cpp into `$WHISPER_MODEL_DIR` if missing. No manual download needed — just make sure you have network access the first time you run a given model size.

## What you get

After a successful run, the workspace contains:

```
.video-input/analysis_<timestamp>/
├── video_file.<ext>              # Copy of the source video
├── frames/frame_0001.png …       # Extracted frames at chosen fps
├── audio.wav                     # 16kHz mono PCM (or placeholder if no audio)
├── transcription.srt             # Timestamped transcript
├── frame_transcription_map.txt   # Every 5th frame ↔ transcript text
├── metadata.txt                  # Duration, resolution, format, audio status
├── analysis.md                   # Human-readable summary — start here
└── .completed                    # Marker file written on success
```

**Start with `analysis.md`.** It links to the transcription preview and a frame-timeline table. From there, use the Read tool to view specific frames as images (`frames/frame_NNNN.png`) and cross-reference them against `frame_transcription_map.txt`.

## Frame-timestamp math

Frame numbers are 1-indexed. To convert:

- `timestamp_seconds = (frame_number - 1) / fps`
- At `fps=1`, `frame_0045.png` corresponds to 44 seconds into the video.

Use this to jump directly to a frame when the user references a moment in the transcript.

## Failure modes to watch for

- **No audio stream** — script still extracts frames and writes a placeholder `transcription.srt`. `analysis.md` will flag this.
- **Missing model file** — script exits with the exact `curl` command to download it.
- **Huge videos at high fps** — frame count can explode. Default `fps=1` is deliberate; only raise it when the user asks for motion detail.
