# Video Analysis Script (PowerShell port)
# Usage: pwsh ./analyze-video.ps1 <path-to-video-file> [fps] [whisper-model]
# Mirrors the behavior of analyze-video.sh for Windows / cross-platform PowerShell 7+.

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$VideoPath,

    [Parameter(Position = 1)]
    [int]$Fps = 1,

    [Parameter(Position = 2)]
    [string]$WhisperModel = 'base'
)

$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

# ---- Model dir resolution ----
$WhisperModelDir =
    if ($env:WHISPER_MODEL_DIR) { $env:WHISPER_MODEL_DIR }
    elseif (Test-Path -LiteralPath (Join-Path $HOME '.cache/whisper')) { Join-Path $HOME '.cache/whisper' }
    elseif (Test-Path -LiteralPath (Join-Path $HOME '.local/share/whisper-cpp')) { Join-Path $HOME '.local/share/whisper-cpp' }
    else { Join-Path $HOME '.cache/whisper' }

# ---- Output helpers ----
function Write-Step     { param([string]$Msg) Write-Host "[STEP] $Msg" -ForegroundColor Blue }
function Write-Ok       { param([string]$Msg) Write-Host "OK  $Msg"    -ForegroundColor Green }
function Write-Fail     { param([string]$Msg) Write-Host "ERR $Msg"    -ForegroundColor Red }
function Write-Warn     { param([string]$Msg) Write-Host "WARN $Msg"   -ForegroundColor Yellow }

function Test-CommandExists {
    param([string]$Name)
    $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Assert-CommandExists {
    param([string]$Name)
    if (-not (Test-CommandExists $Name)) {
        Write-Fail "Required command '$Name' not found. Please install it first."
        exit 1
    }
}

function Assert-FileExists {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        Write-Fail "File not found: $Path"
        exit 1
    }
    Write-Ok "File verified: $Path"
}

function Assert-DirExists {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
        Write-Fail "Directory not found: $Path"
        exit 1
    }
    Write-Ok "Directory verified: $Path"
}

# ---- SRT helpers ----
function Get-SrtSegments {
    param([string]$SrtFile)
    $text = Get-Content -LiteralPath $SrtFile -Raw
    if (-not $text) { return @() }

    $blocks = $text -split "(\r?\n){2,}"
    $segments = foreach ($block in $blocks) {
        $lines = $block -split "\r?\n" | Where-Object { $_ -ne '' }
        if ($lines.Count -lt 3) { continue }
        if ($lines[1] -notmatch '-->') { continue }

        $times = $lines[1] -split '\s*-->\s*'
        [pscustomobject]@{
            Start = ConvertFrom-SrtTimestamp $times[0]
            End   = ConvertFrom-SrtTimestamp $times[1]
            Text  = ($lines[2..($lines.Count - 1)] -join ' ').Trim()
        }
    }
    return @($segments)
}

function ConvertFrom-SrtTimestamp {
    param([string]$Timestamp)
    # Format: HH:MM:SS,mmm -> total seconds (int)
    $timePart = ($Timestamp -split ',')[0]
    $parts = $timePart -split ':'
    return [int]$parts[0] * 3600 + [int]$parts[1] * 60 + [int]$parts[2]
}

function Format-Seconds {
    param([int]$TotalSeconds)
    $h = [int]($TotalSeconds / 3600)
    $m = [int](($TotalSeconds % 3600) / 60)
    $s = $TotalSeconds % 60
    return ('{0:D2}:{1:D2}:{2:D2}' -f $h, $m, $s)
}

function Get-TranscriptForFrame {
    param(
        [int]$FrameNum,
        [int]$FpsLocal,
        [object[]]$Segments
    )
    $frameSeconds = [int](($FrameNum - 1) / $FpsLocal)
    foreach ($seg in $Segments) {
        if ($frameSeconds -ge $seg.Start -and $frameSeconds -lt $seg.End) {
            return $seg.Text
        }
    }
    return '[No transcription at this timestamp]'
}

# ---- CLAUDE_PROJECT_DIR fallback ----
$ClaudeProjectDir = $env:CLAUDE_PROJECT_DIR
if (-not $ClaudeProjectDir) {
    Write-Warn 'CLAUDE_PROJECT_DIR not set, using current directory'
    $ClaudeProjectDir = (Get-Location).Path
}

Write-Step 'Starting video analysis...'
Write-Host "Video: $VideoPath"
Write-Host "FPS: $Fps"
Write-Host "Whisper Model: $WhisperModel"
Write-Host "Project Dir: $ClaudeProjectDir"
Write-Host ''

# ---- Dependency checks ----
Write-Step 'Checking dependencies...'
Assert-CommandExists 'ffmpeg'
Assert-CommandExists 'ffprobe'

