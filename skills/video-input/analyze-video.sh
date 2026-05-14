#!/bin/bash

# Video Analysis Script
# This script ensures all steps are executed in order without skipping
# Usage: ./analyze-video.sh <path-to-video-file> [fps] [whisper-model]

set -euo pipefail  # Exit on error, undefined variables, and pipe failures

# Configuration
VIDEO_PATH="${1:-}"
FPS="${2:-1}"  # Default: 1 frame per second
WHISPER_MODEL="${3:-base}"  # Default: base model
# Model directory - check common locations
if [[ -d "$HOME/.cache/whisper" ]]; then
    WHISPER_MODEL_DIR="${WHISPER_MODEL_DIR:-$HOME/.cache/whisper}"
elif [[ -d "$HOME/.local/share/whisper-cpp" ]]; then
    WHISPER_MODEL_DIR="${WHISPER_MODEL_DIR:-$HOME/.local/share/whisper-cpp}"
else
    WHISPER_MODEL_DIR="${WHISPER_MODEL_DIR:-$HOME/.cache/whisper}"
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Function to check if command exists
check_command() {
    if ! command -v "$1" &> /dev/null; then
        print_error "Required command '$1' not found. Please install it first."
        exit 1
    fi
}

# Function to verify file exists
verify_file() {
    if [[ ! -f "$1" ]]; then
        print_error "File not found: $1"
        exit 1
    fi
    print_success "File verified: $1"
}

# Function to verify directory exists
verify_directory() {
    if [[ ! -d "$1" ]]; then
        print_error "Directory not found: $1"
        exit 1
    fi
    print_success "Directory verified: $1"
}

# Function to parse SRT file and extract segments
# Returns format: timestamp_start|timestamp_end|text
parse_srt() {
    local srt_file="$1"
    awk '
    BEGIN { RS=""; FS="\n" }
    {
        if (NF >= 3) {
            # Extract timestamps from line 2
            split($2, times, " --> ")
            start = times[1]
            end = times[2]

            # Extract text from line 3 onwards
            text = ""
            for (i = 3; i <= NF; i++) {
                text = text $i " "
            }

            print start "|" end "|" text
        }
    }' "$srt_file"
}

# Function to convert SRT timestamp to seconds
srt_to_seconds() {
    local timestamp="$1"
    # Format: 00:01:23,456 -> extract HH:MM:SS
    local time_part="${timestamp%,*}"  # Remove milliseconds

    IFS=':' read -r hours minutes seconds <<< "$time_part"
    echo "$((10#$hours * 3600 + 10#$minutes * 60 + 10#$seconds))"
}

# Function to format seconds as HH:MM:SS
seconds_to_timestamp() {
    local total_seconds="$1"
    local hours=$((total_seconds / 3600))
    local minutes=$(((total_seconds % 3600) / 60))
    local seconds=$((total_seconds % 60))
    printf "%02d:%02d:%02d" "$hours" "$minutes" "$seconds"
}

# Function to match frame number to transcription
match_frame_to_transcript() {
    local frame_num="$1"
    local fps="$2"
    local srt_data="$3"

    # Calculate frame timestamp in seconds (frame numbers start at 1)
    local frame_seconds=$(( (frame_num - 1) / fps ))

    # Find matching SRT segment
    while IFS='|' read -r start_time end_time text; do
        local start_sec=$(srt_to_seconds "$start_time")
        local end_sec=$(srt_to_seconds "$end_time")

        if [ "$frame_seconds" -ge "$start_sec" ] && [ "$frame_seconds" -lt "$end_sec" ]; then
            echo "$text"
            return 0
        fi
    done <<< "$srt_data"

    echo "[No transcription at this timestamp]"
}

# Validate input
if [[ -z "$VIDEO_PATH" ]]; then
    print_error "Usage: $0 <path-to-video-file> [fps] [whisper-model]"
    echo "Example: $0 /path/to/video.mp4 1 base"
    exit 1
fi

# Check if CLAUDE_PROJECT_DIR is set
if [[ -z "${CLAUDE_PROJECT_DIR:-}" ]]; then
    print_warning "CLAUDE_PROJECT_DIR not set, using current directory"
    CLAUDE_PROJECT_DIR="$(pwd)"
fi

print_step "Starting video analysis..."
echo "Video: $VIDEO_PATH"
echo "FPS: $FPS"
echo "Whisper Model: $WHISPER_MODEL"
echo "Project Dir: $CLAUDE_PROJECT_DIR"
echo ""

