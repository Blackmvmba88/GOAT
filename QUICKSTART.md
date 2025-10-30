# GOAT Quick Start Guide

Get up and running with GOAT in under 5 minutes!

## Prerequisites

- Python 3.8+ installed
- Audio output device
- (Optional) Media files to play

## Installation (One Command)

```bash
git clone https://github.com/Blackmvmba88/GOAT.git && cd GOAT && pip install -r requirements.txt
```

## Your First Run

### Option 1: Demo Mode (No Media Required)

```bash
python demo.py
```

Press **SPACE** to start the demo, **V** to change visualizations, **Q** to quit.

### Option 2: Play Your Music

```bash
python main.py /path/to/your/song.mp3
```

### Option 3: Play Video

```bash
python main.py /path/to/your/video.mp4
```

## Essential Controls

| Key | Action |
|-----|--------|
| SPACE | Play/Pause |
| S | Stop |
| V | Change Visualization |
| Q | Quit |

## Common Use Cases

### Full-Screen Music Visualization

```bash
python main.py --fullscreen --width 1920 --height 1080 music.mp3
```

### Try Different Media Formats

```bash
# Audio
python main.py song.mp3    # MP3
python main.py track.wav   # WAV
python main.py audio.flac  # FLAC

# Video
python main.py video.mp4   # MP4
python main.py clip.mov    # MOV
python main.py movie.mkv   # MKV
```

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### PyAudio installation fails
**Linux:**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

### No audio plays
- Check system volume
- Verify file format is supported
- Try a different audio file

## What's Next?

- Read [USAGE.md](USAGE.md) for detailed features
- Check [ARCHITECTURE.md](ARCHITECTURE.md) to understand the design
- See [INSTALL.md](INSTALL.md) for platform-specific setup

## Tips & Tricks

1. **Best Visualization**: Try spectrum mode with electronic music
2. **Performance**: Start with 1280x720, scale up if smooth
3. **Exploration**: Press V multiple times to see all modes
4. **Custom Config**: Edit `~/.goat/config.json` after first run

## Need Help?

- Check existing issues on GitHub
- Review [USAGE.md](USAGE.md) documentation
- Open a new issue with:
  - Your OS and Python version
  - Full error message
  - Steps to reproduce

---

**Enjoy your intelligent multimedia experience!** 🎵🎨🤖
