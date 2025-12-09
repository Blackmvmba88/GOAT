#!/usr/bin/env python3
"""
GOAT Demo Script
Demonstrates the capabilities of the GOAT player without requiring media files
"""

import pygame
import numpy as np
import time
import sys
from goat_player import GOATPlayer
from ai_module import AIModule, AdaptiveVisualEngine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_test_audio(duration: float = 5.0, sample_rate: int = 44100):
    """Generate test audio signal"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Create a complex signal with multiple frequencies
    signal = (
        0.3 * np.sin(2 * np.pi * 440 * t) +  # A4 note
        0.2 * np.sin(2 * np.pi * 554 * t) +  # C#5 note
        0.15 * np.sin(2 * np.pi * 659 * t)   # E5 note
    )
    
    # Add some rhythm
    beat_freq = 2  # 2 beats per second (120 BPM)
    envelope = 0.5 + 0.5 * np.sin(2 * np.pi * beat_freq * t)
    signal = signal * envelope
    
    return signal, sample_rate


def demo_visualizations():
    """Demo the visualization capabilities"""
    logger.info("Starting GOAT Visualization Demo...")
    
    # Initialize player
    player = GOATPlayer(width=1280, height=720)
    
    # Generate test audio
    logger.info("Generating test audio signal...")
    audio_data, sample_rate = generate_test_audio(duration=10.0)
    player.audio_data = audio_data
    player.sample_rate = sample_rate
    player.media_type = 'audio'
    
    # Analyze audio
    player._analyze_audio()
    
    # Initialize AI module
    ai_module = AIModule()
    visual_engine = AdaptiveVisualEngine(ai_module)
    
    # Detect mood
    mood = ai_module.analyze_mood(player.audio_features)
    logger.info(f"Detected mood: {mood}")
    
    # Get adaptive palette
    palette = ai_module.generate_adaptive_palette(mood)
    player.colors = palette
    
    # Demo message
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 32)
    
    logger.info("\n" + "="*60)
    logger.info("GOAT DEMO MODE")
    logger.info("="*60)
    logger.info("This demo showcases GOAT's visualization capabilities")
    logger.info("with synthesized audio. Press SPACE to toggle demo mode.")
    logger.info("\nControls:")
    logger.info("  V - Cycle visualizations")
    logger.info("  Q - Quit demo")
    logger.info("="*60 + "\n")
    
    # Demo loop
    running = True
    demo_active = False
    demo_start_time = time.time()
    
    visualization_cycle_time = 5.0  # Change visualization every 5 seconds
    last_cycle = time.time()
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_SPACE:
                    demo_active = not demo_active
                    if demo_active:
                        logger.info("Demo mode ACTIVATED")
                    else:
                        logger.info("Demo mode PAUSED")
                elif event.key == pygame.K_v:
                    player.cycle_visualization()
        
        # Clear screen
        player.screen.fill((0, 0, 0))
        
        if demo_active:
            # Simulate playback position
            current_time = (time.time() - demo_start_time) % 10.0
            
            # Auto-cycle visualizations
            if time.time() - last_cycle > visualization_cycle_time:
                player.cycle_visualization()
                last_cycle = time.time()
            
            # Simulate audio playback for visualizations
            player.playing = True
            
            # Render visualization based on synthetic position
            frame_idx = int(current_time * player.sample_rate / 512)
            
            if player.visualization_mode == 'spectrum':
                # Draw spectrum bars
                num_bars = 64
                bar_width = player.width // num_bars
                
                for i in range(num_bars):
                    if frame_idx < len(player.audio_features['spectral_centroid']):
                        sc = player.audio_features['spectral_centroid']
                        height = int(sc[min(frame_idx, len(sc)-1)] / 100)
                        height = min(height, player.height - 200)
                        
                        # Animate based on time
                        phase = (current_time * 2 + i * 0.1) % (2 * np.pi)
                        height = int(height * (0.5 + 0.5 * np.sin(phase)))
                        
                        color = player.colors[i % len(player.colors)]
                        x = i * bar_width
                        y = player.height - height - 100
                        pygame.draw.rect(player.screen, color, (x, y, bar_width - 2, height))
            
            elif player.visualization_mode == 'waveform':
                # Draw animated waveform
                points = []
                for x in range(player.width):
                    phase = (current_time * 4 + x * 0.01) % (2 * np.pi)
                    y = int(player.height / 2 + 100 * np.sin(phase))
                    points.append((x, y))
                
                if len(points) > 1:
                    pygame.draw.lines(player.screen, player.colors[0], False, points, 3)
            
            elif player.visualization_mode == 'particles':
                # Draw animated particles
                num_particles = 100
                for i in range(num_particles):
                    phase = (current_time + i * 0.1) % 10.0
                    x = int((player.width / 2) + 300 * np.cos(phase * np.pi / 5 + i))
                    y = int((player.height / 2) + 200 * np.sin(phase * np.pi / 5 + i))
                    radius = int(5 + 3 * np.sin(current_time * 3 + i))
                    color = player.colors[i % len(player.colors)]
                    pygame.draw.circle(player.screen, color, (x, y), radius)
        
        else:
            player.playing = False
        
        # Draw UI
        title_text = font.render("GOAT DEMO MODE", True, (255, 255, 255))
        player.screen.blit(title_text, (player.width // 2 - 200, 50))
        
        status = "Active (press SPACE to pause)" if demo_active else "Paused (press SPACE to start)"
        status_text = small_font.render(status, True, (200, 200, 200))
        player.screen.blit(status_text, (player.width // 2 - 200, 110))
        
        mood_text = small_font.render(f"Mood: {mood}", True, (150, 255, 150))
        player.screen.blit(mood_text, (20, player.height - 150))
        
        viz_text = small_font.render(f"Visualization: {player.visualization_mode}", True, (150, 200, 255))
        player.screen.blit(viz_text, (20, player.height - 110))
        
        help_text = small_font.render("Controls: SPACE=Play/Pause | V=Change Viz | Q=Quit", True, (180, 180, 180))
        player.screen.blit(help_text, (20, player.height - 40))
        
        # Update display
        pygame.display.flip()
        player.clock.tick(60)
    
    # Cleanup
    player.cleanup()
    logger.info("Demo ended")


def main():
    """Main entry point for demo"""
    try:
        demo_visualizations()
    except KeyboardInterrupt:
        logger.info("\nDemo interrupted by user")
    except Exception as e:
        logger.error(f"Demo error: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
