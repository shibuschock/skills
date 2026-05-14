# Install these skills

Step-by-step for a first-time recipient. Should take 5–10 minutes.

## What you're installing

A bundle of seven Claude Code skills — extra `/commands` you can call inside Claude Code:

- `/daydream` — mine an Obsidian vault for non-obvious note connections
- `/humanizer` — heavy edit pass for long-form drafts (~400+ words)
- `/stop-slop` — remove AI writing patterns from prose
- `/remotion-best-practices` — reference for making videos in React with Remotion
- `/find-skills` — discover and install other agent skills
- `/huashu-design` — HTML-based prototyping and slide design (~32 MB)
- `/video-input` — analyze a local video (needs ffmpeg + whisper, optional)

The installer copies these into **your** `~/.claude/skills/` folder. It does not touch any other machine, sign you into anything, or send data anywhere.

## Step 0 — Prerequisites

You need three things on your machine. If any are missing, install them first.

### 1. Claude Code

Download and install: https://claude.com/claude-code

After install, open a terminal and run `claude --version` to confirm it works.

### 2. Git

- **Windows:** https://git-scm.com/download/win (accept all defaults)
- **macOS:** comes with Xcode Command Line Tools — if missing, run `xcode-select --install`
- **Linux:** `sudo apt install git` (Debian/Ubuntu) or `sudo dnf install git` (Fedora)

Confirm: `git --version`

### 3. (Windows only) Allow PowerShell to run local scripts

By default Windows blocks running `.ps1` files. Run this **once** in PowerShell to allow scripts signed locally:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Answer `Y` when prompted. You only need to do this once per user account, ever.

## Step 1 — Clone the repo

Open a terminal (**PowerShell** on Windows, **Terminal** on macOS/Linux) and run:

```powershell
# Windows
cd $env:USERPROFILE
git clone https://github.com/shibuschock/skills.git arend-claude-skills
cd arend-claude-skills
```

```bash
# macOS / Linux
cd ~
git clone https://github.com/shibuschock/skills.git arend-claude-skills
cd arend-claude-skills
```

If the repo is private, git will pop up a browser to sign you into GitHub the first time. Approve and continue.

## Step 2 — Run the installer

```powershell
# Windows
.\install.ps1
```

```bash
# macOS / Linux
chmod +x install.sh    # one-time, makes the script executable
./install.sh
```

By default this installs only **tier 1** skills (no extra software needed). You'll see output like:

```
[ok] daydream -> C:\Users\you\.claude\skills\daydream
[ok] humanizer -> ...
...
Installed: 6 skill(s)
```

### Install everything, including video-input

`video-input` needs `ffmpeg` and `whisper-cli` to actually work. If you want it:

```powershell
# Windows — install ffmpeg first
winget install Gyan.FFmpeg
# whisper is a manual build — see docs/DEPS.md in this repo

.\install.ps1 -All
```

```bash
# macOS
brew install ffmpeg
./install.sh --all
```

The installer will *warn* if dependencies are missing but won't fail — the skill files copy either way, only the runtime calls will fail until you install the tools.

### Other installer options

| Flag | What it does |
|---|---|
| `-DryRun` (or `--dry-run`) | Print what would happen, copy nothing |
| `-Force` (or `--force`) | Overwrite existing skill folders (use when updating) |
| `-Skills daydream,humanizer` (or `--skills daydream,humanizer`) | Cherry-pick |

## Step 3 — Verify

1. Open a **new** Claude Code session (or restart your existing one — skills are scanned at startup).
2. In the prompt, type `/` and look at the autocomplete list.
3. You should see `humanizer`, `stop-slop`, `daydream`, etc. mixed in with the built-in commands.
4. Smoke-test one: type `/humanizer` and hit enter — Claude should respond by asking what draft you want polished.

If the skills don't appear, see Troubleshooting below.

## Updating later

When new skills are added to the repo:

```powershell
cd arend-claude-skills
git pull
.\install.ps1 -Force     # or ./install.sh --force
```

## Troubleshooting

**`install.ps1 cannot be loaded because running scripts is disabled on this system`**
You skipped Step 0 #3. Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, answer `Y`, retry.

**`git: command not found`**
Step 0 #2 didn't take. Reinstall git, close and reopen your terminal.

**Skills don't appear in `/` autocomplete after install**
- Confirm files landed in the right place: `ls ~/.claude/skills/` (or `dir $env:USERPROFILE\.claude\skills` on Windows). You should see folders like `humanizer/`, `daydream/`, etc.
- Make sure you opened a **new** Claude Code session — existing sessions don't see newly installed skills until restart.
- Run `claude --version` — if it's very old, update Claude Code.

**`Permission denied` when running `./install.sh` on macOS/Linux**
Run `chmod +x install.sh` once, then retry.

**Authentication popup loops when cloning**
Means you don't have access to the private repo. Ask the repo owner to add your GitHub username as a collaborator at https://github.com/shibuschock/skills/settings/access.

## Uninstalling

Delete the relevant folders inside `~/.claude/skills/`. That's it — no registry entries, no service, no leftover state.

```powershell
# Windows — remove a specific skill
Remove-Item -Recurse $env:USERPROFILE\.claude\skills\humanizer
```

```bash
# macOS / Linux
rm -rf ~/.claude/skills/humanizer
```

## Questions / problems

Open an issue at https://github.com/shibuschock/skills/issues or contact the person who sent you here.