$WhisperCmd = $null
foreach ($candidate in @('whisper', 'whisper-cli', 'whisper.cpp', 'main')) {
    if (Test-CommandExists $candidate) { $WhisperCmd = $candidate; break }
}
if (-not $WhisperCmd) {
    Write-Fail "Whisper not found. Install whisper.cpp (e.g. 'winget install whispercpp' or build from https://github.com/ggerganov/whisper.cpp) and ensure 'whisper' or 'whisper-cli' is on PATH."
    exit 1
}
Write-Ok "Found whisper command: $WhisperCmd"
Write-Ok 'All dependencies available'

# ---- Model file: auto-download if missing ----
$ModelFile = Join-Path $WhisperModelDir "ggml-$WhisperModel.bin"
if (-not (Test-Path -LiteralPath $ModelFile -PathType Leaf)) {
    Write-Warn "Whisper model not found locally: $ModelFile"
    New-Item -ItemType Directory -Path $WhisperModelDir -Force | Out-Null
    $ModelUrl = "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-$WhisperModel.bin"
    Write-Step "Downloading model from $ModelUrl ..."
    try {
        $ProgressPreference = 'Continue'
        Invoke-WebRequest -Uri $ModelUrl -OutFile $ModelFile -UseBasicParsing
    } catch {
        Write-Fail "Failed to download model: $($_.Exception.Message)"
        if (Test-Path -LiteralPath $ModelFile) { Remove-Item -LiteralPath $ModelFile -Force }
        Write-Host "Try a different model name (tiny, base, small, medium, large) or download manually from https://huggingface.co/ggerganov/whisper.cpp/tree/main"
        exit 1
    }
    Write-Ok "Model downloaded: $ModelFile"
} else {
    Write-Ok "Model file found: $ModelFile"
}
Write-Host ''

# ---- Step 1: verify input video ----
Write-Step 'Verifying input video...'
Assert-FileExists $VideoPath
$VideoName = Split-Path -Leaf $VideoPath
Write-Host ''

# ---- Step 2: isolated workspace ----
Write-Step 'Creating isolated workspace...'
$Timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$WorkDir = Join-Path $ClaudeProjectDir ".video-input/analysis_$Timestamp"
$FramesDir = Join-Path $WorkDir 'frames'
New-Item -ItemType Directory -Path $FramesDir -Force | Out-Null
Assert-DirExists $WorkDir
Assert-DirExists $FramesDir
Write-Ok "Created: $WorkDir"
Write-Host ''

# ---- Step 3: copy video ----
Write-Step 'Copying video to workspace...'
$VideoExt = [System.IO.Path]::GetExtension($VideoPath).TrimStart('.')
$VideoFile = Join-Path $WorkDir "video_file.$VideoExt"
Copy-Item -LiteralPath $VideoPath -Destination $VideoFile
Assert-FileExists $VideoFile
Write-Ok 'Video copied to workspace'
Write-Host ''

# ---- Step 4: metadata ----
Write-Step 'Extracting video metadata...'
$Duration   = (& ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $VideoFile).Trim()
$Resolution = (& ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 $VideoFile).Trim()
$Format     = (& ffprobe -v error -show_entries format=format_name -of default=noprint_wrappers=1:nokey=1 $VideoFile).Trim()

$DurationInt = [int]([double]$Duration)
$DurationFormatted = ('{0:D2}:{1:D2}' -f [int]($DurationInt / 60), ($DurationInt % 60))

Write-Host "Duration: $DurationFormatted"
Write-Host "Resolution: $Resolution"
Write-Host "Format: $Format"

$MetadataContent = @"
Video: $VideoName
Duration: $DurationFormatted
Resolution: $Resolution
Format: $Format
FPS Setting: $Fps
Whisper Model: $WhisperModel
Analysis Date: $(Get-Date)
"@
$MetadataFile = Join-Path $WorkDir 'metadata.txt'
Set-Content -LiteralPath $MetadataFile -Value $MetadataContent -Encoding UTF8
Assert-FileExists $MetadataFile
Write-Ok 'Metadata extracted and saved'
Write-Host ''

# ---- Step 5: extract frames ----
Write-Step "Extracting frames from video ($Fps fps)..."
$FramePattern = Join-Path $FramesDir 'frame_%04d.png'
& ffmpeg -i $VideoFile -vf "fps=$Fps" $FramePattern -hide_banner -loglevel error
if ($LASTEXITCODE -ne 0) {
    Write-Fail 'ffmpeg frame extraction failed'
    exit 1
}

$FrameCount = (Get-ChildItem -LiteralPath $FramesDir -Filter 'frame_*.png').Count
if ($FrameCount -eq 0) {
    Write-Fail 'No frames extracted! Check video file.'
    exit 1
}
Write-Ok "Extracted $FrameCount frames"
Write-Host ''

