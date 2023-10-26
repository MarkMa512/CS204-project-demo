import subprocess
import ipaddress

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

def filter_private_ips(ip_address_list: list[str])->list[str]:
    """
    Filter out private IP addresses from the provided list.
    
    :param ip_list: List of IP addresses.
    :return: List of public IP addresses.
    """
    public_ip_address_list = []
    
    for ip in ip_address_list:
        if ipaddress.ip_address(ip).is_private:
            continue
        public_ip_address_list.append(ip)
        
    return public_ip_address_list

import ipaddress

def to_cidr(ip_address_range:str)->str:
    """
    Convert given IP address range into CIDR format.

    :param ip_address_range: IP address range in CIDR or "start - end" format.
    :return: String representation of the IP address range in CIDR format.
    """

    # If the input is already in CIDR format, return it
    try:
        ip_network = ipaddress.ip_network(ip_address_range, strict=False)
        logger.info(f"{ip_address_range} is already in CIDR format. ")
        return str(ip_network)
    except ValueError:
        pass

    logger.info(f"Converting {ip_address_range} to CIDR format. ")

    # If not, then process the "start - end" format
    start_ip, end_ip = [ip.strip() for ip in ip_address_range.split('-')]
    
    try:
        combined_ip_network = ipaddress.summarize_address_range(ipaddress.ip_address(start_ip), ipaddress.ip_address(end_ip))
        return ', '.join(str(net) for net in combined_ip_network)
    except ValueError:
        raise ValueError(f"Could not convert {ip_address_range} to CIDR notation")

        
def match_ip_to_org(ip_address_range_dict:dict[str:str], ip_address:str)->tuple[str:str]:
    """
    Find the IP address range and organization for a given IP address.

    :param ip_address_range_dict: Dictionary with IP address ranges as keys and organizations as values.
    :param ip_address: IP address to search for.
    :return: Tuple of (IP address range, organization) or None.
    """
    logger.info(f"Checking if {ip_address} was found previously")
    for ip_range, org in ip_address_range_dict.items():
        # Convert the range and IP to network and IP objects
        try:
            if ipaddress.ip_address(ip_address) in ipaddress.ip_network(ip_range):
                logger.info(f"{ip_address} belongs to {ip_address_range_dict[ip_range]}")
                return (ip_range, org)
        except ValueError:
            # This will happen if the ip_range is not a valid format. 
            logger.info(f"{ip_address} is not found in any identified organizations")
            continue

    return None

   
if __name__ == "__main__":

    info = get_wifi_info_macos()
    for key, value in info.items():
        print(f"{key}: {value}")

    print(to_cidr("128.2.0.0/16"))       # '128.2.0.0/16'
    print(to_cidr("128.2.0.0 - 128.2.255.255"))  # '128.2.0.0/16'
    print(to_cidr("192.168.0.0 - 192.168.1.255"))  # '192.168.0.0/23'

    ip_range_dict = {
    "192.168.0.0/24": "Organization A",
    "10.0.0.0/8": "Organization B",
    "172.16.0.0/12": "Organization C"
    }

    ip_address = "192.168.0.15"
    print(match_ip_to_org(ip_range_dict, ip_address))

    ip_address = "182.168.0.15"
    print(match_ip_to_org(ip_range_dict, ip_address))