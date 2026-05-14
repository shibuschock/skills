# Tier 2 dependencies

Install hints for the external binaries that tier-2 skills need.

## ffmpeg + ffprobe

### Windows

```powershell
# Easiest (needs winget):
winget install Gyan.FFmpeg

# Portable (no admin, no winget):
# 1. Download "release essentials" zip from https://www.gyan.dev/ffmpeg/builds/
# 2. Unzip to C:\Tools\ffmpeg\
# 3. Add C:\Tools\ffmpeg\bin to PATH (User scope, no admin needed):
#    [System.Environment]::SetEnvironmentVariable('Path', $env:Path + ';C:\Tools\ffmpeg\bin', 'User')
# 4. Restart your shell, verify: ffmpeg -version
```

### macOS

```bash
brew install ffmpeg
```

### Linux

```bash
sudo apt install ffmpeg          # Debian/Ubuntu
sudo dnf install ffmpeg          # Fedora
```

## whisper-cli (whisper.cpp)

There are several whisper implementations. The `video-input` skill expects `whisper-cli` (or `main`) from [whisper.cpp](https://github.com/ggerganov/whisper.cpp).

### Windows

```powershell
# Option 1 — build from source (needs MSVC or MinGW + cmake):
git clone https://github.com/ggerganov/whisper.cpp C:\Tools\whisper.cpp
cd C:\Tools\whisper.cpp
cmake -B build
cmake --build build --config Release
# Resulting binary: C:\Tools\whisper.cpp\build\bin\Release\whisper-cli.exe
# Add to PATH:
[System.Environment]::SetEnvironmentVariable('Path', $env:Path + ';C:\Tools\whisper.cpp\build\bin\Release', 'User')

# Option 2 — pre-built Windows binary from the Releases page:
# https://github.com/ggerganov/whisper.cpp/releases
# Download whisper-bin-x64.zip, unzip, add bin folder to PATH.
```

### macOS / Linux

```bash
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp
make
# Binary at ./main — copy or symlink as 'whisper-cli' onto your PATH
sudo cp main /usr/local/bin/whisper-cli
```

## Whisper model file

After installing whisper.cpp, download a model. `ggml-base.en.bin` (~140 MB, English-only) is a good default.

```powershell
# Windows
$dest = "$env:USERPROFILE\.whisper-models"
New-Item -ItemType Directory -Force $dest | Out-Null
Invoke-WebRequest `
  -Uri 'https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin' `
  -OutFile "$dest\ggml-base.en.bin"
```

```bash
# POSIX
mkdir -p ~/.whisper-models
curl -L -o ~/.whisper-models/ggml-base.en.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin
```

Then point the `video-input` script at it: `--model ~/.whisper-models/ggml-base.en.bin` (PowerShell variant uses `-Model`).

## Verification

```powershell
ffmpeg -version
ffprobe -version
whisper-cli --help
```

If all three respond, tier-2 skills are good to go.