# ---- Step 6: extract audio ----
Write-Step 'Extracting audio from video...'
$HasAudio = (& ffprobe -v error -select_streams a -show_entries stream=codec_type -of csv=p=0 $VideoFile 2>$null | Select-Object -First 1)
$AudioFile = Join-Path $WorkDir 'audio.wav'

if (-not $HasAudio) {
    Write-Warn 'No audio stream found in video'
    New-Item -ItemType File -Path $AudioFile -Force | Out-Null
    $AudioPresent = $false
} else {
    & ffmpeg -i $VideoFile -ar 16000 -ac 1 -c:a pcm_s16le $AudioFile -hide_banner -loglevel error -y
    if ($LASTEXITCODE -ne 0) {
        Write-Fail 'ffmpeg audio extraction failed'
        exit 1
    }
    Assert-FileExists $AudioFile
    Write-Ok 'Audio extracted successfully'
    $AudioPresent = $true
}

Add-Content -LiteralPath $MetadataFile -Value "Audio: $($AudioPresent.ToString().ToLower())"
Write-Host ''

# ---- Step 7: transcribe ----
$TranscriptionSrt = Join-Path $WorkDir 'transcription.srt'
$WordCount = 0

if (-not $AudioPresent) {
    Write-Step 'Skipping transcription (no audio stream found)...'
    $placeholder = @'
1
00:00:00,000 --> 00:00:01,000
[No audio stream - video has no audio track]
'@
    Set-Content -LiteralPath $TranscriptionSrt -Value $placeholder -Encoding UTF8
    Write-Warn 'Created placeholder transcription file'
} else {
    Write-Step 'Transcribing audio (this may take a while)...'
    $TranscriptionBase = Join-Path $WorkDir 'transcription'
    & $WhisperCmd -m $ModelFile -f $AudioFile -osrt -of $TranscriptionBase
    if ($LASTEXITCODE -ne 0) {
        Write-Fail 'Whisper transcription failed'
        exit 1
    }
    Assert-FileExists $TranscriptionSrt
    $WordCount = (Get-Content -LiteralPath $TranscriptionSrt | Measure-Object -Word).Words
    Write-Ok "Transcription complete (~$WordCount words)"
}
Write-Host ''

# ---- Step 7.5: match frames to transcript ----
$MatchCount = 0
$MatchingTable = ''
$MatchingFile = Join-Path $WorkDir 'frame_transcription_map.txt'

if (-not $AudioPresent) {
    Write-Step 'Skipping frame-transcription matching (no audio stream)...'
    Write-Warn 'No matching performed - video has no audio track'
} else {
    Write-Step 'Matching frames with transcription timestamps...'

    $Segments = Get-SrtSegments -SrtFile $TranscriptionSrt

    $header = @"
# Frame-Transcription Matching
# Format: Frame_Number|Timestamp|Transcription
# Generated at: $(Get-Date)

"@
    Set-Content -LiteralPath $MatchingFile -Value $header -Encoding UTF8

    $MatchInterval = 5
    $sb = [System.Text.StringBuilder]::new()

    for ($i = 1; $i -le $FrameCount; $i += $MatchInterval) {
        $frameTimeSec = [int](($i - 1) / $Fps)
        $frameTimeFormatted = Format-Seconds $frameTimeSec
        $transcriptText = Get-TranscriptForFrame -FrameNum $i -FpsLocal $Fps -Segments $Segments
        [void]$sb.AppendLine("$i|$frameTimeFormatted|$transcriptText")
        $MatchCount++
    }
    Add-Content -LiteralPath $MatchingFile -Value $sb.ToString()

    Assert-FileExists $MatchingFile
    Write-Ok "Matched $MatchCount frames with transcription segments"

    # Build markdown preview table (first 20 matches)
    $preview = Get-Content -LiteralPath $MatchingFile | Select-Object -Skip 4 -First 20
    $tableLines = @('', '| Frame | Time | Transcription |', '|-------|------|---------------|')
    foreach ($line in $preview) {
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        $parts = $line -split '\|', 3
        if ($parts.Count -lt 3) { continue }
        $frameNum = [int]$parts[0]
        $timestamp = $parts[1]
        $transcript = $parts[2]
        if ($transcript.Length -gt 80) { $transcript = $transcript.Substring(0, 80) + '...' }
        $tableLines += ('| frame_{0:D4}.png | {1} | {2} |' -f $frameNum, $timestamp, $transcript)
    }
    $MatchingTable = $tableLines -join "`n"
}
Write-Host ''

# ---- Step 8: analysis.md ----
Write-Step 'Generating analysis summary...'

