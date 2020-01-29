from pathlib import Path
import pygame


MAPS_DIR = Path('maps')

MAPS = {
    'haven': {
        'arena': pygame.image.load(str(MAPS_DIR / 'haven' / 'haven.png')),
        'background': None
    }
}