# Step 0: Check dependencies
print_step "Checking dependencies..."
check_command ffmpeg
# Check for whisper - try multiple possible command names
WHISPER_CMD=""
if command -v whisper &> /dev/null; then
    WHISPER_CMD="whisper"
elif command -v whisper-cli &> /dev/null; then
    WHISPER_CMD="whisper-cli"
elif command -v whisper.cpp &> /dev/null; then
    WHISPER_CMD="whisper.cpp"
else
    print_error "Whisper not found. Install whisper.cpp: brew install whisper-cpp"
    exit 1
fi
print_success "Found whisper command: $WHISPER_CMD"
check_command ffprobe
print_success "All dependencies available"

# Check for model file, auto-download if missing
MODEL_FILE="${WHISPER_MODEL_DIR}/ggml-${WHISPER_MODEL}.bin"
if [[ ! -f "$MODEL_FILE" ]]; then
    print_warning "Whisper model not found locally: $MODEL_FILE"
    check_command curl
    mkdir -p "$WHISPER_MODEL_DIR"
    MODEL_URL="https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-${WHISPER_MODEL}.bin"
    print_step "Downloading model from $MODEL_URL ..."
    if ! curl -L --fail --progress-bar -o "$MODEL_FILE" "$MODEL_URL"; then
        print_error "Failed to download model. Check your network or try a different model name (tiny/base/small/medium/large)."
        rm -f "$MODEL_FILE"
        exit 1
    fi
    print_success "Model downloaded: $MODEL_FILE"
else
    print_success "Model file found: $MODEL_FILE"
fi
echo ""

# Step 1: Verify input video exists
print_step "Verifying input video..."
verify_file "$VIDEO_PATH"
VIDEO_NAME=$(basename "$VIDEO_PATH")
echo ""

# Step 2: Create isolated working directory
print_step "Creating isolated workspace..."
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
WORK_DIR="${CLAUDE_PROJECT_DIR}/.video-input/analysis_${TIMESTAMP}"

mkdir -p "${WORK_DIR}/frames"
verify_directory "${WORK_DIR}"
verify_directory "${WORK_DIR}/frames"
print_success "Created: ${WORK_DIR}"
echo ""

# Step 3: Copy video file (preserve original extension)
print_step "Copying video to workspace..."
VIDEO_EXT="${VIDEO_PATH##*.}"
VIDEO_FILE="${WORK_DIR}/video_file.${VIDEO_EXT}"
cp "$VIDEO_PATH" "$VIDEO_FILE"
verify_file "$VIDEO_FILE"
print_success "Video copied to workspace"
echo ""

# Step 4: Extract video metadata
print_step "Extracting video metadata..."
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$VIDEO_FILE")
RESOLUTION=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "$VIDEO_FILE")
FORMAT=$(ffprobe -v error -show_entries format=format_name -of default=noprint_wrappers=1:nokey=1 "$VIDEO_FILE")

# Convert duration to mm:ss format
DURATION_FORMATTED=$(printf '%02d:%02d\n' $((${DURATION%.*}/60)) $((${DURATION%.*}%60)))

echo "Duration: $DURATION_FORMATTED"
echo "Resolution: $RESOLUTION"
echo "Format: $FORMAT"

# Save metadata to file (audio status added after audio extraction)
cat > "${WORK_DIR}/metadata.txt" << EOF
Video: $VIDEO_NAME
Duration: $DURATION_FORMATTED
Resolution: $RESOLUTION
Format: $FORMAT
FPS Setting: $FPS
Whisper Model: $WHISPER_MODEL
Analysis Date: $(date)
EOF

verify_file "${WORK_DIR}/metadata.txt"
print_success "Metadata extracted and saved"
echo ""

# Step 5: Extract video frames
print_step "Extracting frames from video (${FPS} fps)..."
ffmpeg -i "$VIDEO_FILE" \
       -vf fps=${FPS} \
       "${WORK_DIR}/frames/frame_%04d.png" \
       -hide_banner -loglevel error

FRAME_COUNT=$(find "${WORK_DIR}/frames" -name "frame_*.png" | wc -l | tr -d ' ')
if [[ "$FRAME_COUNT" -eq 0 ]]; then
    print_error "No frames extracted! Check video file."
    exit 1
fi

print_success "Extracted ${FRAME_COUNT} frames"
echo ""

# Step 6: Extract audio from video (required for whisper - it can't read all video formats directly)
print_step "Extracting audio from video..."

