# GOAT Architecture Documentation

## Overview

GOAT (Generative Organic Audio-visual Technology) is designed with a modular architecture that separates concerns and allows for easy extension and customization.

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     User Interface                       │
│              (Pygame Display & Controls)                 │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────┐
│                   GOAT Player Core                       │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────┐ │
│  │Media Loader  │  │Playback Engine│  │Visualization │ │
│  │  & Decoder   │→ │   & Control   │→ │   Renderer   │ │
│  └──────────────┘  └───────────────┘  └──────────────┘ │
└──────────┬──────────────────┬──────────────┬───────────┘
           │                  │              │
    ┌──────┴─────┐    ┌──────┴──────┐   ┌──┴──────────┐
    │Audio       │    │AI Analysis  │   │Configuration│
    │Processing  │    │Module       │   │Manager      │
    │(librosa)   │    │             │   │             │
    └────────────┘    └─────────────┘   └─────────────┘
```

## Core Components

### 1. Main Entry Point (`main.py`)

**Responsibility**: Application bootstrap and main event loop

**Key Functions**:
- Parse command-line arguments
- Initialize GOATPlayer
- Run main event loop
- Handle graceful shutdown

**Flow**:
```python
main() → Initialize Player → Load Media (optional) → Event Loop → Cleanup
```

### 2. GOAT Player (`goat_player.py`)

**Responsibility**: Core player functionality and visualization

**Key Components**:

#### Media Loading
```python
load_media(filepath) → Detect format → Route to specific loader
    ├─ _load_audio() → pygame.mixer + librosa analysis
    └─ _load_video() → OpenCV capture
```

#### Audio Analysis Pipeline
```python
_analyze_audio() → Extract features:
    ├─ Tempo & Beat tracking
    ├─ Spectral centroid (brightness)
    ├─ Chroma features (harmony)
    └─ MFCC (timbre)
```

#### Visualization Rendering
```python
render() → Clear screen → Route by media type:
    ├─ Video: _render_video_frame()
    └─ Audio: Route by mode:
        ├─ 'spectrum': _render_spectrum_visualization()
        ├─ 'waveform': _render_waveform_visualization()
        └─ 'particles': _render_particles_visualization()
```

**State Management**:
- `playing`: Boolean indicating playback state
- `paused`: Boolean indicating pause state
- `current_media`: Path to loaded media
- `media_type`: 'audio' or 'video'
- `audio_features`: Dict of extracted audio features

### 3. AI Module (`ai_module.py`)

**Responsibility**: Intelligent analysis and adaptive features

**Components**:

#### AIModule Class
- `analyze_mood()`: Tempo-based mood detection
- `detect_key_moments()`: Onset detection for significant audio events
- `generate_adaptive_palette()`: Mood-aware color selection
- `analyze_genre()`: Simple genre classification
- `suggest_visualization()`: Recommend optimal viz mode
- `enhance_visuals_with_ai()`: Real-time visual parameter adjustment

#### AdaptiveVisualEngine Class
- Coordinates AI module with visualization
- Updates color palettes dynamically
- Adjusts visual parameters in real-time

**AI Pipeline**:
```
Audio Features → Mood Detection → Palette Generation → Visual Enhancement
                      ↓
                Genre Detection → Visualization Suggestion
                      ↓
                Key Moments → Trigger Effects
```

### 4. Configuration (`config.py`)

**Responsibility**: Settings management and persistence

**Structure**:
```json
{
  "display": { ... },
  "audio": { ... },
  "visualization": { ... },
  "ai": { ... },
  "playback": { ... }
}
```

**Features**:
- Dot-notation access: `config.get('display.width')`
- Persistent storage in `~/.goat/config.json`
- Default fallback values
- Color theme management

### 5. Demo Mode (`demo.py`)

**Responsibility**: Showcase capabilities without media files

**Features**:
- Synthesized audio generation
- Auto-cycling visualizations
- Interactive controls
- Educational overlay

## Data Flow

### Audio Playback Flow
```
1. User selects media file
2. main.py calls player.load_media(filepath)
3. Player detects format and routes to appropriate loader
4. Audio file loaded by pygame.mixer (playback) and librosa (analysis)
5. _analyze_audio() extracts features
6. AI module analyzes features for mood/genre
7. User presses SPACE to play
8. Main loop continuously:
   - Gets current playback position
   - Calculates corresponding audio feature frame
   - Renders visualization based on features
   - Updates display at target FPS
```

### Video Playback Flow
```
1. User selects video file
2. Player opens video with OpenCV
3. Main loop continuously:
   - Reads next frame from video
   - Converts color space (BGR→RGB)
   - Resizes to fit window
   - Converts to pygame surface
   - Blits to screen
   - Maintains target FPS
```

### Visualization Update Flow
```
Audio Position → Frame Index Calculation → Feature Lookup → Render Algorithm
     ↓
