#!/usr/bin/env python3
"""
GOAT - Reproductor Multimedia Inteligente
Clase principal del reproductor con integración IA y visuales reactivos
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

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class GOATPlayer:
    """
    Reproductor multimedia inteligente con integración IA y visuales reactivos
    """
    
    def __init__(self, width: int = 1280, height: int = 720):
        """Inicializar el reproductor GOAT"""
        pygame.init()
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("GOAT - Reproductor Multimedia Inteligente")
        
        # Estado del reproductor
        self.playing = False
        self.paused = False
        self.current_media = None
        self.media_type = None  # 'audio' o 'video'
        
        # Análisis de audio para visuales reactivos
        self.audio_data = None
        self.sample_rate = None
        self.audio_features = {
            'tempo': 0,
            'beats': [],
            'spectral_centroid': None,
            'chroma': None,
            'mfcc': None
        }
        
        # Configuración de visualización
        self.visualization_mode = 'spectrum'  # 'spectrum', 'waveform', 'particles', 'ai_generated'
        self.colors = self._generate_color_palette()
        
        # Reproducción de video
        self.video_cap = None
        self.video_fps = 30
        self.video_frame = None
        
        # Reloj para control de FPS
        self.clock = pygame.time.Clock()
        self.target_fps = 60
        
        logger.info("Reproductor GOAT inicializado exitosamente")
    
    def _generate_color_palette(self) -> List[Tuple[int, int, int]]:
        """Generar una paleta de colores vibrante para visualizaciones"""
        return [
            (255, 0, 128),    # Rosa
            (0, 255, 255),    # Cian
            (255, 255, 0),    # Amarillo
            (128, 0, 255),    # Púrpura
            (0, 255, 128),    # Verde
            (255, 128, 0),    # Naranja
        ]
    
    def load_media(self, filepath: str) -> bool:
        """Cargar archivo de audio o video"""
        path = Path(filepath)
        
        if not path.exists():
            logger.error(f"Archivo no encontrado: {filepath}")
            return False
        
        extension = path.suffix.lower()
        
        # Formatos de audio
        if extension in ['.mp3', '.wav', '.ogg', '.flac', '.m4a']:
            return self._load_audio(filepath)
        # Formatos de video
        elif extension in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
            return self._load_video(filepath)
        else:
            logger.error(f"Formato no compatible: {extension}")
            return False
    
    def _load_audio(self, filepath: str) -> bool:
        """Cargar archivo de audio y analizar para visuales reactivos"""
        try:
            logger.info(f"Cargando archivo de audio: {filepath}")
            
            # Cargar con pygame para reproducción
            pygame.mixer.music.load(filepath)
            
            # Cargar con librosa para análisis
            self.audio_data, self.sample_rate = librosa.load(filepath, sr=None)
            
            # Realizar análisis de audio
            self._analyze_audio()
            
            self.current_media = filepath
            self.media_type = 'audio'
            logger.info("Audio cargado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error al cargar audio: {e}")
            return False
    
    def _load_video(self, filepath: str) -> bool:
        """Cargar archivo de video"""
        try:
            logger.info(f"Cargando archivo de video: {filepath}")
            
            self.video_cap = cv2.VideoCapture(filepath)
            
            if not self.video_cap.isOpened():
                logger.error("Error al abrir video")
                return False
            
            self.video_fps = self.video_cap.get(cv2.CAP_PROP_FPS)
            
            # Intentar extraer audio para visuales reactivos
            # Nota: En producción, usaría ffmpeg para extraer pista de audio
            
            self.current_media = filepath
            self.media_type = 'video'
            logger.info("Video cargado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error al cargar video: {e}")
            return False
    
    def _analyze_audio(self):
        """Analizar audio para visualizaciones reactivas"""
        if self.audio_data is None:
            return
        
        try:
            logger.info("Analizando características de audio...")
            
            # Tempo y seguimiento de ritmo
            tempo, beats = librosa.beat.beat_track(y=self.audio_data, sr=self.sample_rate)
            self.audio_features['tempo'] = tempo
            self.audio_features['beats'] = librosa.frames_to_time(beats, sr=self.sample_rate)
            
            # Centroide espectral (brillo)
            self.audio_features['spectral_centroid'] = librosa.feature.spectral_centroid(
                y=self.audio_data, sr=self.sample_rate
            )[0]
            
            # Características de chroma (contenido armónico)
            self.audio_features['chroma'] = librosa.feature.chroma_stft(
                y=self.audio_data, sr=self.sample_rate
            )
            
            # MFCC (características de timbre)
            self.audio_features['mfcc'] = librosa.feature.mfcc(
                y=self.audio_data, sr=self.sample_rate, n_mfcc=13
            )
            
            logger.info(f"Análisis de audio completo. Tempo: {tempo:.2f} BPM")
            
        except Exception as e:
            logger.error(f"Error al analizar audio: {e}")
    
    def play(self):
        """Iniciar o reanudar reproducción"""
        if self.media_type == 'audio':
            if self.paused:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.play()
        elif self.media_type == 'video':
            pass  # Reproducción de video manejada en bucle principal
        
        self.playing = True
        self.paused = False
        logger.info("Reproducción iniciada")
    
    def pause(self):
        """Pausar reproducción"""
        if self.media_type == 'audio':
            pygame.mixer.music.pause()
        
        self.paused = True
        logger.info("Reproducción pausada")
    
    def stop(self):
        """Detener reproducción"""
        if self.media_type == 'audio':
            pygame.mixer.music.stop()
        elif self.media_type == 'video' and self.video_cap:
            self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        self.playing = False
        self.paused = False
        logger.info("Reproducción detenida")
    
    def _render_spectrum_visualization(self):
        """Renderizar visualización de analizador de espectro"""
        if self.audio_features['spectral_centroid'] is not None:
            # Obtener posición actual en audio
            pos = pygame.mixer.music.get_pos() / 1000.0  # Convertir a segundos
            
            if pos > 0 and pos < len(self.audio_data) / self.sample_rate:
                # Obtener datos espectrales para tiempo actual
                frame_idx = int(pos * self.sample_rate / 512)  # Longitud de salto de 512
                
                if frame_idx < len(self.audio_features['spectral_centroid']):
                    # Dibujar barras de espectro
                    num_bars = 64
                    bar_width = self.width // num_bars
                    
                    for i in range(num_bars):
                        if i < len(self.audio_features['spectral_centroid']):
                            # Calcular altura de barra basada en contenido espectral
                            height = int(self.audio_features['spectral_centroid'][min(frame_idx, len(self.audio_features['spectral_centroid'])-1)] / 100)
                            height = min(height, self.height - 100)
                            
                            # Color basado en frecuencia
                            color = self.colors[i % len(self.colors)]
                            
                            # Dibujar barra
                            x = i * bar_width
                            y = self.height - height
                            pygame.draw.rect(self.screen, color, (x, y, bar_width - 2, height))
    
    def _render_waveform_visualization(self):
        """Renderizar visualización de forma de onda"""
        if self.audio_data is not None:
            pos = pygame.mixer.music.get_pos() / 1000.0
            
            if pos > 0:
                # Obtener segmento de forma de onda
                start_sample = int(pos * self.sample_rate)
                end_sample = start_sample + self.sample_rate // 10  # Ventana de 100ms
                
                if end_sample < len(self.audio_data):
                    segment = self.audio_data[start_sample:end_sample]
                    
                    # Submuestreo para visualización
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
                    
                    # Dibujar forma de onda
                    if len(points) > 1:
                        pygame.draw.lines(self.screen, self.colors[0], False, points, 2)
    
    def _render_particles_visualization(self):
        """Renderizar visualización basada en partículas"""
        # Efecto simple de partículas basado en características de audio
        if self.audio_features['spectral_centroid'] is not None:
            pos = pygame.mixer.music.get_pos() / 1000.0
            frame_idx = int(pos * self.sample_rate / 512)
            
            if frame_idx < len(self.audio_features['spectral_centroid']):
                energy = self.audio_features['spectral_centroid'][frame_idx]
                
                # Dibujar partículas basadas en energía
                num_particles = int(energy / 50)
                for i in range(min(num_particles, 100)):
                    x = np.random.randint(0, self.width)
                    y = np.random.randint(0, self.height)
                    radius = np.random.randint(2, 8)
                    color = self.colors[i % len(self.colors)]
                    pygame.draw.circle(self.screen, color, (x, y), radius)
    
    def _render_video_frame(self):
        """Renderizar fotograma de video actual"""
        if self.video_cap and self.playing:
            ret, frame = self.video_cap.read()
            
            if ret:
                # Convertir BGR a RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Redimensionar para ajustar a pantalla
                frame = cv2.resize(frame, (self.width, self.height))
                
                # Convertir a superficie pygame
                frame = np.rot90(frame)
                frame = pygame.surfarray.make_surface(frame)
                
                self.screen.blit(frame, (0, 0))
                self.video_frame = frame
            else:
                # Video terminado, repetir o detener
                self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    def render(self):
        """Renderizar fotograma actual"""
        self.screen.fill((0, 0, 0))  # Limpiar pantalla
        
        if self.media_type == 'video':
            self._render_video_frame()
        elif self.media_type == 'audio' and self.playing:
            # Renderizar visualización de audio
            if self.visualization_mode == 'spectrum':
                self._render_spectrum_visualization()
            elif self.visualization_mode == 'waveform':
                self._render_waveform_visualization()
            elif self.visualization_mode == 'particles':
                self._render_particles_visualization()
        
        # Dibujar superposición de UI
        self._render_ui()
        
        pygame.display.flip()
        self.clock.tick(self.target_fps)
    
    def _render_ui(self):
        """Renderizar superposición de interfaz"""
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)
        
        # Título
        title = font.render("GOAT - Reproductor Multimedia Inteligente", True, (255, 255, 255))
        self.screen.blit(title, (10, 10))
        
        # Estado
        if self.current_media:
            filename = Path(self.current_media).name
            media_text = small_font.render(f"Medio: {filename}", True, (200, 200, 200))
            self.screen.blit(media_text, (10, 50))
        
        # Estado de reproducción
        status = "Reproduciendo" if self.playing and not self.paused else "Pausado" if self.paused else "Detenido"
        status_text = small_font.render(f"Estado: {status}", True, (200, 200, 200))
        self.screen.blit(status_text, (10, 75))
        
        # Modo de visualización (para audio)
        if self.media_type == 'audio':
            vis_text = small_font.render(f"Visualización: {self.visualization_mode}", True, (200, 200, 200))
            self.screen.blit(vis_text, (10, 100))
        
        # Ayuda de controles
        help_text = [
            "Controles:",
            "ESPACIO - Reproducir/Pausar",
            "S - Detener",
            "V - Cambiar Visualización",
            "Q - Salir"
        ]
        
        y_offset = self.height - 120
        for line in help_text:
            text = small_font.render(line, True, (150, 150, 150))
            self.screen.blit(text, (10, y_offset))
            y_offset += 25
    
    def cycle_visualization(self):
        """Alternar entre modos de visualización"""
        modes = ['spectrum', 'waveform', 'particles']
        current_idx = modes.index(self.visualization_mode)
        self.visualization_mode = modes[(current_idx + 1) % len(modes)]
        logger.info(f"Modo de visualización: {self.visualization_mode}")
    
    def handle_event(self, event):
        """Manejar eventos de pygame"""
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
        """Limpiar recursos"""
        if self.video_cap:
            self.video_cap.release()
        pygame.mixer.quit()
        pygame.quit()
        logger.info("Reproductor GOAT cerrado")
