import subprocess
import re


def whois_lookup(domain_or_ip):
    try:
        # Execute the whois command and decode the result
        result = subprocess.check_output(['whois', domain_or_ip], stderr=subprocess.STDOUT).decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error executing whois on {domain_or_ip}.")
        return {}

    # Use regular expressions to extract the desired details
    org_patterns = [r'descr:\s+(.+)', r'Organization:\s+(.+)', r'OrgName:\s+(.+)']
    org = None
    for pattern in org_patterns:
        match = re.search(pattern, result)
        if match:
            org = match.group(1)
            break

    net_range_patterns = [r'inetnum:\s+(.+)', r'NetRange:\s+(.+)']
    net_range = None
    for pattern in net_range_patterns:
        match = re.search(pattern, result)
        if match:
            net_range = match.group(1)
            break

    # Construct the result dictionary
    return {
        'Organization': org,
        'Network Range': net_range
    }
if __name__ == "__main__":
    ip_address_list = ["62.115.45.169", "38.140.44.154", "154.54.58.5", "30.117.14.181"] 

    for ip_address in ip_address_list:
        print(whois_lookup(ip_address))