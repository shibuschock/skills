# arend-claude-skills

Personal Claude Code skills, packaged for transfer to a fresh machine (e.g. enterprise laptop).

## What's in here

Twenty-four entries. The original seven are split by external-binary dependency; the **OCM suite** adds sixteen Python-library skills (plus one shared folder) covering the full change-management lifecycle.

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

### OCM suite — needs Python libraries (`pip install`)

Sixteen portable organizational-change-management skills (client-agnostic, cross-platform, conversational) covering the full change lifecycle. They run Python to render Office/HTML deliverables from workshop transcripts / a CIA. Install their libs once: `pip install openpyxl python-docx python-pptx`. Render scripts refuse to overwrite existing outputs unless `--force`. The whole suite was simulation-tested end-to-end (July 2026) — every skill exercised by practitioner agents on a synthetic engagement, defects fixed.

**Start here:** `docs/OCM Skill Suite Overview.html` — interactive catalog (what each skill does, when to use it, example asks) — and `docs/OCM-SUITE-README.md` for the pipeline and conventions.

| Skill | What it does |
|---|---|
| **cia-builder** | Change Impact Assessment (6 MECE Change Dimensions) -> Excel workbook + interactive HTML dashboard. The foundation the others chain from. |
| **sha-builder** | Stakeholder Assessment (Influence x Interest / Mendelow) -> Excel + HTML with engagement grid. |
| **tom-vro-builder** | Target Operating Model + Value Realization accelerator -> PPTX slide + Word approach doc + Excel VRO registers + HTML dashboard. |
| **comms-toolkit** | Change-comms operation from a CIA -> comms master grid (Excel) + dashboard (HTML) + coverage matrix (GAP flags) + plain-language QA + Markdown templates. |
| **change-network-builder** | Champion/change-agent network: roster + coverage dashboard, nomination/onboarding/touchpoint templates. |
| **adoption-metrics-builder** | Adoption & success measurement: metric-ladder register + dashboard; flags CIA value levers with no metric. |
| **readiness-pulse-builder** | Pulse survey design (question bank, anonymity discipline) + readiness readout dashboards from results. |
| **persona-journey-builder** | Tiered personas, current->future journeys, day-in-the-life narratives from CIA/SHA data. |
| **ocm-playbook-builder** | OCM playbook + 90-day tactical plan: swimlane dashboard + activity register with GAP flags. |
| **ocm-readout-builder** | Executive readouts: Change Intensity Map (derived from the CIA), who/what/how theme boards, leader talking points. |
| **training-strategy-builder** | Training strategy upstream of the TNA: principles, modality-by-workforce matrix, governance, phasing. |
| **training-needs-builder** | TNA from change impacts: audience x capability matrix + dashboard (no hours — that's curriculum-stage). |
| **curriculum-architect** | Curriculum blueprint: learning paths, Bloom-aligned modules, 70-20-10 blend, prerequisites. |
| **training-content-builder** | Per-module deliverables: facilitator/participant guides, job aids, slide outlines, assessments. |
| **interactive-learning-builder** | Gamified quizzes + flashcards as self-contained HTML, optional SCORM 1.2 packaging. |
| **training-rollout-builder** | Training deployment: waves anchored to go-lives, readiness gates, Kirkpatrick L1-L4, reinforcement. |
| _`_training-shared`_ | Shared adult-learning methodology + per-project context template the training skills read. Install it alongside them. |

## Quickstart

> First time on a new machine? See **[INSTALL.md](INSTALL.md)** for the full step-by-step (prereqs, troubleshooting, uninstall).

### Windows (PowerShell)

```powershell
git clone https://github.com/shibuschock/skills.git arend-claude-skills
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
git clone https://github.com/shibuschock/skills.git arend-claude-skills
cd arend-claude-skills
chmod +x install.sh
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
