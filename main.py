from datetime import datetime
import logging
import argparse

from util.speed_test import ping_test, speed_test
from util.trace_route import trace_route, get_locations
from util.network import get_wifi_info_macos
from util.gpt_whois import identify_IXP, filter_private_ips
from util.csv_helper import write_summary_stats_to, write_ip_location_to, write_whois_data_to

# Create a logger 
logger = logging.getLogger()
# Set Logging level 
logger.setLevel(logging.INFO)

# Get the current date and time and format it as desired for the log filename
time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"{time_stamp}.log"
output_filename = f"{time_stamp}_"

# Create a file handler for writing the logs to a file
file_handler = logging.FileHandler(log_filename)
file_handler.setFormatter(logging.Formatter("%(asctime)s: %(funcName)s(): %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))

# Create a stream handler for writing the logs to the console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("%(asctime)s: %(funcName)s(): %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def main(target_url:str, speed_test_flag:bool, ping_test_flag:bool) -> None:
    target_url = target_url or "cmu.edu"
    # Get the WiFi information
    logger.info("------------------------------------------------------------")
    logger.info(f"Getting WiFi Information: ")
    network_info = get_wifi_info_macos()
    for key, value in network_info.items():
        logger.info(f"{key}: {value}")
    logger.info("------------------------------------------------------------")

    # Speed Test
    download, upload = ("NA", "NA")
    if speed_test_flag: 
        logger.info(f"Testing network speed for: {network_info['SSID']}")
        download, upload = speed_test()
        logger.info(f"Download Speed: {download:.2f} Mbps")
        logger.info(f"Upload Speed: {upload:.2f} Mbps")
        logger.info("------------------------------------------------------------")


    logger.info(f"Target URL: {target_url}")
    logger.info("------------------------------------------------------------")
    
    
    # Ping Test
    latency = "NA"
    if ping_test_flag: 
        logger.info(f"Ping Test to {target_url}")
        latency = ping_test(target_url)
        if latency:
            logger.info(f"Average latency to {target_url} is: {latency} ms")
        logger.info("------------------------------------------------------------")

    # Trace Route
    logger.info(f"Trace Route to {target_url}")
    traceroute_hops, hop_count = trace_route(target_url)

    ip_address_location_dict = get_locations(traceroute_hops) 
    logger.info("------------------------------------------------------------")
    
    logger.info("List of hops identified and their locations: ")
    for ip_address, location in ip_address_location_dict.items():
        logger.info(f"{ip_address} : {location}")

    # Write into csv file
    write_summary_stats_to(download, upload, latency, hop_count, f"{output_filename}stats.csv")
    write_ip_location_to(ip_address_location_dict, ("IP Address", "Location"), f"{output_filename}ip_location.csv")

    logger.info("------------------------------------------------------------")

    """
    Analyse IXPs (Exact IP Matching)
    """
    # from caida.ip_map_ixp import parseJSONL, printIXs
    # with open("ixs_202307.jsonl") as ixp_jsonl: 
    # print("List of IXP found: ")
    # ixs = parseJSONL("ixs_202307.jsonl")
    # printIXs(traceroute_hops, ixs)


    """
    Analyse IXPs (Longest Prefix Matching)
    """
    # from caida.map_ixp import extract_ipv4_name_dict_from, longest_prefix_match
    # prefix_dict = extract_ipv4_name_dict_from("ixs_202307.jsonl")

    # for ip_address in traceroute_hops:
    #     print(longest_prefix_match(ip_address, prefix_dict))

    """
    Analyse IXPs (Deduce from `whois` query)
    """
    # filter out the private ip addresses 
    public_ip_address_list = filter_private_ips(traceroute_hops)


    # Find out the organization which the ip address belongs to. 
    logger.info("List of hops identified and their organization with whois and GPT: ")

    ixp_list = identify_IXP(public_ip_address_list)

    logger.info(f"Recording the IXP found to a {output_filename}")
    write_whois_data_to(ixp_list, f"{output_filename}whois.csv")
    
    logger.info("------------------------------------------------------------")

if __name__ == "__main__":
    
    # Set up the argument flags 
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', dest='target_url', type=str, required=False, help="Target URL for investigation")
    parser.add_argument('-s', action='store_true', required=False, help="Perform Speed Test for current network")
    parser.add_argument('-p', action='store_true', required=False, help="Perform Ping Test to target URL")

    # Pass in the arguments 
    arguments = parser.parse_args()
    input_target_url = arguments.target_url
    speed_test_flag = arguments.s 
    ping_test_flag = arguments.p

    # Invoke main function 
    try: 
        main(input_target_url, speed_test_flag, ping_test_flag)
    # Graceful exit with keyboard interruption 
    except KeyboardInterrupt:
        logger.error("Keyboard Interrupted. Exiting the program. ")
        logger.info("============================================================")

        exit(0)