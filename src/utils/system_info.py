"""
System information utilities for macOS.
Provides functions to query login items, launch agents, and system resources.
"""

import subprocess
import os
import logging
import plistlib
import re
from pathlib import Path
from typing import List, Dict, Optional, Set

logger = logging.getLogger(__name__)


# Allowed directories for plist files (used for symlink protection)
ALLOWED_PLIST_DIRECTORIES = [
    '/Library/LaunchAgents',
    '/Library/LaunchDaemons',
    '/System/Library/LaunchAgents',
    '/System/Library/LaunchDaemons',
]


def _escape_applescript_string(s: str) -> str:
    """
    Escape special characters for AppleScript strings.

    Args:
        s: String to escape

    Returns:
        Escaped string safe for AppleScript interpolation
    """
    return s.replace('\\', '\\\\').replace('"', '\\"')


def _validate_applescript_input(name: str) -> bool:
    """
    Validate input for AppleScript to prevent command injection.

    Args:
        name: Input string to validate

    Returns:
        True if input is safe, False otherwise
    """
    # Only allow alphanumeric, spaces, dots, hyphens, underscores, and parentheses
    # This covers typical application names like "Google Chrome.app" or "Dropbox (daemon)"
    if not name or len(name) > 256:
        return False
    return bool(re.match(r'^[\w\s.\-()]+$', name))


def _is_safe_path(filepath: str, allowed_dirs: List[str]) -> bool:
    """
    Check if path is safe from symlink escape attacks.

    This function specifically protects against symlink attacks where an attacker
    places a symlink in an allowed directory that points outside of it.

    On macOS, /System/Library may be firmlinked to /System/Volumes/Data, so we
    can't simply check if the resolved path is within allowed directories.
    Instead, we only block paths that are:
    1. Actually symlinks AND
    2. The symlink target is outside of standard system directories

    Args:
        filepath: Path to validate
        allowed_dirs: List of allowed base directories

    Returns:
        True if path is safe, False if it's a symlink escape attempt
    """
    try:
        file_path = Path(filepath)

        # If it's not a symlink, it's safe (no escape possible)
        if not file_path.is_symlink():
            return True

        # It's a symlink - check where it points
        real_path = file_path.resolve()

        # Check if the symlink target is within any allowed directory
        for allowed_dir in allowed_dirs:
            allowed_path = Path(allowed_dir).resolve()
            try:
                real_path.relative_to(allowed_path)
                return True
            except ValueError:
                continue

        # Also allow system directories that may be firmlinked
        system_dirs = [
            '/System/Volumes/Data/Library',
            '/private/var',
            '/usr',
            '/bin',
            '/sbin',
        ]
        for sys_dir in system_dirs:
            try:
                real_path.relative_to(Path(sys_dir))
                return True
            except ValueError:
                continue

        # Symlink points outside allowed areas - potential attack
        return False

    except (OSError, ValueError) as e:
        logger.warning("Error validating path %s: %s", filepath, e)
        return False


