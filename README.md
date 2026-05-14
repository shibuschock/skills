# arend-claude-skills

Personal Claude Code skills, packaged for transfer to a fresh machine (e.g. enterprise laptop).

## What's in here

Seven skills, split into two tiers based on external dependencies.

### Tier 1 — pure markdown, zero deps (safe on locked-down laptops)

| Skill | What it does |
|---|---|
| **daydream** | Multi-agent default-mode-network simulation over an Obsidian vault; samples note pairs, synthesizes connections, critic-filters. |
| **humanizer** | Heavy edit pass for long-form drafts (book chapters, decks, articles). Two-pass audit removing AI patterns, optional voice calibration. MIT, version 2.5.1. |
| **stop-slop** | Removes AI writing tells from prose — cuts filler, breaks formulaic structures, enforces active voice. Third-party (Hardik Pandya, MIT). |
| **remotion-best-practices** | Reference guide for [Remotion](https://www.remotion.dev/) video creation in React. Optional npm/Node only at use time, not install time. |
| **find-skills** | Helps discover and install other agent skills from the ecosystem. |
| **huashu-design** | 花叔Design — HTML-based high-fidelity prototyping, slide design, interactive demos. **~32 MB** (includes HTML demos + assets). Optional Playwright/Node only at use time. |

### Tier 2 — needs external binaries

| Skill | Needs | Install hint |
|---|---|---|
| **video-input** | `ffmpeg`, `ffprobe`, `whisper-cli` | `winget install Gyan.FFmpeg` + build [whisper.cpp](https://github.com/ggerganov/whisper.cpp) |

## Quickstart

### Windows (PowerShell)

```powershell
git clone <your-private-repo-url> arend-claude-skills
cd arend-claude-skills

# Tier 1 only (safest on a fresh/locked-down laptop)
.\install.ps1

# Everything (will warn if ffmpeg/whisper missing, doesn't fail)
.\install.ps1 -All

# Cherry-pick
.\install.ps1 -Skills daydream,humanizer

# See what would happen, copy nothing
.\install.ps1 -DryRun -All
```

### macOS / Linux

```bash
./install.sh             # tier 1
./install.sh --all       # everything
./install.sh --skills daydream,humanizer
./install.sh --dry-run --all
```

### Verify

1. Start a **new** Claude Code session.
2. Type `/` in the prompt — installed skill names should appear in autocomplete.
3. Smoke-test one: drop a short draft into a scratch file, run `/humanizer`.

## Updating

```powershell
git pull
.\install.ps1 -Force        # overwrites existing skill folders
```

## Repo layout

```
arend-claude-skills/
├── README.md              ← you are here
├── install.ps1            ← Windows installer (primary)
├── install.sh             ← POSIX installer
├── manifest.json          ← skill list + tier + deps + sha256
├── skills/                ← skill folders (copied verbatim into ~/.claude/skills/)
│   ├── daydream/
│   ├── humanizer/
│   ├── stop-slop/
│   ├── remotion-best-practices/
│   ├── find-skills/
│   ├── huashu-design/
│   └── video-input/       ← tier 2
└── docs/
    ├── ENTERPRISE.md      ← per-skill enterprise-deployment notes
    └── DEPS.md            ← ffmpeg / whisper install hints
```

## What's NOT in this bundle

Intentionally excluded:

- **Custom subagents** (`mempalace-librarian`, `outline-builder`, `prose-reviewer`) — not part of the original ask.
- **Custom slash commands** (`process-inbox`, `process-next`, `ingest-url`, `lint-wiki`) — hardcoded to `G:\My Drive\G Vault`; would need a rewrite for a different workspace.
- **MemPalace MCP setup** — separate Python install + MCP config; documented in `docs/ENTERPRISE.md` if you want to recreate it.
- **Anthropic-shipped skills** (`init`, `review`, `security-review`, `simplify`, etc.) — already ship with Claude Code.
- **Plugins** (`ui-ux-pro-max`) — installable separately via `/plugin add`.

## Licenses

- `humanizer/LICENSE` — MIT
- `stop-slop/LICENSE` — MIT (Hardik Pandya)
- `huashu-design/LICENSE` — check before redistributing publicly
- Everything else: personal use, no formal license declared
