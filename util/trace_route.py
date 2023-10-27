import re
import requests
import subprocess
import logging

logger:logging.Logger = logging.getLogger(__name__)

def trace_route(target_url:str) -> tuple[list[str], int]:
    """
    Perform a traceroute and obtain all the IP addresses 
    :param target_url:  
    :return: a list of IP address of the hops that 
    
    """
    cmd = ['traceroute',  target_url]
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )

    identified_hops = []
    
    hop_count = -3 # account for the first 3 lines 
    # Pattern to match IP addresses (with parenthesis to avoid duplication)
    ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')  
    

    while True:
        output_line = process.stdout.readline()
        if output_line == '' and process.poll() is not None:
            break
        if output_line:
            hop_count += 1 
            logger.info(output_line.strip())
            match = ip_pattern.search(output_line)  # Search for IP in the line
            if match:  # If found
                matched_ip_address = match.group()
                cleaned_ip_address = matched_ip_address.replace('(', '').replace(')', '')
                identified_hops.append(cleaned_ip_address)  # Add the matched IP
    
    identified_hops = identified_hops[1:] # omit the first ip address as it is the destination ip address 
    return (identified_hops, hop_count)

def get_ip_location(ip_address:str):
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        data = response.json()
        
        if 'error' in data:
            return data['error']['message']
        
        city = data.get('city', 'Private')
        region = data.get('region', 'Private')
        country = data.get('country', 'Private')
        location = f"{city}, {region}, {country}"
        return location
    except requests.RequestException as e:
        return str(e)

def get_locations(ip_addresses)->dict:
    return {ip: get_ip_location(ip) for ip in ip_addresses}