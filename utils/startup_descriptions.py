"""
Startup item descriptions and explanations for common macOS startup items.
Provides both technical and user-friendly descriptions with recommendations.
"""

class StartupDescriber:
    """Provides friendly descriptions for common startup items."""

    # Database of common startup items and their descriptions
    STARTUP_DB = {
        # Apple System Services
        'com.apple.loginwindow': {
            'technical': 'Manages user login, logout, and session initialization.',
            'simple': 'Handles your login screen and getting you into your Mac.',
            'should_enable': True,
            'recommendation': 'Keep enabled - essential for logging into your Mac.'
        },
        'com.apple.Finder': {
            'technical': 'Launches the Finder application for file management.',
            'simple': 'Starts the Finder app so you can browse your files.',
            'should_enable': True,
            'recommendation': 'Keep enabled - you need this to access your files and folders.'
        },
        'com.apple.Dock': {
            'technical': 'Launches the macOS Dock application launcher.',
            'simple': 'Starts the app bar at the bottom of your screen.',
            'should_enable': True,
            'recommendation': 'Keep enabled - essential for accessing your apps easily.'
        },
        'com.apple.notificationcenterui': {
            'technical': 'Notification Center UI daemon for system notifications.',
            'simple': 'Shows notifications and alerts from apps.',
            'should_enable': True,
            'recommendation': 'Keep enabled if you want to see app notifications.'
        },
        'com.apple.speech.speechsynthesisd': {
            'technical': 'Speech synthesis daemon for text-to-speech functionality.',
            'simple': 'Makes your Mac able to read text out loud.',
            'should_enable': None,
            'recommendation': 'Only needed if you use text-to-speech features.'
        },
        'com.apple.CallHistorySyncHelper': {
            'technical': 'Syncs call history between Apple devices via iCloud.',
            'simple': 'Keeps your phone call history in sync across your devices.',
            'should_enable': None,
            'recommendation': 'Disable if you don\'t use Continuity features or multiple Apple devices.'
        },
        'com.apple.photoanalysisd': {
            'technical': 'Analyzes photos for face recognition, scene detection, and memories.',
            'simple': 'Scans your photos to recognize people and organize them.',
            'should_enable': None,
            'recommendation': 'Can use significant resources. Disable if you don\'t use Photos app.'
        },
        'com.apple.cloudphotod': {
            'technical': 'iCloud Photo Library synchronization daemon.',
            'simple': 'Syncs your photos to iCloud and other devices.',
            'should_enable': None,
            'recommendation': 'Only needed if you use iCloud Photos. Can use bandwidth and storage.'
        },
        'com.apple.CrashReporterSupportHelper': {
            'technical': 'Collects crash reports and diagnostic data for Apple.',
            'simple': 'Reports when apps crash to help Apple fix bugs.',
            'should_enable': None,
            'recommendation': 'Safe to disable if you don\'t want to share crash data with Apple.'
        },

        # Cloud Services
        'com.dropbox.DropboxMacUpdate': {
            'technical': 'Dropbox automatic update service.',
            'simple': 'Keeps Dropbox up to date automatically.',
            'should_enable': None,
            'recommendation': 'Only needed if you use Dropbox and want automatic updates.'
        },
        'com.google.GoogleDrive': {
            'technical': 'Google Drive file synchronization service.',
            'simple': 'Syncs your files with Google Drive cloud storage.',
            'should_enable': None,
            'recommendation': 'Only needed if you actively use Google Drive for file syncing.'
        },
        'com.microsoft.OneDrive': {
            'technical': 'Microsoft OneDrive cloud storage synchronization.',
            'simple': 'Syncs your files with Microsoft OneDrive.',
            'should_enable': None,
            'recommendation': 'Only needed if you use OneDrive. Can use resources in background.'
        },

        # Communication Apps
        'com.slack.SlackHelper': {
            'technical': 'Slack messaging helper for background notifications.',
            'simple': 'Lets Slack show you messages even when it\'s not open.',
            'should_enable': None,
            'recommendation': 'Disable if you don\'t want Slack starting automatically or running in background.'
        },
        'com.tinyspeck.slackmacgap.helper': {
            'technical': 'Slack application auto-launcher.',
            'simple': 'Starts Slack automatically when you log in.',
            'should_enable': None,
            'recommendation': 'Disable if you don\'t need Slack to start automatically.'
        },
        'com.hnc.Discord': {
            'technical': 'Discord voice and chat application launcher.',
            'simple': 'Starts Discord automatically when you log in.',
            'should_enable': None,
            'recommendation': 'Disable if you don\'t want Discord starting automatically.'
        },
        'us.zoom.xos': {
            'technical': 'Zoom video conferencing application launcher.',
            'simple': 'Starts Zoom automatically when you log in.',
            'should_enable': None,
            'recommendation': 'Safe to disable - you can open Zoom manually when needed.'
        },
        'com.microsoft.teams': {
            'technical': 'Microsoft Teams collaboration platform launcher.',
            'simple': 'Starts Microsoft Teams automatically.',
            'should_enable': None,
            'recommendation': 'Disable if you don\'t need Teams to start automatically.'
        },

        # Productivity Apps
        'com.spotify.webhelper': {
            'technical': 'Spotify web helper for browser integration.',
            'simple': 'Helps Spotify work with web browsers.',
            'should_enable': False,
            'recommendation': 'Usually safe to disable - Spotify works fine without it.'
        },
        'com.adobe.AdobeCreativeCloud': {
            'technical': 'Adobe Creative Cloud background services and sync.',
            'simple': 'Manages Adobe apps and keeps them updated.',
            'should_enable': None,
            'recommendation': 'Only needed if you actively use Adobe Creative Cloud apps.'
        },
        'com.evernote.Evernote': {
            'technical': 'Evernote note-taking application launcher.',
            'simple': 'Starts Evernote automatically.',
            'should_enable': None,
            'recommendation': 'Disable if you don\'t need Evernote to start automatically.'
        },

        # Development Tools
        'com.docker.helper': {
            'technical': 'Docker Desktop helper for container management.',
            'simple': 'Helps Docker run containers on your Mac.',
            'should_enable': None,
            'recommendation': 'Only needed if you actively develop with Docker. Can use significant resources.'
        },
        'com.github.GitHubDesktop': {
            'technical': 'GitHub Desktop application launcher.',
            'simple': 'Starts GitHub Desktop automatically.',
            'should_enable': None,
            'recommendation': 'Safe to disable and launch manually when needed.'
        },

        # Security & VPN
        'com.nordvpn.macos.helper': {
            'technical': 'NordVPN helper service for VPN connectivity.',
            'simple': 'Helps NordVPN connect to secure servers.',
            'should_enable': None,
            'recommendation': 'Only needed if you use NordVPN regularly.'
        },
        'com.expressvpn.ExpressVPN': {
            'technical': 'ExpressVPN service for secure network connections.',
            'simple': 'Manages your ExpressVPN connections.',
            'should_enable': None,
            'recommendation': 'Only needed if you use ExpressVPN regularly.'
        },

        # Utilities
        'com.apple.backupd': {
            'technical': 'Time Machine backup daemon.',
            'simple': 'Automatically backs up your Mac with Time Machine.',
            'should_enable': True,
            'recommendation': 'Keep enabled if you use Time Machine for backups - very important for data safety!'
        },
        'com.apple.metadata.mds': {
            'technical': 'Spotlight metadata indexing daemon.',
            'simple': 'Helps Spotlight search find your files quickly.',
            'should_enable': True,
            'recommendation': 'Keep enabled - makes searching your Mac much faster.'
        },
        'com.google.keystone': {
            'technical': 'Google Software Update service.',
            'simple': 'Keeps Google apps like Chrome up to date.',
            'should_enable': None,
            'recommendation': 'Safe to disable if you prefer to update apps manually.'
        },
        'com.microsoft.autoupdate': {
            'technical': 'Microsoft AutoUpdate service for Office and other apps.',
            'simple': 'Keeps Microsoft apps updated automatically.',
            'should_enable': None,
            'recommendation': 'Safe to disable if you prefer to update manually.'
        },
        'com.apple.softwareupdated': {
            'technical': 'macOS system software update daemon.',
            'simple': 'Checks for and downloads macOS updates.',
            'should_enable': True,
            'recommendation': 'Keep enabled - important for security updates!'
        },
    }

    @classmethod
    def get_description(cls, item_name: str, technical: bool = False) -> str:
        """
        Get description for a startup item.

        Args:
            item_name: Name or label of the startup item
            technical: Whether to return technical description

        Returns:
            Description string
        """
        # Try exact match first
        if item_name in cls.STARTUP_DB:
            return cls.STARTUP_DB[item_name]['technical' if technical else 'simple']

        # Try partial match (check if any known item is in the name)
        for known_item, data in cls.STARTUP_DB.items():
            if known_item.lower() in item_name.lower():
                return data['technical' if technical else 'simple']

        # Generic description
        if technical:
            return "Third-party or custom startup item. Launches automatically when you log in."
        else:
            return "This app or service starts automatically when you log into your Mac."

    @classmethod
    def get_recommendation(cls, item_name: str, item_type: str = None) -> dict:
        """
        Get recommendation for a startup item.

        Args:
            item_name: Name or label of the startup item
            item_type: Type of item (Login Item, Launch Agent, Launch Daemon)

        Returns:
            Dict with 'should_enable' (True/False/None) and 'reason' string
        """
        # Try exact match
        if item_name in cls.STARTUP_DB:
            data = cls.STARTUP_DB[item_name]
            return {
                'should_enable': data['should_enable'],
                'reason': data['recommendation']
            }

        # Try partial match
        for known_item, data in cls.STARTUP_DB.items():
            if known_item.lower() in item_name.lower():
                return {
                    'should_enable': data['should_enable'],
                    'reason': data['recommendation']
                }

        # Generic recommendations based on type
        if item_type == 'Launch Daemon':
            return {
                'should_enable': None,
                'reason': 'Launch Daemons run system-level services. Be careful disabling unless you know what it does.'
            }
        elif item_type == 'Launch Agent':
            if 'apple' in item_name.lower():
                return {
                    'should_enable': True,
                    'reason': 'This appears to be an Apple system service. Usually best to keep enabled.'
                }
            else:
                return {
                    'should_enable': None,
                    'reason': 'Third-party service. Disable if you don\'t recognize it or don\'t need it to start automatically.'
                }
        else:  # Login Item
            return {
                'should_enable': None,
                'reason': 'Apps that start when you log in. Disable any you don\'t need to start automatically to speed up login.'
            }

    @classmethod
    def is_recognized(cls, item_name: str) -> bool:
        """
        Check if a startup item is in the database.

        Args:
            item_name: Name or label of the startup item

        Returns:
            True if recognized, False otherwise
        """
        if item_name in cls.STARTUP_DB:
            return True

        # Check partial match
        for known_item in cls.STARTUP_DB.keys():
            if known_item.lower() in item_name.lower():
                return True

        return False