def get_login_items() -> List[Dict[str, str]]:
    """
    Get login items using AppleScript.
    
    Returns:
        List of dicts with 'name', 'path', and 'hidden' keys
    """
    applescript = '''
    tell application "System Events"
        get the name of every login item
    end tell
    '''
    
    try:
        result = subprocess.run(
            ['osascript', '-e', applescript],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0 and result.stdout.strip():
            # Parse comma-separated list
            names = [name.strip() for name in result.stdout.strip().split(',')]
            return [
                {
                    'name': name,
                    'type': 'Login Item',
                    'enabled': True,
                    'path': 'System Preferences'
                }
                for name in names
            ]
    except Exception as e:
        logger.error("Error getting login items: %s", e)
    
    return []


def fetch_launchctl_status() -> Set[str]:
    """
    Run `launchctl list` once and return loaded service labels.

    Returns:
        Set of loaded launchd labels.
    """
    try:
        result = subprocess.run(
            ['launchctl', 'list'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0 and result.stdout:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            services = set()
            for line in lines:
                parts = line.split()
                if len(parts) >= 3:
                    services.add(parts[2])  # Label is third column
            return services
    except Exception as e:
        logger.error("Error fetching launchctl status: %s", e)

    return set()


def get_launch_agents(user_only: bool = False, loaded_labels: Optional[Set[str]] = None) -> List[Dict[str, any]]:
    """
    Get Launch Agents from standard directories.
    
    Args:
        user_only: If True, only check user directories
        
    Returns:
        List of dicts with agent information
    """
    agents = []

    if loaded_labels is None:
        loaded_labels = fetch_launchctl_status()
    
    # Directories to check
    directories = [
        os.path.expanduser('~/Library/LaunchAgents'),
    ]
    
    if not user_only:
        directories.extend([
            '/Library/LaunchAgents',
            '/System/Library/LaunchAgents',
        ])
    
    # Build allowed directories list for symlink protection
    allowed_dirs = directories + ALLOWED_PLIST_DIRECTORIES
    # Add user's LaunchAgents directory
    user_launch_agents = os.path.expanduser('~/Library/LaunchAgents')
    if user_launch_agents not in allowed_dirs:
        allowed_dirs.append(user_launch_agents)

    for directory in directories:
        if not os.path.exists(directory):
            continue

        try:
            for filename in os.listdir(directory):
                if not filename.endswith('.plist'):
                    continue

                filepath = os.path.join(directory, filename)

                # Symlink protection: validate path is within allowed directories
                if not _is_safe_path(filepath, allowed_dirs):
                    logger.warning("Skipping unsafe path (possible symlink attack): %s", filepath)
                    continue

                # Ensure it's a regular file (not a symlink to a directory, etc.)
                if not os.path.isfile(filepath):
                    continue

                agent_info = parse_plist_file(filepath)

                if agent_info:
                    agent_info['type'] = 'Launch Agent'
                    agent_info['location'] = directory
                    agent_info['enabled'] = agent_info['label'] in loaded_labels
                    agents.append(agent_info)
        except Exception as e:
            logger.error("Error reading directory %s: %s", directory, e)

    return agents


def get_launch_daemons(loaded_labels: Optional[Set[str]] = None) -> List[Dict[str, any]]:
    """
    Get Launch Daemons (system-level) from standard directories.
    
    Returns:
        List of dicts with daemon information
    """
    daemons = []

    if loaded_labels is None:
        loaded_labels = fetch_launchctl_status()
    
    # Directories to check (system-level only)
    directories = [
        '/Library/LaunchDaemons',
        '/System/Library/LaunchDaemons',
    ]

    for directory in directories:
        if not os.path.exists(directory):
            continue

        try:
            for filename in os.listdir(directory):
                if not filename.endswith('.plist'):
                    continue

                filepath = os.path.join(directory, filename)

                # Symlink protection: validate path is within allowed directories
                if not _is_safe_path(filepath, ALLOWED_PLIST_DIRECTORIES):
                    logger.warning("Skipping unsafe path (possible symlink attack): %s", filepath)
                    continue

                # Ensure it's a regular file
                if not os.path.isfile(filepath):
                    continue

                daemon_info = parse_plist_file(filepath)

                if daemon_info:
                    daemon_info['type'] = 'Launch Daemon'
                    daemon_info['location'] = directory
                    daemon_info['enabled'] = daemon_info['label'] in loaded_labels
                    daemons.append(daemon_info)
        except Exception as e:
            logger.error("Error reading directory %s: %s", directory, e)

    return daemons


def parse_plist_file(filepath: str) -> Optional[Dict[str, any]]:
    """
    Parse a plist file and extract relevant information.
    
    Args:
        filepath: Path to the plist file
        
    Returns:
        Dict with parsed information or None if parsing fails
    """
    try:
        with open(filepath, 'rb') as f:
            plist = plistlib.load(f)
    except PermissionError:
        # Skip files we don't have permission to read
        return None
    except Exception as e:
        logger.error("Error parsing plist %s: %s", filepath, e)
        return None
    
    try:
            
        label = plist.get('Label', os.path.basename(filepath).replace('.plist', ''))
        program = plist.get('Program', '')
        program_arguments = plist.get('ProgramArguments', [])
        
        # Get the actual program name
        if program:
            name = os.path.basename(program)
        elif program_arguments:
            name = os.path.basename(program_arguments[0]) if program_arguments else label
        else:
            name = label
            
        return {
            'name': name,
            'label': label,
            'path': filepath,
            'program': program,
            'run_at_load': plist.get('RunAtLoad', False),
            'keep_alive': plist.get('KeepAlive', False),
        }
    except Exception:
        return None


def is_launchd_item_enabled(label: str) -> bool:
    """
    Check if a launchd item is currently loaded/enabled.
    
    Args:
        label: The label of the launchd item
        
    Returns:
        True if enabled, False otherwise
    """
    try:
        result = subprocess.run(
            ['launchctl', 'list'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            return label in result.stdout
    except Exception as e:
        logger.error("Error checking launchd status for %s: %s", label, e)
    
    return False


def get_launchctl_list() -> List[str]:
    """
    Get list of all loaded launchd services.
    
    Returns:
        List of service labels
    """
    try:
        result = subprocess.run(
            ['launchctl', 'list'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            services = []
            for line in lines:
                parts = line.split()
                if len(parts) >= 3:
                    services.append(parts[2])  # Label is third column
            return services
    except Exception as e:
        logger.error("Error getting launchctl list: %s", e)
    
    return []


def disable_login_item(name: str) -> bool:
    """
    Disable a login item using AppleScript.

    Args:
        name: Name of the login item

    Returns:
        True if successful, False otherwise
    """
    # Validate input to prevent command injection
    if not _validate_applescript_input(name):
        logger.warning("Invalid login item name rejected: %s", name)
        return False

    # Escape special characters for safe interpolation
    escaped_name = _escape_applescript_string(name)

    applescript = f'''
    tell application "System Events"
        delete login item "{escaped_name}"
    end tell
    '''

    try:
        result = subprocess.run(
            ['osascript', '-e', applescript],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception as e:
        logger.error("Error disabling login item %s: %s", name, e)
        return False


def disable_launch_agent(label: str) -> bool:
    """
    Disable a launch agent using launchctl.
    
    Args:
        label: Label of the launch agent
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Unload the agent
        result = subprocess.run(
            ['launchctl', 'unload', '-w', label],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception as e:
        logger.error("Error disabling launch agent %s: %s", label, e)
        return False


def enable_launch_agent(label: str, plist_path: str) -> bool:
    """
    Enable a launch agent using launchctl.
    
    Args:
        label: Label of the launch agent
        plist_path: Path to the plist file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Load the agent
        result = subprocess.run(
            ['launchctl', 'load', '-w', plist_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception as e:
        logger.error("Error enabling launch agent %s: %s", label, e)
        return False

