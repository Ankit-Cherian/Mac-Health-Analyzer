"""
Font management for the Mac Health Analyzer - Neo-Brutalist Earth Edition.
Downloads and loads distinctive Google Fonts (Sora, DM Sans, IBM Plex Mono).
"""

import os
import requests
from pathlib import Path
from PyQt6.QtGui import QFontDatabase, QFont


# Font URLs from Google Fonts - Distinctive, readable fonts
FONTS = {
    'Sora': {
        'weights': {
            300: 'https://github.com/google/fonts/raw/main/ofl/sora/Sora-Light.ttf',
            400: 'https://github.com/google/fonts/raw/main/ofl/sora/Sora-Regular.ttf',
            600: 'https://github.com/google/fonts/raw/main/ofl/sora/Sora-SemiBold.ttf',
            700: 'https://github.com/google/fonts/raw/main/ofl/sora/Sora-Bold.ttf',
            800: 'https://github.com/google/fonts/raw/main/ofl/sora/Sora-ExtraBold.ttf',
        }
    },
    'DM Sans': {
        'weights': {
            300: 'https://github.com/google/fonts/raw/main/ofl/dmsans/DMSans-Light.ttf',
            400: 'https://github.com/google/fonts/raw/main/ofl/dmsans/DMSans-Regular.ttf',
            500: 'https://github.com/google/fonts/raw/main/ofl/dmsans/DMSans-Medium.ttf',
            600: 'https://github.com/google/fonts/raw/main/ofl/dmsans/DMSans-SemiBold.ttf',
            700: 'https://github.com/google/fonts/raw/main/ofl/dmsans/DMSans-Bold.ttf',
        }
    },
    'IBM Plex Mono': {
        'weights': {
            300: 'https://github.com/google/fonts/raw/main/ofl/ibmplexmono/IBMPlexMono-Light.ttf',
            400: 'https://github.com/google/fonts/raw/main/ofl/ibmplexmono/IBMPlexMono-Regular.ttf',
            500: 'https://github.com/google/fonts/raw/main/ofl/ibmplexmono/IBMPlexMono-Medium.ttf',
            600: 'https://github.com/google/fonts/raw/main/ofl/ibmplexmono/IBMPlexMono-SemiBold.ttf',
            700: 'https://github.com/google/fonts/raw/main/ofl/ibmplexmono/IBMPlexMono-Bold.ttf',
        }
    }
}


class FontManager:
    """
    Manages font loading and application.
    """

    def __init__(self, assets_dir: str = None):
        """
        Initialize the font manager.

        Args:
            assets_dir: Directory to store font files
        """
        if assets_dir is None:
            # Use assets/fonts in project directory
            project_dir = Path(__file__).parent.parent
            assets_dir = project_dir / 'assets' / 'fonts'

        self.assets_dir = Path(assets_dir)
        self.assets_dir.mkdir(parents=True, exist_ok=True)

        self.loaded_fonts = {}

    def download_font(self, font_name: str, weight: int, url: str) -> str:
        """
        Download a font file from URL.

        Args:
            font_name: Name of the font
            weight: Font weight
            url: URL to download from

        Returns:
            Path to downloaded font file
        """
        # Create safe filename
        safe_name = font_name.replace(' ', '_')
        filename = f"{safe_name}_{weight}.ttf"
        filepath = self.assets_dir / filename

        # Skip if already downloaded
        if filepath.exists():
            return str(filepath)

        try:
            print(f"Downloading {font_name} (weight {weight})...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            with open(filepath, 'wb') as f:
                f.write(response.content)

            print(f"Downloaded {filename}")
            return str(filepath)
        except Exception as e:
            print(f"Error downloading font {font_name}: {e}")
            return None

    def load_fonts(self):
        """
        Load all required fonts.
        Downloads fonts if not already present.
        """
        for font_name, font_data in FONTS.items():
            print(f"\nLoading {font_name}...")

            for weight, url in font_data['weights'].items():
                filepath = self.download_font(font_name, weight, url)

                if filepath and os.path.exists(filepath):
                    font_id = QFontDatabase.addApplicationFont(filepath)

                    if font_id != -1:
                        families = QFontDatabase.applicationFontFamilies(font_id)
                        if families:
                            family_name = families[0]
                            self.loaded_fonts[f"{font_name}_{weight}"] = family_name
                            print(f"Loaded {family_name} (weight {weight})")
                    else:
                        print(f"Failed to load {filepath}")

        print("\nFont loading complete!")

    def get_display_font(self, size: int = 24, weight: int = 700) -> QFont:
        """
        Get the display font (Sora for headings).

        Args:
            size: Font size
            weight: Font weight (300, 400, 600, 700, 800)

        Returns:
            QFont object
        """
        # Use Sora for headings
        font_key = f"Sora_{weight}"

        if font_key in self.loaded_fonts:
            font = QFont(self.loaded_fonts[font_key], size)
        else:
            # Fallback to a distinctive system font
            font = QFont("Helvetica Neue", size)

        # Map weight to QFont weight
        if weight <= 300:
            font.setWeight(QFont.Weight.Light)
        elif weight <= 400:
            font.setWeight(QFont.Weight.Normal)
        elif weight <= 600:
            font.setWeight(QFont.Weight.DemiBold)
        elif weight <= 700:
            font.setWeight(QFont.Weight.Bold)
        else:
            font.setWeight(QFont.Weight.ExtraBold)

        return font

    def get_mono_font(self, size: int = 12, weight: int = 400) -> QFont:
        """
        Get the monospace font (IBM Plex Mono).

        Args:
            size: Font size
            weight: Font weight (300, 400, 500, 600, 700)

        Returns:
            QFont object
        """
        # Use IBM Plex Mono if available, fallback to Menlo
        font_key = f"IBM Plex Mono_{weight}"

        if font_key in self.loaded_fonts:
            font = QFont(self.loaded_fonts[font_key], size)
        else:
            # Fallback to Menlo (macOS default monospace)
            font = QFont("Menlo", size)

        # Map weight to QFont weight
        if weight <= 300:
            font.setWeight(QFont.Weight.Light)
        elif weight <= 400:
            font.setWeight(QFont.Weight.Normal)
        elif weight <= 500:
            font.setWeight(QFont.Weight.Medium)
        elif weight <= 600:
            font.setWeight(QFont.Weight.DemiBold)
        else:
            font.setWeight(QFont.Weight.Bold)

        return font

    def get_font_families(self) -> dict:
        """
        Get loaded font families.

        Returns:
            Dict of font families
        """
        return self.loaded_fonts


# Global font manager instance
_font_manager = None


def get_font_manager() -> FontManager:
    """
    Get the global font manager instance.

    Returns:
        FontManager instance
    """
    global _font_manager
    if _font_manager is None:
        _font_manager = FontManager()
    return _font_manager
