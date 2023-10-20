import json
import ipaddress
import subprocess

def extract_ipv4_name_dict_from(jsonl_file_name:str) -> dict:
    result_dict = {}
    
    with open(jsonl_file_name, 'r') as file:
        next(file)  # Skip the first line
        for line in file:
            data = json.loads(line)
            name = data.get("name", None)
            ipv4_list = data.get("prefixes", {}).get("ipv4", [])
            
            for ipv4 in ipv4_list:
                result_dict[ipv4] = name
    
    return result_dict



def longest_prefix_match(ip: str, prefix_dict:dict) -> dict:
    target_ip = ipaddress.ip_address(ip)
    
    # Sort the prefixes by length in descending order for longest match
    sorted_prefixes = sorted(prefix_dict.keys(), key=lambda x: x.split('/')[1], reverse=True)
    
    for prefix in sorted_prefixes:
        network = ipaddress.ip_network(prefix, strict=False)
        if target_ip in network:
            return {
                "Input IP": ip, 
                "Matched IPv4": prefix,
                "Name": prefix_dict[prefix]
            }
        else:
            return {
                "Input IP": ip, 
                "Matched IPv4": "NIL",
                "Name": "NIL"
            }


def get_organization(ip:str)->str:
    try:
        # Run the whois command and get the output
        result = subprocess.run(['whois', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result_str = result.stdout.decode('utf-8')

        # Split the result into lines and look for 'organisation:'
        for line in result_str.split('\n'):
            if 'organisation:' in line:
                return line.split('organisation:')[1].strip()
        return "Organisation not found"

    except Exception as e:
        return str(e)