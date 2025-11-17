"""
Process descriptions and explanations for common macOS processes.
Provides both technical and user-friendly descriptions.
"""

class ProcessDescriber:
    """Provides friendly descriptions for common processes."""

    # Database of common process names and their descriptions
    PROCESS_DB = {
        # System Core
        'kernel_task': {
            'technical': 'Core macOS kernel process that manages system resources, memory, and hardware.',
            'simple': 'The brain of your Mac - manages everything your computer needs to run.'
        },
        'launchd': {
            'technical': 'System initialization daemon that manages all other processes and services.',
            'simple': 'The boss process that starts and manages all other programs on your Mac.'
        },
        'systemstats': {
            'technical': 'Collects system performance metrics and analytics for macOS.',
            'simple': 'Keeps track of how your Mac is performing and what it\'s doing.'
        },
        'WindowServer': {
            'technical': 'Manages the display, windows, and graphical user interface rendering.',
            'simple': 'Shows everything you see on your screen - all windows, icons, and graphics.'
        },
        'Finder': {
            'technical': 'macOS file manager and desktop environment application.',
            'simple': 'Helps you browse files, folders, and manage your desktop icons.'
        },
        'Dock': {
            'technical': 'Application launcher and task switcher UI component.',
            'simple': 'The bar at the bottom of your screen with your favorite apps.'
        },

        # Browsers
        'Google Chrome': {
            'technical': 'Chromium-based web browser application.',
            'simple': 'Your web browser for visiting websites and browsing the internet.'
        },
        'Google Chrome Helper': {
            'technical': 'Helper process for Chrome tabs, plugins, and extensions.',
            'simple': 'Helps Chrome run websites, videos, and browser extensions.'
        },
        'Safari': {
            'technical': 'Apple\'s WebKit-based web browser.',
            'simple': 'Apple\'s web browser for visiting websites.'
        },
        'firefox': {
            'technical': 'Mozilla\'s Gecko-based web browser.',
            'simple': 'Firefox web browser for browsing the internet.'
        },

        # Communication
        'Slack': {
            'technical': 'Team collaboration and messaging platform.',
            'simple': 'Chat app for talking with your team at work.'
        },
        'Discord': {
            'technical': 'VoIP and instant messaging social platform.',
            'simple': 'Chat and voice app for talking with friends or communities.'
        },
        'Messages': {
            'technical': 'Apple\'s iMessage and SMS messaging application.',
            'simple': 'Apple\'s texting app for sending messages to friends and family.'
        },
        'Mail': {
            'technical': 'Apple\'s email client application.',
            'simple': 'Apple\'s email app for reading and sending emails.'
        },
        'Zoom': {
            'technical': 'Video conferencing and screen sharing platform.',
            'simple': 'Video call app for meetings and talking face-to-face online.'
        },
        'Microsoft Teams': {
            'technical': 'Microsoft\'s collaboration platform with chat and video conferencing.',
            'simple': 'Microsoft\'s app for team chat and video meetings.'
        },

        # Development
        'Code': {
            'technical': 'Visual Studio Code editor process.',
            'simple': 'A program for writing and editing code.'
        },
        'Electron': {
            'technical': 'Chromium-based framework for desktop applications.',
            'simple': 'Helps run certain apps on your computer (like Slack, VS Code, etc).'
        },
        'python': {
            'technical': 'Python programming language interpreter.',
            'simple': 'Running a Python program or script.'
        },
        'node': {
            'technical': 'Node.js JavaScript runtime environment.',
            'simple': 'Running a JavaScript program or web server.'
        },
        'Docker': {
            'technical': 'Container runtime and management platform.',
            'simple': 'Runs isolated programs in their own little computer environments.'
        },
        'Terminal': {
            'technical': 'Command-line interface for executing shell commands.',
            'simple': 'A text-based way to control your Mac with typed commands.'
        },
        'iTerm2': {
            'technical': 'Advanced terminal emulator for macOS.',
            'simple': 'An advanced version of Terminal for controlling your Mac with commands.'
        },

        # Media
        'Music': {
            'technical': 'Apple Music application for audio playback and library management.',
            'simple': 'Apple\'s app for playing music and managing your music library.'
        },
        'Spotify': {
            'technical': 'Music streaming service client application.',
            'simple': 'App for streaming and listening to music.'
        },
        'VLC': {
            'technical': 'Open-source multimedia player supporting various formats.',
            'simple': 'Plays videos and music in almost any format.'
        },
        'Photos': {
            'technical': 'Apple\'s photo management and editing application.',
            'simple': 'Organizes and edits your photos and videos.'
        },

        # Productivity
        'Microsoft Word': {
            'technical': 'Word processing application from Microsoft Office suite.',
            'simple': 'Microsoft\'s app for creating and editing documents.'
        },
        'Microsoft Excel': {
            'technical': 'Spreadsheet application from Microsoft Office suite.',
            'simple': 'Microsoft\'s app for working with spreadsheets and data.'
        },
        'Pages': {
            'technical': 'Apple\'s word processing application.',
            'simple': 'Apple\'s app for creating documents and letters.'
        },
        'Notes': {
            'technical': 'Apple\'s note-taking application.',
            'simple': 'Quick note-taking app for jotting down ideas.'
        },
        'Notion': {
            'technical': 'All-in-one workspace for notes, tasks, and collaboration.',
            'simple': 'Organizes your notes, to-do lists, and projects in one place.'
        },

        # System Services
        'mds_stores': {
            'technical': 'Spotlight metadata server indexing file contents.',
            'simple': 'Helps Spotlight search find your files faster by indexing them.'
        },
        'cloudd': {
            'technical': 'iCloud synchronization daemon.',
            'simple': 'Syncs your files and data with iCloud.'
        },
        'photoanalysisd': {
            'technical': 'Analyzes photos for faces, scenes, and machine learning.',
            'simple': 'Looks at your photos to recognize faces and organize them.'
        },
        'backupd': {
            'technical': 'Time Machine backup daemon.',
            'simple': 'Creates backups of your Mac with Time Machine.'
        },
        'coreaudiod': {
            'technical': 'Core Audio daemon managing audio input/output.',
            'simple': 'Manages your Mac\'s sound and audio devices.'
        },
        'bluetoothd': {
            'technical': 'Bluetooth stack daemon for wireless device management.',
            'simple': 'Manages your Bluetooth connections to wireless devices.'
        },
        'UserEventAgent': {
            'technical': 'Handles user-level system events and notifications.',
            'simple': 'Manages system notifications and alerts.'
        },
        'cfprefsd': {
            'technical': 'Core Foundation preferences daemon for app settings.',
            'simple': 'Stores and manages app preferences and settings.'
        },

        # Security
        'trustd': {
            'technical': 'Certificate trust evaluation daemon.',
            'simple': 'Checks if websites and apps are safe and trustworthy.'
        },
        'secd': {
            'technical': 'Security daemon managing keychain and encryption.',
            'simple': 'Keeps your passwords and secure information safe.'
        },

        # Java Apps
        'java': {
            'technical': 'Java Virtual Machine runtime process.',
            'simple': 'Runs programs written in the Java programming language.'
        },
        'IntelliJ IDEA': {
            'technical': 'Java IDE for software development.',
            'simple': 'A program for writing and developing Java applications.'
        },
    }

    @classmethod
    def get_description(cls, process_name: str, simple: bool = False) -> str:
        """
        Get a friendly description for a process.

        Args:
            process_name: Name of the process
            simple: If True, return simplified explanation

        Returns:
            User-friendly description of the process
        """
        # Try exact match first
        if process_name in cls.PROCESS_DB:
            desc_type = 'simple' if simple else 'technical'
            return cls.PROCESS_DB[process_name][desc_type]

        # Try case-insensitive match
        process_lower = process_name.lower()
        for key, value in cls.PROCESS_DB.items():
            if key.lower() == process_lower:
                desc_type = 'simple' if simple else 'technical'
                return value[desc_type]

        # Try partial match (contains)
        for key, value in cls.PROCESS_DB.items():
            if key.lower() in process_lower or process_lower in key.lower():
                desc_type = 'simple' if simple else 'technical'
                return value[desc_type]

        # Generic descriptions based on common patterns
        if 'helper' in process_lower:
            if simple:
                return f'A helper program that supports {process_name.replace("Helper", "").strip()}.'
            else:
                return f'Helper process providing auxiliary services for the main application.'

        if 'agent' in process_lower:
            if simple:
                return 'A background program that does tasks automatically.'
            else:
                return 'Background agent process performing automated tasks.'

        if 'd' == process_name[-1] and len(process_name) > 2:
            if simple:
                return 'A system service running in the background.'
            else:
                return 'System daemon process providing background services.'

        # Default unknown process
        if simple:
            return 'A program running on your Mac. If you don\'t recognize it, it might be a system process.'
        else:
            return 'Application or system process. Check the command line for more details about what it does.'

    @classmethod
    def is_known_process(cls, process_name: str) -> bool:
        """Check if we have specific information about this process."""
        if process_name in cls.PROCESS_DB:
            return True

        process_lower = process_name.lower()
        for key in cls.PROCESS_DB.keys():
            if key.lower() == process_lower:
                return True

        return False
