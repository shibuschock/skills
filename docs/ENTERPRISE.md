# Enterprise deployment notes

Per-skill: what permissions and binaries each skill needs to actually *function* on an enterprise-managed laptop. The installer copies the files regardless; this doc is about whether the skill will work after install.

## Permissions required on the laptop

| Capability | Why | Required for |
|---|---|---|
| Install Claude Code CLI | Host for everything | All skills |
| Write to `~\.claude\skills\` | Where the installer copies to | All skills |
| Run `git clone` over HTTPS | Pull this repo | Install method |
| Run `winget` (or admin install) | ffmpeg | Tier 2 only |
| Outbound HTTPS | Anthropic API + npm/pip if you build downstream | Anything actually doing work |

If `winget` is blocked: ffmpeg has a portable build (single `.exe`, drop on PATH) that works without admin. Same for whisper.cpp (it's a single binary after compile).

## Per-skill notes

### daydream (Tier 1)
- **Works out of the box** after install.
- Designed to run against an Obsidian vault. Paths are relative — point it at any vault folder when invoking.
- Multi-agent skill: uses Claude Sonnet + Haiku internally via the standard Claude Code agent system. No extra config.

### humanizer (Tier 1)
- **Works out of the box.**
- For drafts ~400+ words with layout (headings/lists). Use `stop-slop` for short prose instead.
- Optional voice calibration: paste a writing sample of your own; humanizer aligns to it.

### stop-slop (Tier 1)
- **Works out of the box.**
- Triggered when drafting/editing/reviewing prose. Lightweight.
- Bundles a `references/` folder with phrase/structure lists.

### remotion-best-practices (Tier 1 to install, Tier 2-ish to use)
- Skill files install fine.
- To actually *make* a video you need Node + npm + the Remotion CLI in a separate project. Skill itself is reference material — it tells Claude *how* to write Remotion code, it doesn't run Remotion.
- `ELEVENLABS_API_KEY` mentioned in `rules/voiceover.md` is a *documentation example*, not a leaked key.

### find-skills (Tier 1)
- **Works out of the box.**
- Wraps `npx skills` interaction. If `npx` is unavailable, the skill can still describe options; install actions require npx.

### huashu-design (Tier 1 to install, may need Node to fully use)
- Skill files install fine (~32 MB, mostly HTML demos under `demos/` and assets).
- Heavy use cases (running Playwright validation, exporting MP4/GIF via ffmpeg) need: Node + Playwright + ffmpeg. Without them you can still use the design-direction advisor / static HTML prototyping parts.
- Bilingual: README is in Chinese with an English variant (`README.en.md`).

### video-input (Tier 2)
- **Will not function without ffmpeg + ffprobe + whisper-cli.**
- Both PowerShell (`analyze-video.ps1`) and bash (`analyze-video.sh`) implementations ship. PowerShell is primary on Windows.
- Whisper model file is downloaded on first run (or supplied via `--model`). Default is `ggml-base.en.bin` (~140 MB). Make sure outbound HTTPS to huggingface.co works, or pre-download and side-load.
- See `docs/DEPS.md` for install hints.

## MemPalace (not in this bundle, but you may want it)

If you want the SessionStart hook that shows your MemPalace status on launch, you need to recreate three things on the enterprise box:

1. **Python 3.13** installed and on PATH.
2. **MemPalace MCP server** — installed separately (your own work).
3. **`~/.claude/settings.json`** with the `SessionStart` hook entry pointing at the `mempalace.exe` binary. Not packaged here because it's user-specific.

Without MemPalace the SessionStart banner is missing, but no skill in this bundle requires it.

## Network requirements

Skills don't make network calls themselves (other than the Anthropic API that Claude Code already needs). The exception is:

- **video-input** when first downloading the whisper model
- **find-skills** when fetching the skill registry via `npx skills`
- **huashu-design** when Playwright downloads browser binaries (only if you run validation)

All are HTTPS to standard public domains; no enterprise proxy gymnastics expected beyond what Claude Code already needs.
