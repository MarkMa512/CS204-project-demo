import subprocess
import openai

openai.api_key = open("key", "r").read().strip('\n')


def whois_lookup(domain_or_ip):
    # Step 1: Run the whois command.
    try:
        result = subprocess.check_output(['whois', domain_or_ip], stderr=subprocess.STDOUT).decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error executing whois on {domain_or_ip}.")
        return {}
    
    # print(result)
    
    response = openai.ChatCompletion.create(
        model = "gpt-4",
        messages =[
            {
                "role":"user", 
                "content": f"From the whois details in {result} for ip address {domain_or_ip}, identify the Regional Registry, Organization, Network Range,and Address for {domain_or_ip}. Present the solution in following format:\nRegional Registry:Regional_Registry_Identified\nOrganization:`Organization_identified`\nNetwork Range:`Network_Range_Identified`\nAddress:`Address_Identified",
            }
        ],
        max_tokens=100
        )

    summary =response['choices'][0]['message']['content']

    print(summary)


    # # Step 3: Extract necessary information from the summary.
    org = None
    net_range = None
    regional_registry = None
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
    result = whois_lookup(domain)
    print(result)
