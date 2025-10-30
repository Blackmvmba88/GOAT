#!/usr/bin/env python3
"""
GOAT - Intelligent Multimedia Player
Main player class with AI integration and reactive visuals
"""

import pygame
import numpy as np
import cv2
import librosa
import threading
import time
from pathlib import Path
from typing import Optional, Tuple, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class GOATPlayer:
    """
    Intelligent multimedia player with AI integration and reactive visuals
    """
    
    def __init__(self, width: int = 1280, height: int = 720):
        """Initialize the GOAT player"""
        pygame.init()
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("GOAT - Intelligent Multimedia Player")
        
        # Player state
        self.playing = False
        self.paused = False
        self.current_media = None
        self.media_type = None  # 'audio' or 'video'
        
        # Audio analysis for reactive visuals
        self.audio_data = None
        self.sample_rate = None
        self.audio_features = {
            'tempo': 0,
            'beats': [],
            'spectral_centroid': None,
            'chroma': None,
            'mfcc': None
        }
        
        # Visualization settings
        self.visualization_mode = 'spectrum'  # 'spectrum', 'waveform', 'particles', 'ai_generated'
        self.colors = self._generate_color_palette()
        
        # Video playback
        self.video_cap = None
        self.video_fps = 30
        self.video_frame = None
        
        # Clock for FPS control
        self.clock = pygame.time.Clock()
        self.target_fps = 60
        
        logger.info("GOAT Player initialized successfully")
    
    def _generate_color_palette(self) -> List[Tuple[int, int, int]]:
        """Generate a vibrant color palette for visualizations"""
        return [
            (255, 0, 128),    # Pink
            (0, 255, 255),    # Cyan
            (255, 255, 0),    # Yellow
            (128, 0, 255),    # Purple
            (0, 255, 128),    # Green
            (255, 128, 0),    # Orange
        ]
    
    def load_media(self, filepath: str) -> bool:
        """Load audio or video file"""
        path = Path(filepath)
        
        if not path.exists():
            logger.error(f"File not found: {filepath}")
            return False
        
        extension = path.suffix.lower()
        
        # Audio formats
        if extension in ['.mp3', '.wav', '.ogg', '.flac', '.m4a']:
            return self._load_audio(filepath)
        # Video formats
        elif extension in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
            return self._load_video(filepath)
        else:
            logger.error(f"Unsupported format: {extension}")
            return False
    
    def _load_audio(self, filepath: str) -> bool:
        """Load audio file and analyze for reactive visuals"""
        try:
            logger.info(f"Loading audio file: {filepath}")
            
            # Load with pygame for playback
            pygame.mixer.music.load(filepath)
            
            # Load with librosa for analysis
            self.audio_data, self.sample_rate = librosa.load(filepath, sr=None)
            
            # Perform audio analysis
            self._analyze_audio()
            
            self.current_media = filepath
            self.media_type = 'audio'
            logger.info("Audio loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading audio: {e}")
            return False
    
    def _load_video(self, filepath: str) -> bool:
        """Load video file"""
        try:
            logger.info(f"Loading video file: {filepath}")
            
            self.video_cap = cv2.VideoCapture(filepath)
            
            if not self.video_cap.isOpened():
                logger.error("Failed to open video")
                return False
            
            self.video_fps = self.video_cap.get(cv2.CAP_PROP_FPS)
            
            # Try to extract audio for reactive visuals
            # Note: In production, would use ffmpeg to extract audio track
            
            self.current_media = filepath
            self.media_type = 'video'
            logger.info("Video loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading video: {e}")
            return False
    
    def _analyze_audio(self):
        """Analyze audio for reactive visualizations"""
        if self.audio_data is None:
            return
        
        try:
            logger.info("Analyzing audio features...")
            
            # Tempo and beat tracking
            tempo, beats = librosa.beat.beat_track(y=self.audio_data, sr=self.sample_rate)
            self.audio_features['tempo'] = tempo
            self.audio_features['beats'] = librosa.frames_to_time(beats, sr=self.sample_rate)
            
            # Spectral centroid (brightness)
            self.audio_features['spectral_centroid'] = librosa.feature.spectral_centroid(
                y=self.audio_data, sr=self.sample_rate
            )[0]
            
            # Chroma features (harmonic content)
            self.audio_features['chroma'] = librosa.feature.chroma_stft(
                y=self.audio_data, sr=self.sample_rate
            )
            
            # MFCC (timbre features)
            self.audio_features['mfcc'] = librosa.feature.mfcc(
                y=self.audio_data, sr=self.sample_rate, n_mfcc=13
            )
            
            logger.info(f"Audio analysis complete. Tempo: {tempo:.2f} BPM")
            
        except Exception as e:
            logger.error(f"Error analyzing audio: {e}")
    
    def play(self):
        """Start or resume playback"""
        if self.media_type == 'audio':
            if self.paused:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.play()
        elif self.media_type == 'video':
            pass  # Video playback handled in main loop
        
        self.playing = True
        self.paused = False
        logger.info("Playback started")
    
    def pause(self):
        """Pause playback"""
        if self.media_type == 'audio':
            pygame.mixer.music.pause()
        
        self.paused = True
        logger.info("Playback paused")
    
    def stop(self):
        """Stop playback"""
        if self.media_type == 'audio':
            pygame.mixer.music.stop()
        elif self.media_type == 'video' and self.video_cap:
            self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        self.playing = False
        self.paused = False
        logger.info("Playback stopped")
    
    def _render_spectrum_visualization(self):
        """Render spectrum analyzer visualization"""
        if self.audio_features['spectral_centroid'] is not None:
            # Get current position in audio
            pos = pygame.mixer.music.get_pos() / 1000.0  # Convert to seconds
            
            if pos > 0 and pos < len(self.audio_data) / self.sample_rate:
                # Get spectral data for current time
                frame_idx = int(pos * self.sample_rate / 512)  # Hop length of 512
                
                if frame_idx < len(self.audio_features['spectral_centroid']):
                    # Draw spectrum bars
                    num_bars = 64
                    bar_width = self.width // num_bars
                    
                    for i in range(num_bars):
                        if i < len(self.audio_features['spectral_centroid']):
                            # Calculate bar height based on spectral content
                            height = int(self.audio_features['spectral_centroid'][min(frame_idx, len(self.audio_features['spectral_centroid'])-1)] / 100)
                            height = min(height, self.height - 100)
                            
                            # Color based on frequency
                            color = self.colors[i % len(self.colors)]
                            
                            # Draw bar
                            x = i * bar_width
                            y = self.height - height
                            pygame.draw.rect(self.screen, color, (x, y, bar_width - 2, height))
    
    def _render_waveform_visualization(self):
        """Render waveform visualization"""
        if self.audio_data is not None:
            pos = pygame.mixer.music.get_pos() / 1000.0
            
            if pos > 0:
                # Get segment of waveform
                start_sample = int(pos * self.sample_rate)
                end_sample = start_sample + self.sample_rate // 10  # 100ms window
                
                if end_sample < len(self.audio_data):
                    segment = self.audio_data[start_sample:end_sample]
                    
                    # Downsample for display
                    points_to_show = min(self.width, len(segment))
                    step = len(segment) // points_to_show
                    
                    points = []
                    for i in range(points_to_show):
                        sample_idx = i * step
                        if sample_idx < len(segment):
                            amplitude = segment[sample_idx]
                            x = i
                            y = int(self.height / 2 + amplitude * self.height / 4)
                            points.append((x, y))
                    
                    # Draw waveform
                    if len(points) > 1:
                        pygame.draw.lines(self.screen, self.colors[0], False, points, 2)
    
    def _render_particles_visualization(self):
        """Render particle-based visualization"""
        # Simple particle effect based on audio features
        if self.audio_features['spectral_centroid'] is not None:
            pos = pygame.mixer.music.get_pos() / 1000.0
            frame_idx = int(pos * self.sample_rate / 512)
            
            if frame_idx < len(self.audio_features['spectral_centroid']):
                energy = self.audio_features['spectral_centroid'][frame_idx]
                
                # Draw particles based on energy
                num_particles = int(energy / 50)
                for i in range(min(num_particles, 100)):
                    x = np.random.randint(0, self.width)
                    y = np.random.randint(0, self.height)
                    radius = np.random.randint(2, 8)
                    color = self.colors[i % len(self.colors)]
                    pygame.draw.circle(self.screen, color, (x, y), radius)
    
    def _render_video_frame(self):
        """Render current video frame"""
        if self.video_cap and self.playing:
            ret, frame = self.video_cap.read()
            
            if ret:
                # Convert BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Resize to fit screen
                frame = cv2.resize(frame, (self.width, self.height))
                
                # Convert to pygame surface
                frame = np.rot90(frame)
                frame = pygame.surfarray.make_surface(frame)
                
                self.screen.blit(frame, (0, 0))
                self.video_frame = frame
            else:
                # Video ended, loop or stop
                self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    def render(self):
        """Render current frame"""
        self.screen.fill((0, 0, 0))  # Clear screen
        
        if self.media_type == 'video':
            self._render_video_frame()
        elif self.media_type == 'audio' and self.playing:
            # Render audio visualization
            if self.visualization_mode == 'spectrum':
                self._render_spectrum_visualization()
            elif self.visualization_mode == 'waveform':
                self._render_waveform_visualization()
            elif self.visualization_mode == 'particles':
                self._render_particles_visualization()
        
        # Draw UI overlay
        self._render_ui()
        
        pygame.display.flip()
        self.clock.tick(self.target_fps)
    
    def _render_ui(self):
        """Render UI overlay"""
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)
        
        # Title
        title = font.render("GOAT - Intelligent Media Player", True, (255, 255, 255))
        self.screen.blit(title, (10, 10))
        
        # Status
        if self.current_media:
            filename = Path(self.current_media).name
            media_text = small_font.render(f"Media: {filename}", True, (200, 200, 200))
            self.screen.blit(media_text, (10, 50))
        
        # Playback status
        status = "Playing" if self.playing and not self.paused else "Paused" if self.paused else "Stopped"
        status_text = small_font.render(f"Status: {status}", True, (200, 200, 200))
        self.screen.blit(status_text, (10, 75))
        
        # Visualization mode (for audio)
        if self.media_type == 'audio':
            vis_text = small_font.render(f"Visualization: {self.visualization_mode}", True, (200, 200, 200))
            self.screen.blit(vis_text, (10, 100))
        
        # Controls help
        help_text = [
            "Controls:",
            "SPACE - Play/Pause",
            "S - Stop",
            "V - Change Visualization",
            "Q - Quit"
        ]
        
        y_offset = self.height - 120
        for line in help_text:
            text = small_font.render(line, True, (150, 150, 150))
            self.screen.blit(text, (10, y_offset))
            y_offset += 25
    
    def cycle_visualization(self):
        """Cycle through visualization modes"""
        modes = ['spectrum', 'waveform', 'particles']
        current_idx = modes.index(self.visualization_mode)
        self.visualization_mode = modes[(current_idx + 1) % len(modes)]
        logger.info(f"Visualization mode: {self.visualization_mode}")
    
    def handle_event(self, event):
        """Handle pygame events"""
        if event.type == pygame.QUIT:
            return False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.playing and not self.paused:
                    self.pause()
                else:
                    self.play()
            
            elif event.key == pygame.K_s:
                self.stop()
            
            elif event.key == pygame.K_v:
                self.cycle_visualization()
            
            elif event.key == pygame.K_q:
                return False
        
        elif event.type == pygame.VIDEORESIZE:
            self.width = event.w
            self.height = event.h
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        
        return True
    
    def cleanup(self):
        """Clean up resources"""
        if self.video_cap:
            self.video_cap.release()
        pygame.mixer.quit()
        pygame.quit()
        logger.info("GOAT Player closed")
