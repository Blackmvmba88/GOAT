#!/usr/bin/env python3
"""
GOAT - Intelligent Multimedia Player
Main entry point with cross-platform support
"""

import sys
import argparse
from pathlib import Path
import pygame
import logging

from goat_player import GOATPlayer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for GOAT player"""
    parser = argparse.ArgumentParser(
        description='GOAT - Intelligent Multimedia Player with AI and Reactive Visuals'
    )
    parser.add_argument(
        'media',
        nargs='?',
        help='Path to media file (audio or video)'
    )
    parser.add_argument(
        '--width',
        type=int,
        default=1280,
        help='Window width (default: 1280)'
    )
    parser.add_argument(
        '--height',
        type=int,
        default=720,
        help='Window height (default: 720)'
    )
    parser.add_argument(
        '--fullscreen',
        action='store_true',
        help='Start in fullscreen mode'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize player
        logger.info("Starting GOAT Intelligent Multimedia Player...")
        player = GOATPlayer(width=args.width, height=args.height)
        
        # Load media if provided
        if args.media:
            if not player.load_media(args.media):
                logger.error("Failed to load media file")
                return 1
            player.play()
        
        # Main loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if not player.handle_event(event):
                    running = False
                    break
            
            # Render frame
            player.render()
        
        # Cleanup
        player.cleanup()
        logger.info("GOAT Player closed gracefully")
        return 0
        
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
