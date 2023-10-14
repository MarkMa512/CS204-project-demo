import re
import requests
import subprocess

def trace_route(target_url:str) -> list:
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

    hops = []
    # Pattern to match IP addresses
    ip_pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')  
    

    while True:
        output_line = process.stdout.readline()
        if output_line == '' and process.poll() is not None:
            break
        if output_line:
            print(output_line.strip())
            match = ip_pattern.search(output_line)  # Search for IP in the line
            if match:  # If found
                hops.append(match.group())  # Add the matched IP
    
    hops = hops[1:] # omit the first ip address as it is the destination ip address 
    return hops

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

def get_locations(ip_addresses):
    return {ip: get_ip_location(ip) for ip in ip_addresses}