# Check if video has an audio stream
HAS_AUDIO=$(ffprobe -v error -select_streams a -show_entries stream=codec_type -of csv=p=0 "$VIDEO_FILE" 2>/dev/null | head -1)

if [[ -z "$HAS_AUDIO" ]]; then
    print_warning "No audio stream found in video"
    # Create empty audio file placeholder
    touch "${WORK_DIR}/audio.wav"
    AUDIO_PRESENT="false"
else
    ffmpeg -i "$VIDEO_FILE" \
           -ar 16000 -ac 1 -c:a pcm_s16le \
           "${WORK_DIR}/audio.wav" \
           -hide_banner -loglevel error -y

    verify_file "${WORK_DIR}/audio.wav"
    print_success "Audio extracted successfully"
    AUDIO_PRESENT="true"
fi

# Append audio status to metadata
echo "Audio: ${AUDIO_PRESENT}" >> "${WORK_DIR}/metadata.txt"
echo ""

# Step 7: Transcribe audio using whisper
if [[ "$AUDIO_PRESENT" == "false" ]]; then
    print_step "Skipping transcription (no audio stream found)..."
    cat > "${WORK_DIR}/transcription.srt" << 'EOFSILENT'
1
00:00:00,000 --> 00:00:01,000
[No audio stream - video has no audio track]

EOFSILENT
    WORD_COUNT=0
    print_warning "Created placeholder transcription file"
else
    print_step "Transcribing audio (this may take a while)..."
    $WHISPER_CMD \
        -m "$MODEL_FILE" \
        -f "${WORK_DIR}/audio.wav" \
        -osrt \
        -of "${WORK_DIR}/transcription"

    verify_file "${WORK_DIR}/transcription.srt"

    WORD_COUNT=$(wc -w < "${WORK_DIR}/transcription.srt" | tr -d ' ')
    print_success "Transcription complete (~${WORD_COUNT} words)"
fi
echo ""

# Step 7.5: Match frames with transcription
if [[ "$AUDIO_PRESENT" == "false" ]]; then
    print_step "Skipping frame-transcription matching (no audio stream)..."
    MATCHING_TABLE=""
    MATCH_COUNT=0
    print_warning "No matching performed - video has no audio track"
