#!/usr/bin/env bash
# Install Arend's Claude Code skills into ~/.claude/skills/ on POSIX systems.
# Usage:
#   ./install.sh                # tier 1 only (default, safest)
#   ./install.sh --all          # tier 1 + tier 2
#   ./install.sh --skills daydream,humanizer
#   ./install.sh --dry-run --all
#   ./install.sh --force        # overwrite existing
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST="$SCRIPT_DIR/manifest.json"
SKILLS_SRC="$SCRIPT_DIR/skills"
TARGET="${HOME}/.claude/skills"

MODE="core"          # core | all | list
SELECTED=""
DRY_RUN=0
FORCE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --all)        MODE="all"; shift ;;
    --core-only)  MODE="core"; shift ;;
    --skills)     MODE="list"; SELECTED="$2"; shift 2 ;;
    --target)     TARGET="$2"; shift 2 ;;
    --dry-run)    DRY_RUN=1; shift ;;
    --force)      FORCE=1; shift ;;
    -h|--help)
      sed -n '2,11p' "$0"; exit 0 ;;
    *)
      echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

if [[ ! -f "$MANIFEST" ]]; then
  echo "manifest.json not found at $MANIFEST" >&2
  exit 1
fi

# Need a JSON reader. Prefer jq; fall back to python3.
read_skills() {
  if command -v jq >/dev/null 2>&1; then
    case "$MODE" in
      core) jq -r '.skills[] | select(.tier==1) | .name' "$MANIFEST" ;;
      all)  jq -r '.skills[] | .name' "$MANIFEST" ;;
      list) printf '%s\n' ${SELECTED//,/ } ;;
    esac
  elif command -v python3 >/dev/null 2>&1; then
    python3 - "$MANIFEST" "$MODE" "$SELECTED" <<'PY'
import json, sys
m, mode, selected = sys.argv[1], sys.argv[2], sys.argv[3]
with open(m) as f: data = json.load(f)
if mode == "core":
    names = [s["name"] for s in data["skills"] if s["tier"] == 1]
elif mode == "all":
    names = [s["name"] for s in data["skills"]]
else:
    names = [n.strip() for n in selected.split(",") if n.strip()]
print("\n".join(names))
PY
  else
    echo "Need jq or python3 to read manifest.json" >&2
    exit 1
  fi
}

skill_tier() {
  local name="$1"
  if command -v jq >/dev/null 2>&1; then
    jq -r --arg n "$name" '.skills[] | select(.name==$n) | .tier' "$MANIFEST"
  else
    python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(next((s['tier'] for s in d['skills'] if s['name']==sys.argv[2]), ''))" "$MANIFEST" "$name"
  fi
}

skill_binaries() {
  local name="$1"
  if command -v jq >/dev/null 2>&1; then
    jq -r --arg n "$name" '.skills[] | select(.name==$n) | .binaries[]' "$MANIFEST"
  else
    python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print('\n'.join(next((s['binaries'] for s in d['skills'] if s['name']==sys.argv[2]), [])))" "$MANIFEST" "$name"
  fi
}

mapfile -t REQUESTED < <(read_skills)
if [[ ${#REQUESTED[@]} -eq 0 ]]; then
  echo "No skills selected." >&2; exit 1
fi

echo ""
echo "Install target : $TARGET"
echo "Mode           : $([[ $DRY_RUN -eq 1 ]] && echo 'DRY RUN' || echo 'EXECUTE')"
echo "Force          : $FORCE"
echo "Skills selected: ${REQUESTED[*]}"
echo ""

[[ $DRY_RUN -eq 0 ]] && mkdir -p "$TARGET"

# Tier 2 binary probe
declare -A SEEN_BINS
for name in "${REQUESTED[@]}"; do
  tier="$(skill_tier "$name")"
  [[ "$tier" != "2" ]] && continue
  while IFS= read -r bin; do
    [[ -z "$bin" ]] && continue
    SEEN_BINS["$bin"]=1
  done < <(skill_binaries "$name")
done

if [[ ${#SEEN_BINS[@]} -gt 0 ]]; then
  echo "Checking tier-2 binary dependencies..."
  for bin in "${!SEEN_BINS[@]}"; do
    if command -v "$bin" >/dev/null 2>&1; then
      echo "  [ok]      $bin found"
    else
      echo "  [missing] $bin"
      case "$bin" in
        ffmpeg|ffprobe) echo "    install: apt install ffmpeg  /  brew install ffmpeg" ;;
        whisper*)       echo "    install: build whisper.cpp (https://github.com/ggerganov/whisper.cpp)" ;;
      esac
    fi
  done
  echo ""
fi

# Copy loop
INSTALLED=()
SKIPPED=()
for name in "${REQUESTED[@]}"; do
  src="$SKILLS_SRC/$name"
  dst="$TARGET/$name"
  if [[ ! -d "$src" ]]; then
    echo "[warn] source missing: $src"
    SKIPPED+=("$name [source missing]")
    continue
  fi
  if [[ -d "$dst" ]]; then
    if [[ $FORCE -eq 0 ]]; then
      echo "[skip] $name already at $dst (use --force to overwrite)"
      SKIPPED+=("$name [exists]")
      continue
    fi
    [[ $DRY_RUN -eq 0 ]] && rm -rf "$dst"
  fi
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "[dry-run] would copy $src -> $dst"
  else
    cp -r "$src" "$dst"
    echo "[ok] $name -> $dst"
  fi
  INSTALLED+=("$name")
done

echo ""
echo "==================== Summary ===================="
echo "Installed: ${#INSTALLED[@]} skill(s)$([[ $DRY_RUN -eq 1 ]] && echo ' (DRY RUN - nothing copied)')"
for n in "${INSTALLED[@]}"; do echo "  + $n"; done
if [[ ${#SKIPPED[@]} -gt 0 ]]; then
  echo "Skipped:"
  for n in "${SKIPPED[@]}"; do echo "  - $n"; done
fi
echo ""
if [[ $DRY_RUN -eq 0 && ${#INSTALLED[@]} -gt 0 ]]; then
  echo "Next steps:"
  echo "  1. Start a new Claude Code session (or restart your current one)."
  echo "  2. Type / and verify the skill names appear in autocomplete."
fi
