import subprocess

import logging

logger:logging.Logger = logging.getLogger(__name__)

def get_ssid_macos():
    """
    Retrieve the SSID of the connected WiFi on macOS through a shell command.
    """
    try:
        result = subprocess.check_output(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"])
        for line in result.decode("utf-8").splitlines():
            if " SSID: " in line:
                return line.split(":")[1].strip()
    except Exception as e:
        logger.error(f"Error getting SSID: {e}")
        return None

def get_ipv4_macos():
    """
    Retrieve the IPv4 address of the connected WiFi on macOS through a shell command.
    """
    try:
        result = subprocess.check_output(["ifconfig", "en0"])
        for line in result.decode("utf-8").splitlines():
            if "inet " in line and not "inet6" in line:
                return line.split()[1]
    except Exception as e:
        logger.error(f"Error getting IPv4: {e}")
        return None

def get_wifi_info_macos():
    ssid = get_ssid_macos()
    ipv4 = get_ipv4_macos()
    return {'SSID': ssid, 'IPv4 Address': ipv4}

if __name__ == "__main__":
    info = get_wifi_info_macos()
    for key, value in info.items():
        print(f"{key}: {value}")
