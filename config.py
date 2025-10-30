#!/usr/bin/env python3
"""
GOAT Configuration Module
Manages settings and configuration for the player
"""

import json
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class Config:
    """Configuration manager for GOAT player"""
    
    DEFAULT_CONFIG = {
        'display': {
            'width': 1280,
            'height': 720,
            'fullscreen': False,
            'fps': 60
        },
        'audio': {
            'frequency': 44100,
            'channels': 2,
            'buffer_size': 512
        },
        'visualization': {
            'mode': 'spectrum',
            'enable_ai': True,
            'particle_count': 100,
            'color_themes': [
                'vibrant',
                'pastel',
                'dark',
                'neon'
            ],
            'default_theme': 'vibrant'
        },
        'ai': {
            'enable_mood_detection': True,
            'enable_genre_detection': True,
            'enable_adaptive_visuals': True,
            'enable_smart_playlist': False
        },
        'playback': {
            'auto_play': True,
            'loop': False,
            'shuffle': False
        }
    }
    
    def __init__(self, config_path: str = None):
        """Initialize configuration"""
        self.config_path = config_path or Path.home() / '.goat' / 'config.json'
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r') as f:
                    user_config = json.load(f)
                # Merge with defaults
                config = self.DEFAULT_CONFIG.copy()
                config.update(user_config)
                logger.info(f"Loaded configuration from {self.config_path}")
                return config
            else:
                logger.info("Using default configuration")
                return self.DEFAULT_CONFIG.copy()
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self) -> bool:
        """Save current configuration to file"""
        try:
            # Create directory if it doesn't exist
            Path(self.config_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            
            logger.info(f"Configuration saved to {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (supports dot notation)"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> bool:
        """Set configuration value by key (supports dot notation)"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        return True
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config = self.DEFAULT_CONFIG.copy()
        logger.info("Configuration reset to defaults")


# Color themes for visualizations
COLOR_THEMES = {
    'vibrant': [
        (255, 0, 128),    # Pink
        (0, 255, 255),    # Cyan
        (255, 255, 0),    # Yellow
        (128, 0, 255),    # Purple
        (0, 255, 128),    # Green
        (255, 128, 0),    # Orange
    ],
    'pastel': [
        (255, 179, 186),  # Pastel Pink
        (186, 255, 201),  # Pastel Green
        (186, 225, 255),  # Pastel Blue
        (255, 223, 186),  # Pastel Orange
        (230, 190, 255),  # Pastel Purple
        (255, 255, 186),  # Pastel Yellow
    ],
    'dark': [
        (139, 0, 0),      # Dark Red
        (0, 100, 0),      # Dark Green
        (0, 0, 139),      # Dark Blue
        (85, 26, 139),    # Dark Purple
        (139, 69, 19),    # Dark Brown
        (47, 79, 79),     # Dark Slate Gray
    ],
    'neon': [
        (57, 255, 20),    # Neon Green
        (255, 20, 147),   # Neon Pink
        (0, 255, 255),    # Neon Cyan
        (255, 255, 0),    # Neon Yellow
        (255, 0, 255),    # Neon Magenta
        (255, 128, 0),    # Neon Orange
    ]
}


def get_color_theme(theme_name: str):
    """Get color theme by name"""
    return COLOR_THEMES.get(theme_name, COLOR_THEMES['vibrant'])