Current Time (seconds) → (time * sample_rate / hop_length) = frame_idx
     ↓
audio_features[feature_type][frame_idx] → value
     ↓
Transform value to visual parameter (height, color, position, etc.)
     ↓
Draw to screen
```

## Extension Points

### Adding New Visualization Modes

1. Add method to `GOATPlayer`:
```python
def _render_custom_visualization(self):
    # Access audio features
    pos = pygame.mixer.music.get_pos() / 1000.0
    frame_idx = int(pos * self.sample_rate / 512)
    
    # Use features for visualization
    if frame_idx < len(self.audio_features['spectral_centroid']):
        energy = self.audio_features['spectral_centroid'][frame_idx]
        # Draw based on energy
```

2. Update `cycle_visualization()`:
```python
modes = ['spectrum', 'waveform', 'particles', 'custom']
```

3. Update `render()` method:
```python
elif self.visualization_mode == 'custom':
    self._render_custom_visualization()
```

### Adding AI Features

1. Extend `AIModule` class:
```python
def new_analysis_method(self, audio_features):
    # Your analysis code
    return results
```

2. Integrate in visualization pipeline:
```python
# In GOATPlayer.render() or adaptive engine
ai_results = self.ai_module.new_analysis_method(self.audio_features)
# Use results to enhance visuals
```

### Adding Configuration Options

1. Update `Config.DEFAULT_CONFIG`:
```python
'new_section': {
    'option1': default_value,
    'option2': default_value
}
```

2. Access in code:
```python
value = config.get('new_section.option1')
```

## Performance Considerations

### Optimization Strategies

1. **Audio Analysis**: Performed once during load, not per-frame
2. **Feature Caching**: All features stored in memory for fast access
3. **Frame Rate Control**: pygame.Clock ensures consistent FPS
4. **Lazy Loading**: Video frames loaded just-in-time
5. **Efficient Drawing**: Use pygame's optimized primitives

### Memory Management

- Audio data stored as numpy array (efficient)
- Video frames discarded after rendering
- Feature matrices kept in memory (acceptable for typical song lengths)
- Configuration loaded once at startup

### CPU Usage

- Target 60 FPS leaves plenty of headroom
- Audio analysis happens on separate thread (could be implemented)
- Visualization complexity adjustable via particle count

## Cross-Platform Compatibility

### Supported Platforms
- **Linux**: Full support with system packages
- **macOS**: Full support via Homebrew
- **Windows**: Full support via pip

### Platform-Specific Notes

#### Linux
- Requires portaudio for PyAudio
- May need SDL2 development libraries

#### macOS
- Metal-accelerated graphics via pygame
- Homebrew simplifies dependency installation

#### Windows
- Self-contained pip installation
- May need Visual C++ Build Tools for some packages

## Security Considerations

1. **File Input Validation**: Checks file existence and format
2. **Path Handling**: Uses pathlib for safe path operations
3. **Error Handling**: Comprehensive try-catch blocks
4. **No Remote Code Execution**: Only loads local media files
5. **Configuration Isolation**: User config in home directory

## Testing Strategy

### Unit Testing
- Individual methods tested in isolation
- Mock pygame/librosa for testing without dependencies

### Integration Testing
- Full pipeline tests with synthetic audio
- demo.py serves as integration test

### Manual Testing
- Various media formats
- Different window sizes
- All visualization modes
- Keyboard controls

## Future Architecture Enhancements

### Planned Improvements

1. **Plugin System**
   - Dynamic loading of visualization modules
   - Third-party visualization support

2. **Async Processing**
   - Background audio analysis
   - Non-blocking UI updates

3. **GPU Acceleration**
   - OpenGL/Vulkan for complex visualizations
   - Shader-based effects

4. **Streaming Support**
   - Network stream playback
   - Real-time feature extraction

5. **Advanced AI**
   - Deep learning models for mood/genre
   - Generative visual models
   - Style transfer

6. **Distributed Architecture**
   - Separate visualization server
   - Multi-display support
   - Remote control interface

## Dependency Graph

```
main.py
  └─ goat_player.py
      ├─ pygame (graphics, audio)
      ├─ opencv-python (video)
      ├─ librosa (audio analysis)
      ├─ numpy (numerical ops)
      └─ config.py
          └─ json (persistence)

ai_module.py
  ├─ numpy
  └─ librosa

demo.py
  ├─ goat_player.py
  └─ ai_module.py
```

## Conclusion

GOAT's architecture is designed for:
- **Modularity**: Components are loosely coupled
- **Extensibility**: Easy to add new features
- **Performance**: Optimized for real-time rendering
- **Maintainability**: Clear separation of concerns
- **Cross-platform**: Works on major operating systems

The architecture balances simplicity with power, providing a solid foundation for an intelligent multimedia experience.
