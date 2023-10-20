import logging


from util.speed_test import ping_test, speed_test
from util.trace_route import trace_route, get_locations
from util.network import get_wifi_info_macos
# from caida.ip_map_ixp import parseJSONL, printIXs

from caida.map_ixp import extract_ipv4_name_dict_from, longest_prefix_match, get_organization

logging.basicConfig(format="%(asctime)s %(levelname)s %(filename)s:%(funcName)s():%(lineno)i: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)


logger:logging.Logger = logging.getLogger(__name__)
    
if __name__ == "__main__":

    # Get the WiFi information
    info = get_wifi_info_macos()
    for key, value in info.items():
        print(f"{key}: {value}")
    
    TARGET_URL = "cmu.edu"
    
    # Ping Test
    # latency = ping_test(TARGET_URL)
    # if latency:
    #     print(f"Average latency to {TARGET_URL} is: {latency} ms")

    # Speed Test
    # download, upload = speed_test()
    # print(f"Download Speed: {download:.2f} Mbps")
    # print(f"Upload Speed: {upload:.2f} Mbps")

    # Trace Route
    traceroute_hops = trace_route(TARGET_URL)

    ip_address_location_dict = get_locations(traceroute_hops) 

    print("List of hops identified and their locations: ")
    for ip_address, location in ip_address_location_dict.items():
        print(f"{ip_address} : {location}")
    
    # Analyse IXPs (Exact IP Matching)

    # with open("ixs_202307.jsonl") as ixp_jsonl: 
    # print("List of IXP found: ")
    # ixs = parseJSONL("ixs_202307.jsonl")
    # printIXs(traceroute_hops, ixs)

    # Analyse IXPs (Longest Prefix Matching)

    prefix_dict = extract_ipv4_name_dict_from("ixs_202307.jsonl")

    for ip_address in traceroute_hops:
        print(longest_prefix_match(ip_address, prefix_dict))


    # Find out the organization which the ip address belongs to. 
    for ip_address in traceroute_hops: 
        print(f"IP Address: {ip_address} : Organization: {get_organization(ip_address)}")
