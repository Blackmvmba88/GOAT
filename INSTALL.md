# GOAT Installation Guide

## System Requirements

- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- Audio output device
- Graphics card with OpenGL support (for optimal performance)

## Installation

### Method 1: Using pip (Recommended)

```bash
# Clone the repository
git clone https://github.com/Blackmvmba88/GOAT.git
cd GOAT

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Method 2: Using setup.py

```bash
# After cloning the repository
cd GOAT
python setup.py install
```

## Platform-Specific Instructions

### Linux (Ubuntu/Debian)

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y \
    python3-dev \
    python3-pip \
    portaudio19-dev \
    python3-pygame \
    libopencv-dev \
    ffmpeg

# Install Python dependencies
pip install -r requirements.txt
```

### Linux (Fedora)

```bash
# Install system dependencies
sudo dnf install -y \
    python3-devel \
    portaudio-devel \
    pygame \
    opencv-python \
    ffmpeg

# Install Python dependencies
pip install -r requirements.txt
```

### macOS

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install system dependencies
brew install portaudio ffmpeg

# Install Python dependencies
pip install -r requirements.txt
```

### Windows

```bash
# No additional system packages required
# Just install Python dependencies
pip install -r requirements.txt
```

**Note**: On Windows, you may need to install Visual C++ Build Tools if you encounter compilation errors.

## Verifying Installation

```bash
# Test the installation
python main.py --help

# Should display:
# usage: main.py [-h] [--width WIDTH] [--height HEIGHT] [--fullscreen] [media]
# GOAT - Intelligent Multimedia Player with AI and Reactive Visuals
```

## Troubleshooting

### PyAudio Installation Issues

**Linux**:
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

**macOS**:
```bash
brew install portaudio
pip install pyaudio
```

**Windows**:
Download pre-built wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

### Pygame Installation Issues

```bash
# Try installing SDL2 dependencies first
# Ubuntu/Debian:
sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev

# Then reinstall pygame
pip install --upgrade pygame
```

### OpenCV Issues

```bash
# If opencv-python fails, try headless version
pip uninstall opencv-python
pip install opencv-python-headless
```

### librosa Installation Issues

```bash
# Install numba and llvmlite first
pip install numba llvmlite
pip install librosa
```

## Optional Dependencies

### For Development

```bash
pip install pytest pytest-cov black flake8 mypy
```

### For Advanced AI Features

```bash
pip install torch torchvision torchaudio
pip install openai transformers
```

## Post-Installation

### First Run

```bash
# Run GOAT without media file to see the interface
python main.py

# Try with a media file
python main.py /path/to/your/music.mp3
```

### Configuration

On first run, GOAT creates a configuration file at:
- **Linux/macOS**: `~/.goat/config.json`
- **Windows**: `%USERPROFILE%\.goat\config.json`

You can edit this file to customize settings.

## Uninstallation

```bash
# If installed via pip
pip uninstall goat-player

# Remove configuration (optional)
# Linux/macOS:
rm -rf ~/.goat
# Windows:
rmdir /s %USERPROFILE%\.goat
```

## Getting Help

If you encounter issues:
1. Check the [USAGE.md](USAGE.md) documentation
2. Review the troubleshooting section above
3. Check existing issues on GitHub
4. Open a new issue with:
   - Your OS and Python version
   - Full error message
   - Steps to reproduce

## Next Steps

After installation, see [USAGE.md](USAGE.md) for:
- Basic usage
- Keyboard controls
- Configuration options
- Advanced features
