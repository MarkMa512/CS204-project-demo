import re
import requests
import subprocess
import logging

logger:logging.Logger = logging.getLogger(__name__)

def trace_route(target_url:str) -> tuple[list[str],int]:
    """
    Perform a traceroute and obtain all the IP addresses 
    :param target_url:  
    :return: (identified_hops, hop_count)
        identified_hops: a list of IP address of the hops that have been identified 
        hop_count: the number of hops went through
    
    """
    cmd = ['traceroute',  target_url]
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )

    identified_hops = []
    hop_count = 0 
    trace_route_output = []

    # Pattern to match IP addresses (with parenthesis to avoid duplication)
    ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')  
    # Pattern to match hop number at the start of the line
    hop_number_pattern = re.compile(r'^\s*(\d+)\s')

    while True:
        output_line = process.stdout.readline()
        if output_line == '' and process.poll() is not None:
            break
        if output_line:
            logger.info(output_line.strip())
            trace_route_output.append(output_line.strip())
             # Extract hop number
            hop_match = hop_number_pattern.match(output_line)
            if hop_match:
                hop_count = max(hop_count, int(hop_match.group(1)))
            
            # Extract IP address
            match = ip_pattern.search(output_line)  # Search for IP in the line
            if match:  # If found
                matched_ip_address = match.group(1) # This should remove the parenthesis 
                if matched_ip_address not in identified_hops:
                    identified_hops.append(matched_ip_address)  # Add the matched IP if it's not already in the list
    
    identified_hops = identified_hops[1:] # omit the first ip address as it is the destination ip address 
    return (identified_hops, hop_count)

def get_ip_info(ip_address:str):
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        data = response.json()
        
        if 'error' in data:
            return data['error']['message']
        
        city = data.get('city', 'Private')
        region = data.get('region', 'Private')
        country = data.get('country', 'Private')
        org = data.get('org', 'Private')
        location = f"{org}, {city}, {region}, {country}"
        return location
    except requests.RequestException as e:
        return str(e)

def get_locations(ip_addresses_list: list[str]) -> list[list[str]]:
    return [[ip, get_ip_info(ip)] for ip in ip_addresses_list]