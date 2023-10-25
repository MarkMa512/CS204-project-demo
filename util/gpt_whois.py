import subprocess
import openai
import logging

# Obtain API key from `key` file stored in the project root directory
openai.api_key = open("key", "r").read().strip('\n')

logger:logging.Logger = logging.getLogger(__name__)

def gpt_whois(ip_address:str)->dict:

    logger.info(f"Query for IP Address: {ip_address} ...")
    
    # Step 1: Run the whois command.
    try:
        result = subprocess.check_output(['whois', ip_address], stderr=subprocess.STDOUT).decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error executing whois on {ip_address}.")
        return {}
    
    # print(result)
    # Step 2: Pass the result of whois to ChatGPT to identify the Regional Registry, Organization, Network Range,and Address
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages =[
            {
                "role":"user", 
                "content": f"From the whois details in {result} for ip address {ip_address}, identify the Regional Registry, Network Range, Organization,and Address for {ip_address}. Present the solution in following format:\nRegional Registry:Regional_Registry_Identified\nOrganization:`Organization_identified`\nNetwork Range:`Network_Range_Identified`\nAddress:`Address_Identified",
            }
        ],
        max_tokens=100
        )

    summary =response['choices'][0]['message']['content']

    # print(summary)


    # # Step 3: Extract necessary information from the summary. 
    regional_registry = None
    net_range = None
    org = None
    address = None
    
    for line in summary.split('\n'):
        if 'Organization' in line:
            org = line.split(':')[-1].strip()
        elif 'Network Range' in line:
            net_range = line.split(':')[-1].strip()
        elif 'Regional Registry' in line:
            regional_registry = line.split(':')[-1].strip()
        elif 'Address' in line:
            address = line.split(':')[-1].strip()

    return {
        'Regional Registry': regional_registry,
        'Network Range': net_range,
        'Organization': org,
        'Address': address
    }

# Test
if __name__ == "__main__":
    domain = '62.115.45.169'
    result = gpt_whois(domain)
    print(result)
