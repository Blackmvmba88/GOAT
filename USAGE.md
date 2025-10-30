# GOAT - Intelligent Multimedia Player

## Usage Guide

GOAT (Generative Organic Audio-visual Technology) is an intelligent multimedia player that combines AI analysis, reactive visuals, and cross-platform support to create a living, breathing media experience.

## Features

### Core Capabilities
- **Multi-format Support**: Play audio (MP3, WAV, OGG, FLAC, M4A) and video (MP4, AVI, MOV, MKV, WEBM)
- **Reactive Visuals**: Real-time audio analysis drives dynamic visualizations
- **AI Integration**: Intelligent mood detection, genre analysis, and adaptive color palettes
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Modular Architecture**: Easy to extend with new visualization modes and AI features

### Visualization Modes
1. **Spectrum Analyzer**: Frequency-based visualization with colored bars
2. **Waveform**: Classic waveform display showing audio amplitude
3. **Particles**: Generative particle system responding to audio energy

### AI Features
- **Mood Detection**: Analyzes tempo and audio features to detect mood (energetic, calm, upbeat, etc.)
- **Adaptive Color Palettes**: Colors change based on detected mood
- **Key Moment Detection**: Identifies drops, crescendos, and other significant moments
- **Genre Classification**: Estimates musical genre from audio features

## Installation

### Requirements
- Python 3.8 or higher
- System audio libraries (varies by platform)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Platform-Specific Notes

#### Linux
```bash
# Ubuntu/Debian
sudo apt-get install python3-pygame python3-opencv libportaudio2

# Fedora
sudo dnf install python3-pygame python3-opencv portaudio
```

#### macOS
```bash
brew install portaudio
```

#### Windows
No additional system packages required. All dependencies install via pip.

## Quick Start

### Basic Usage

```bash
# Start the player
python main.py

# Play a specific media file
python main.py /path/to/your/music.mp3

# Custom window size
python main.py --width 1920 --height 1080 /path/to/video.mp4

# Fullscreen mode
python main.py --fullscreen /path/to/music.mp3
```

## Controls

### Keyboard Shortcuts
- **SPACE**: Play/Pause
- **S**: Stop playback
- **V**: Cycle through visualization modes (audio only)
- **Q**: Quit application

### Mouse
- Resize window by dragging edges (window automatically adjusts content)

## Architecture

### Core Modules

#### `goat_player.py`
Main player class handling:
- Media loading (audio/video)
- Playback control
- Audio analysis with librosa
- Visualization rendering
- UI overlay

#### `ai_module.py`
AI integration providing:
- Mood analysis based on tempo and audio features
- Genre detection
- Key moment identification
- Adaptive color palette generation
- Visual enhancement suggestions

#### `config.py`
Configuration management:
- User preferences
- Display settings
- AI feature toggles
- Color themes

#### `main.py`
Entry point:
- Command-line argument parsing
- Application initialization
- Main event loop

## Advanced Features

### Configuration

Configuration is stored in `~/.goat/config.json`. Default settings:

```json
{
  "display": {
    "width": 1280,
    "height": 720,
    "fullscreen": false,
    "fps": 60
  },
  "audio": {
    "frequency": 44100,
    "channels": 2,
    "buffer_size": 512
  },
  "visualization": {
    "mode": "spectrum",
    "enable_ai": true,
    "particle_count": 100,
    "default_theme": "vibrant"
  },
  "ai": {
    "enable_mood_detection": true,
    "enable_genre_detection": true,
    "enable_adaptive_visuals": true
  }
}
```

### Color Themes

Available themes:
- **vibrant**: Bold, saturated colors (default)
- **pastel**: Soft, muted tones
- **dark**: Deep, rich colors
- **neon**: Ultra-bright, electric colors

## Extending GOAT

### Adding New Visualization Modes

1. Add new method to `GOATPlayer` class:
```python
def _render_custom_visualization(self):
    # Your visualization code here
    pass
```

2. Register in `cycle_visualization()` method
3. Add to render() switch statement

### Adding AI Features

1. Extend `AIModule` class in `ai_module.py`
2. Add analysis methods following existing patterns
3. Integrate with visualization engine

### Custom Color Palettes

Edit `COLOR_THEMES` dictionary in `config.py`:
```python
COLOR_THEMES['custom'] = [
    (r1, g1, b1),
    (r2, g2, b2),
    # ... more colors
]
```

## Performance Tips

1. **High Resolution**: Use `--width` and `--height` matching your display
2. **FPS**: Default 60fps provides smooth visuals; adjust in config if needed
3. **Audio Buffer**: Smaller buffers (512) = lower latency, more CPU
4. **Particle Count**: Reduce for better performance on slower systems

## Troubleshooting

### Audio Not Playing
- Check file format is supported
- Verify system audio is working
- Try different audio file

### Visualization Not Showing
- Ensure file is audio format (not video)
- Check that librosa analyzed audio successfully
- Look for errors in console output

### Performance Issues
- Reduce window size
- Lower target FPS in config
- Disable AI features if not needed
- Use simpler visualization mode (waveform)

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

## Examples

### Playing Audio with Visualizations
```bash
python main.py my_song.mp3
# Press V to cycle through visualizations
# Press SPACE to pause/play
```

### Playing Video
```bash
python main.py my_video.mp4
# Video plays with optional audio-reactive overlay
```

### Custom Window Size
```bash
python main.py --width 1920 --height 1080 music.wav
```

## Future Enhancements

Planned features:
- Playlist management
- Real-time audio effects
- VR/AR support
- Streaming integration
- Machine learning-based visualization generation
- MIDI controller support
- Plugin system for custom visualizers

## Contributing

GOAT is designed to be extensible. Key areas for contribution:
- New visualization algorithms
- Enhanced AI models for mood/genre detection
- Platform-specific optimizations
- Additional audio effects
- UI improvements

## License

See LICENSE file for details.

## Credits

Built with:
- pygame: Core graphics and audio
- librosa: Audio analysis
- opencv-python: Video processing
- numpy: Numerical operations
