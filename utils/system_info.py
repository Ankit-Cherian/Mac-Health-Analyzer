"""
System information utilities for macOS.
Provides functions to query login items, launch agents, and system resources.
"""

import subprocess
import os
import plistlib
from pathlib import Path
from typing import List, Dict, Optional, Set


def get_login_items() -> List[Dict[str, str]]:
    """
    Get login items using AppleScript.

    Returns:
        List of dicts with 'name', 'path', and 'hidden' keys
    """
    applescript = """
    tell application "System Events"
        get the name of every login item
    end tell
    """

    try:
        result = subprocess.run(
            ["osascript", "-e", applescript], capture_output=True, text=True, timeout=5
        )

        if result.returncode == 0 and result.stdout.strip():
            # Parse comma-separated list
            names = [name.strip() for name in result.stdout.strip().split(",")]
            return [
                {
                    "name": name,
                    "type": "Login Item",
                    "enabled": True,
                    "path": "System Preferences",
                }
                for name in names
            ]
    except Exception as e:
        print(f"Error getting login items: {e}")

    return []


def fetch_launchctl_status() -> Set[str]:
    """
    Run `launchctl list` once and return loaded service labels.

    Returns:
        Set of loaded launchd labels.
    """
    try:
        result = subprocess.run(
            ["launchctl", "list"], capture_output=True, text=True, timeout=5
        )

        if result.returncode == 0 and result.stdout:
            lines = result.stdout.strip().split("\n")[1:]  # Skip header
            services = set()
            for line in lines:
                parts = line.split()
                if len(parts) >= 3:
                    services.add(parts[2])  # Label is third column
            return services
    except Exception as e:
        print(f"Error fetching launchctl status: {e}")

    return set()


def get_launch_agents(
    user_only: bool = False, loaded_labels: Optional[Set[str]] = None
) -> List[Dict[str, any]]:
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
        os.path.expanduser("~/Library/LaunchAgents"),
    ]

    if not user_only:
        directories.extend(
            [
                "/Library/LaunchAgents",
                "/System/Library/LaunchAgents",
            ]
        )

    for directory in directories:
        if not os.path.exists(directory):
            continue

        try:
            for filename in os.listdir(directory):
                if not filename.endswith(".plist"):
                    continue

                filepath = os.path.join(directory, filename)
                agent_info = parse_plist_file(filepath)

                if agent_info:
                    agent_info["type"] = "Launch Agent"
                    agent_info["location"] = directory
                    agent_info["enabled"] = agent_info["label"] in loaded_labels
                    agents.append(agent_info)
        except Exception as e:
            print(f"Error reading directory {directory}: {e}")

    return agents


def get_launch_daemons(
    loaded_labels: Optional[Set[str]] = None,
) -> List[Dict[str, any]]:
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
        "/Library/LaunchDaemons",
        "/System/Library/LaunchDaemons",
    ]

    for directory in directories:
        if not os.path.exists(directory):
            continue

        try:
            for filename in os.listdir(directory):
                if not filename.endswith(".plist"):
                    continue

                filepath = os.path.join(directory, filename)
                daemon_info = parse_plist_file(filepath)

                if daemon_info:
                    daemon_info["type"] = "Launch Daemon"
                    daemon_info["location"] = directory
                    daemon_info["enabled"] = daemon_info["label"] in loaded_labels
                    daemons.append(daemon_info)
        except Exception as e:
            print(f"Error reading directory {directory}: {e}")

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
        with open(filepath, "rb") as f:
            plist = plistlib.load(f)
    except PermissionError:
        # Skip files we don't have permission to read
        return None
    except Exception as e:
        print(f"Error parsing plist {filepath}: {e}")
        return None

    try:

        label = plist.get("Label", os.path.basename(filepath).replace(".plist", ""))
        program = plist.get("Program", "")
        program_arguments = plist.get("ProgramArguments", [])

        # Get the actual program name
        if program:
            name = os.path.basename(program)
        elif program_arguments:
            name = (
                os.path.basename(program_arguments[0]) if program_arguments else label
            )
        else:
            name = label

        return {
            "name": name,
            "label": label,
            "path": filepath,
            "program": program,
            "run_at_load": plist.get("RunAtLoad", False),
            "keep_alive": plist.get("KeepAlive", False),
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
            ["launchctl", "list"], capture_output=True, text=True, timeout=5
        )

        if result.returncode == 0:
            return label in result.stdout
    except Exception as e:
        print(f"Error checking launchd status for {label}: {e}")

    return False


def get_launchctl_list() -> List[str]:
    """
    Get list of all loaded launchd services.

    Returns:
        List of service labels
    """
    try:
        result = subprocess.run(
            ["launchctl", "list"], capture_output=True, text=True, timeout=5
        )

        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")[1:]  # Skip header
            services = []
            for line in lines:
                parts = line.split()
                if len(parts) >= 3:
                    services.append(parts[2])  # Label is third column
            return services
    except Exception as e:
        print(f"Error getting launchctl list: {e}")

    return []


def disable_login_item(name: str) -> bool:
    """
    Disable a login item using AppleScript.

    Args:
        name: Name of the login item

    Returns:
        True if successful, False otherwise
    """
    applescript = f"""
    tell application "System Events"
        delete login item "{name}"
    end tell
    """

    try:
        result = subprocess.run(
            ["osascript", "-e", applescript], capture_output=True, text=True, timeout=5
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error disabling login item {name}: {e}")
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
            ["launchctl", "unload", "-w", label],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error disabling launch agent {label}: {e}")
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
            ["launchctl", "load", "-w", plist_path],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error enabling launch agent {label}: {e}")
        return False
