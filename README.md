# GOAT - Intelligent Multimedia Player

**Generative Organic Audio-visual Technology**

Reproductor multimedia inteligente desarrollado bajo el proyecto GOAT. Diseñado para ofrecer una experiencia fluida, visual y sonora de alto rendimiento. Integración modular con IA, audio reactivo y soporte multiplataforma.

## ✨ Features

- 🎵 **Multi-format Support**: Audio (MP3, WAV, OGG, FLAC, M4A) and Video (MP4, AVI, MOV, MKV)
- 🎨 **Reactive Visuals**: Real-time audio analysis drives dynamic visualizations
- 🤖 **AI Integration**: Mood detection, genre analysis, and adaptive color palettes
- 🌈 **Multiple Visualization Modes**: Spectrum analyzer, waveform, particle systems
- 💻 **Cross-platform**: Windows, macOS, Linux support
- ⚡ **High Performance**: 60 FPS rendering with optimized audio analysis
- 🎯 **Modular Architecture**: Easily extensible for custom features

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Blackmvmba88/GOAT.git
cd GOAT

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Start the player
python main.py

# Play a specific file
python main.py /path/to/music.mp3

# Custom window size
python main.py --width 1920 --height 1080 video.mp4

# Fullscreen mode
python main.py --fullscreen music.mp3
```

## 🎮 Controls

- **SPACE**: Play/Pause
- **S**: Stop
- **V**: Cycle visualization modes
- **Q**: Quit

## 📖 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[USAGE.md](USAGE.md)** - Detailed usage guide and features
- **[INSTALL.md](INSTALL.md)** - Platform-specific installation instructions
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and architecture

## 🏗️ Architecture

```
GOAT/
├── main.py              # Entry point
├── goat_player.py       # Core player with visualization
├── ai_module.py         # AI integration and analysis
├── config.py            # Configuration management
├── requirements.txt     # Python dependencies
└── USAGE.md            # Detailed documentation
```

## 🎨 Visualization Modes

1. **Spectrum Analyzer**: Frequency-based bars responding to audio
2. **Waveform**: Classic amplitude visualization
3. **Particles**: Generative particle system driven by audio energy

## 🤖 AI Features

- **Mood Detection**: Analyzes tempo and features (energetic, calm, upbeat, ambient)
- **Adaptive Palettes**: Colors change based on detected mood
- **Key Moments**: Identifies drops, crescendos, and transitions
- **Genre Classification**: Estimates musical genre from audio analysis

## 🛠️ Technology Stack

- **pygame**: Graphics and audio playback
- **librosa**: Audio analysis and feature extraction
- **opencv-python**: Video processing
- **numpy**: Numerical computations
- **PyQt6**: Cross-platform UI support

## 💡 Examples

### Audio with Visualizations
```bash
python main.py your_song.mp3
# Press V to cycle through spectrum, waveform, and particles
```

### Video Playback
```bash
python main.py your_video.mp4
# Enjoy fluid video playback with optional audio-reactive overlays
```

## 🌟 Future Enhancements

- Real-time audio effects and filters
- Playlist management and smart recommendations
- Streaming service integration
- VR/AR visualization support
- Machine learning-generated visuals
- MIDI controller support
- Plugin system for custom visualizers

## 🤝 Contributing

Contributions are welcome! Areas of interest:
- New visualization algorithms
- Enhanced AI models
- Performance optimizations
- UI/UX improvements
- Documentation

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

GOAT fuses technology, art, and sound to create a living interface that responds to your media. Experience multimedia the way it was meant to be - intelligent, adaptive, and beautiful.

---

**Made with ❤️ for the GOAT project**