if (-not $AudioPresent) {
    $AudioStatus = 'None (no audio stream)'
    $AudioNote = '**Note:** This video has no audio stream.'
} else {
    $AudioStatus = 'Yes'
    $AudioNote = 'The complete transcription is available in `transcription.srt` with timestamps.'
}

$VideoBaseName = [System.IO.Path]::GetFileNameWithoutExtension($VideoName)
$AnalysisDate = Get-Date -Format 'MMMM dd, yyyy \a\t HH:mm:ss'
$NowStr = Get-Date

$matchingSection = if ($MatchingTable) { $MatchingTable } else { '**Note:** No frame-transcription matching performed (no audio stream).' }
$transcriptionPreview = (Get-Content -LiteralPath $TranscriptionSrt | Select-Object -First 50) -join "`n"

$analysisContent = @"
# Video Analysis: $VideoBaseName

**Analysis Date**: $AnalysisDate
**Duration**: $DurationFormatted
**Resolution**: $Resolution
**Format**: $Format
**Audio**: $AudioStatus

---

## Analysis Summary

This video has been processed and analyzed with the following components:

- **Frames Extracted**: $FrameCount frames at $Fps fps
- **Transcription**: ~$WordCount words
- **Frame-Transcription Matching**: $MatchCount correlations created
- **Working Directory**: ``$WorkDir``

## Content Overview

### Visual Content
The video has been extracted into $FrameCount frames, available in the ``frames/`` directory.
Each frame is named sequentially (frame_0001.png, frame_0002.png, etc.).

### Audio Transcription
$AudioNote

### Frame-Transcription Timeline

$matchingSection

For complete frame-by-frame matching, see ``frame_transcription_map.txt``.

**How to use the timeline:**
- Each frame number corresponds to a specific timestamp in the video
- Frame timestamp = (frame_number - 1) / FPS
- Example: frame_0045.png at 1 fps = 44 seconds into the video
- The transcription column shows what was being said at that moment

---

## Next Steps

1. Review ``frame_transcription_map.txt`` for complete frame-by-frame correlation
2. Examine specific frames for visual context
3. Use the integrated timeline above to understand content flow
4. Reference specific frames when discussing transcribed content

## Files Generated

- ``video_file.$VideoExt`` - Original video copy
- ``audio.wav`` - Extracted audio (16kHz mono)
- ``transcription.srt`` - Full transcription with timestamps
- ``frame_transcription_map.txt`` - Complete frame-to-transcription correlation
- ``frames/`` - Directory containing $FrameCount extracted frames
- ``metadata.txt`` - Video metadata and processing information
- ``analysis.md`` - This summary file

---

## Transcription Preview

``````
$transcriptionPreview
...
(See full transcription in transcription.srt)
``````

---

**Analysis completed successfully at**: $NowStr
"@

$AnalysisFile = Join-Path $WorkDir 'analysis.md'
Set-Content -LiteralPath $AnalysisFile -Value $analysisContent -Encoding UTF8
Assert-FileExists $AnalysisFile
Write-Ok 'Analysis summary created'
Write-Host ''

# ---- Step 9: completion marker ----
Write-Step 'Creating completion marker...'
$CompletedFile = Join-Path $WorkDir '.completed'
Set-Content -LiteralPath $CompletedFile -Value "COMPLETED`n$(Get-Date)" -Encoding UTF8
Assert-FileExists $CompletedFile
Write-Ok 'Analysis marked as complete'
Write-Host ''

# ---- Final summary ----
Write-Host ('-' * 60)
Write-Ok 'Video analysis completed successfully!'
Write-Host ''
Write-Host "Working Directory: $WorkDir"
Write-Host ''
Write-Host 'Files Created:'
Write-Host "  - video_file.$VideoExt (video copy)"
if ($AudioPresent) {
    Write-Host '  - audio.wav (extracted audio)'
    Write-Host "  - transcription.srt ($WordCount words)"
    Write-Host "  - frame_transcription_map.txt ($MatchCount frame-transcription matches)"
} else {
    Write-Host '  - audio.wav (placeholder - no audio stream)'
    Write-Host '  - transcription.srt (placeholder - no audio stream)'
}
Write-Host "  - frames/ ($FrameCount frames)"
Write-Host '  - metadata.txt (video information)'
Write-Host '  - analysis.md (comprehensive summary)'
Write-Host '  - .completed (completion marker)'
Write-Host ''
Write-Host "View analysis:      Get-Content '$AnalysisFile'"
Write-Host "View transcription: Get-Content '$TranscriptionSrt'"
if ($AudioPresent) {
    Write-Host "View frame-transcription map: Get-Content '$MatchingFile'"
}
Write-Host ('-' * 60)

exit 0