else
    print_step "Matching frames with transcription timestamps..."

    # Parse SRT file
    SRT_DATA=$(parse_srt "${WORK_DIR}/transcription.srt")

    # Create matching table file
    MATCHING_FILE="${WORK_DIR}/frame_transcription_map.txt"
    echo "# Frame-Transcription Matching" > "$MATCHING_FILE"
    echo "# Format: Frame_Number|Timestamp|Transcription" >> "$MATCHING_FILE"
    echo "# Generated at: $(date)" >> "$MATCHING_FILE"
    echo "" >> "$MATCHING_FILE"

    # Generate matching for every 5th frame to keep file manageable
    # (Users can manually check specific frames if needed)
    MATCH_INTERVAL=5
    MATCH_COUNT=0

    for ((i=1; i<=$FRAME_COUNT; i+=$MATCH_INTERVAL)); do
        FRAME_TIME_SEC=$(( (i - 1) / FPS ))
        FRAME_TIME_FORMATTED=$(seconds_to_timestamp "$FRAME_TIME_SEC")
        FRAME_FILE=$(printf "frame_%04d.png" "$i")

        # Find matching transcription
        TRANSCRIPT_TEXT=$(match_frame_to_transcript "$i" "$FPS" "$SRT_DATA")

        # Write to file
        echo "$i|$FRAME_TIME_FORMATTED|$TRANSCRIPT_TEXT" >> "$MATCHING_FILE"
        MATCH_COUNT=$((MATCH_COUNT + 1))
    done

    verify_file "$MATCHING_FILE"
    print_success "Matched ${MATCH_COUNT} frames with transcription segments"

    # Generate markdown table for analysis.md (show first 20 matches)
    MATCHING_TABLE=$(head -n 24 "$MATCHING_FILE" | tail -n 20 | awk -F'|' '
    BEGIN { print "\n| Frame | Time | Transcription |"; print "|-------|------|---------------|" }
    {
        frame_num = $1
        timestamp = $2
        transcript = substr($3, 1, 80)  # Truncate long transcriptions
        if (length($3) > 80) transcript = transcript "..."
        printf "| frame_%04d.png | %s | %s |\n", frame_num, timestamp, transcript
    }')
fi
echo ""

# Step 8: Generate analysis summary
print_step "Generating analysis summary..."

# Determine audio status for report
if [[ "$AUDIO_PRESENT" == "false" ]]; then
    AUDIO_STATUS="None (no audio stream)"
    AUDIO_NOTE="**Note:** This video has no audio stream."
else
    AUDIO_STATUS="Yes"
    AUDIO_NOTE=""
fi

cat > "${WORK_DIR}/analysis.md" << EOF
# Video Analysis: ${VIDEO_NAME%.*}

**Analysis Date**: $(date '+%B %d, %Y at %H:%M:%S')
**Duration**: $DURATION_FORMATTED
**Resolution**: $RESOLUTION
**Format**: $FORMAT
**Audio**: $AUDIO_STATUS

---

## Analysis Summary

This video has been processed and analyzed with the following components:

- **Frames Extracted**: ${FRAME_COUNT} frames at ${FPS} fps
- **Transcription**: ~${WORD_COUNT} words
- **Frame-Transcription Matching**: ${MATCH_COUNT:-0} correlations created
- **Working Directory**: \`${WORK_DIR}\`

## Content Overview

### Visual Content
The video has been extracted into ${FRAME_COUNT} frames, available in the \`frames/\` directory.
Each frame is named sequentially (frame_0001.png, frame_0002.png, etc.).

### Audio Transcription
${AUDIO_NOTE:-The complete transcription is available in \`transcription.srt\` with timestamps.}

### Frame-Transcription Timeline

${MATCHING_TABLE:-**Note:** No frame-transcription matching performed (no audio stream).}

For complete frame-by-frame matching, see \`frame_transcription_map.txt\`.

**How to use the timeline:**
- Each frame number corresponds to a specific timestamp in the video
- Frame timestamp = (frame_number - 1) / FPS
- Example: frame_0045.png at 1 fps = 44 seconds into the video
- The transcription column shows what was being said at that moment

---

## Next Steps

1. Review the \`frame_transcription_map.txt\` for complete frame-by-frame correlation
2. Examine specific frames for visual context
3. Use the integrated timeline above to understand content flow
4. Reference specific frames when discussing transcribed content

## Files Generated

- \`video_file.${VIDEO_EXT}\` - Original video copy
- \`audio.wav\` - Extracted audio (16kHz mono)
- \`transcription.srt\` - Full transcription with timestamps
- \`frame_transcription_map.txt\` - Complete frame-to-transcription correlation
- \`frames/\` - Directory containing ${FRAME_COUNT} extracted frames
- \`metadata.txt\` - Video metadata and processing information
- \`analysis.md\` - This summary file

---

## Transcription Preview

\`\`\`
$(head -n 50 "${WORK_DIR}/transcription.srt")
...
(See full transcription in transcription.srt)
\`\`\`

---

**Analysis completed successfully at**: $(date)
EOF

verify_file "${WORK_DIR}/analysis.md"
print_success "Analysis summary created"
echo ""

# Step 9: Create completion marker
print_step "Creating completion marker..."
echo "COMPLETED" > "${WORK_DIR}/.completed"
echo "$(date)" >> "${WORK_DIR}/.completed"
verify_file "${WORK_DIR}/.completed"
print_success "Analysis marked as complete"
echo ""

# Final summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
print_success "Video analysis completed successfully!"
echo ""
echo "Working Directory: ${WORK_DIR}"
echo ""
echo "Files Created:"
echo "  - video_file.${VIDEO_EXT} (video copy)"
if [[ "$AUDIO_PRESENT" == "true" ]]; then
    echo "  - audio.wav (extracted audio)"
    echo "  - transcription.srt (${WORD_COUNT} words)"
    echo "  - frame_transcription_map.txt (${MATCH_COUNT} frame-transcription matches)"
else
    echo "  - audio.wav (placeholder - no audio stream)"
    echo "  - transcription.srt (placeholder - no audio stream)"
fi
echo "  - frames/ (${FRAME_COUNT} frames)"
echo "  - metadata.txt (video information)"
echo "  - analysis.md (comprehensive summary)"
echo "  - .completed (completion marker)"
echo ""
echo "View analysis: cat ${WORK_DIR}/analysis.md"
echo "View transcription: cat ${WORK_DIR}/transcription.srt"
if [[ "$AUDIO_PRESENT" == "true" ]]; then
    echo "View frame-transcription map: cat ${WORK_DIR}/frame_transcription_map.txt"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

exit 0
