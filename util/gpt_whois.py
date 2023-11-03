import subprocess
import openai
import logging
import ipaddress
import time

# Obtain API key from `key` file stored in the project root directory
openai.api_key = open("key", "r").read().strip('\n')

logger:logging.Logger = logging.getLogger(__name__)

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
    try: 
        start_ip, end_ip = [ip.strip() for ip in ip_address_range.split('-')]
    except ValueError:
        logger.error(f"Invalid IP address range has been provided. ")
        return "0.0.0.0/0"
    
    try:
        combined_ip_network = ipaddress.summarize_address_range(ipaddress.ip_address(start_ip), ipaddress.ip_address(end_ip))
        return ', '.join(str(net) for net in combined_ip_network)
    except ValueError:
        logger.error(f"Could not convert: {ip_address_range} to CIDR notation")
        pass

        
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

def identify_org_details(ip_address_list: list[str])-> list[dict[str:str]]:

    ip_address_range_dict = {} 
    org_detail_list = []
    org_peering_list = []

    for ip_address in ip_address_list: 
        logger.info(f"Querying for IP Address: {ip_address} ...")

        # 1. Check if this IP address has already been identified previously 
        result = match_ip_to_org(ip_address_range_dict, ip_address)

        if result != None: 
            # if found to be previous identified 
            logger.info(f"{ip_address} belong to a previously found organizations: {result}")
            org_peering_list.append(result)
            logger.info("..................................................")
        else:
            logger.info(f"{ip_address} does not belong to previously found organizations. Run whois command now ...")
            
            # Step 2: Run the whois command.
            try:
                result = subprocess.check_output(['whois', ip_address], stderr=subprocess.STDOUT).decode('utf-8')
            except subprocess.CalledProcessError as e:
                print(f"Error executing whois on {ip_address}.")
                return {}
            
            retry_count = 3
            wait_time = 3 
            response = None

            for attempt in range(retry_count): 
                try: 
                    # Step 2: Pass the result of whois to ChatGPT to identify the Regional Registry, Organization, Network Range,and Address
                    response = openai.ChatCompletion.create(
                        model = "gpt-3.5-turbo",
                        messages =[
                            {
                                "role":"user", 
                                "content": f"From the whois details in {result} for ip address {ip_address}, identify the Regional Registry, Network Range, Organization,and Address for {ip_address}. Present the solution in following format:\nRegional Registry:Regional_Registry_Identified\nOrganization:`Organization_identified`\nNetwork Range:`Network_Range_Identified`\nAddress:`Address_Identified",
                            }
                        ],
                        max_tokens=200
                        )
                    # if success, break 
                    break 
                except openai.error.OpenAIError as e: 
                    logger.error(f"Error on attempt {attempt + 1}: {e}")
                    # if this is the last attempt, raise exception 
                    if attempt == retry_count - 1:
                            raise
                    # If not the last attempt, wait for a bit before retrying
                    time.sleep(wait_time)

            summary =response['choices'][0]['message']['content']

            # # Step 3: Extract necessary information from the summary. 
            regional_registry = None
            network_range = None
            organization = None
            address = None
            
            for line in summary.split('\n'):
                if 'Organization' in line:
                    organization = line.split(':')[-1].strip()
                elif 'Network Range' in line:
                    network_range = line.split(':')[-1].strip()
                elif 'Regional Registry' in line:
                    regional_registry = line.split(':')[-1].strip()
                elif 'Address' in line:
                    address = line.split(':')[-1].strip()

            # convert the network range to CIDR format 
            network_range = to_cidr(network_range)
            # put the newly identified range and org pair into the dictionary 
            ip_address_range_dict[network_range] = organization

            org_detail_list.append(
                {
                    'Regional Registry': regional_registry,
                    'Network Range': network_range,
                    'Organization': organization,
                    'Address': address
                }
            )

            org_peering_list.append((network_range, organization))

            logger.info(f"Regional Registry: {regional_registry}")
            logger.info(f"Network Range: {network_range}")
            logger.info(f"Organization:{organization}")
            logger.info(f"Address:{address}")
            logger.info("++++++++++++++++++++++++++++++++++++++++++++++++++")
            
    return org_detail_list

def integrate_ip_info(ip_address_location: list[list[str]], org_detail_list: list[dict]) -> list[list[str]]:
    """
    Integrate IP information from the provided org_detail_list into the ip_address_location list based on the IP range.

    Args:
    - ip_address_location (list[list[str]]): List containing IP addresses and their locations.
    - org_detail_list (list[dict]): List of dictionaries containing IP-related information.

    Returns:
    - list[list[str]]: Updated ip_address_location list with integrated information.
    """
    
    for record in ip_address_location:
        ip_addr = ipaddress.ip_address(record[0])  # Convert string to IP address object
        
        # Check if the IP address is within any of the network ranges
        for info in org_detail_list:
            network = ipaddress.ip_network(info['Network Range'])
            if ip_addr in network:
                # Add the information from the dictionary to the record
                record.extend([
                    info['Regional Registry'],
                    info['Network Range'],
                    info['Organization'],
                    info['Address']
                ])
                break  # Exit the inner loop if a match is found

    return ip_address_location


# Test
if __name__ == "__main__":
    print(to_cidr("128.2.0.0/16"))       # '128.2.0.0/16'
    print(to_cidr("128.2.0.0 - 128.2.255.255"))  # '128.2.0.0/16'
    print(to_cidr("192.168.0.0 - 192.168.1.255"))  # '192.168.0.0/23'
    print(to_cidr(""))
    print(to_cidr("192.168.0.0"))


    ip_range_dict = {
    "192.168.0.0/24": "Organization A",
    "10.0.0.0/8": "Organization B",
    "172.16.0.0/12": "Organization C"
    }

    ip_address = "192.168.0.15"
    print(match_ip_to_org(ip_range_dict, ip_address))

    ip_address = "182.168.0.15"
    print(match_ip_to_org(ip_range_dict, ip_address))