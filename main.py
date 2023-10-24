from datetime import datetime
import logging


from util.speed_test import ping_test, speed_test
from util.trace_route import trace_route, get_locations
from util.network import get_wifi_info_macos
from caida.map_ixp import extract_ipv4_name_dict_from, longest_prefix_match, get_organization

# Create a logger 
logger = logging.getLogger()
# Set Logging level 
logger.setLevel(logging.INFO)

# Get the current date and time and format it as desired for the log filename
log_filename = datetime.now().strftime("%Y-%m-%d %H:%M:%S_trace.log")

# Create a file handler for writing the logs to a file
file_handler = logging.FileHandler(log_filename)
file_handler.setFormatter(logging.Formatter("%(asctime)s: %(funcName)s(): %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))

# Create a stream handler for writing the logs to the console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("%(asctime)s: %(funcName)s(): %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def main() -> None:
    # Get the WiFi information
    logger.info("------------------------------------------------------------")
    logger.info(f"Getting WiFi Information: ")
    network_info = get_wifi_info_macos()
    for key, value in network_info.items():
        # print(f"{key}: {value}")
        logger.info(f"{key}: {value}")
    logger.info("------------------------------------------------------------")

    # Speed Test
    logger.info(f"Testing network speed for: {network_info['SSID']}")
    download, upload = speed_test()
    logger.info(f"Download Speed: {download:.2f} Mbps")
    logger.info(f"Upload Speed: {upload:.2f} Mbps")
    logger.info("------------------------------------------------------------")

    
    TARGET_URL = "cmu.edu"
    logger.info(f"Target URL: {TARGET_URL}")
    logger.info("------------------------------------------------------------")
    
    
    # Ping Test
    logger.info(f"Ping Test to {TARGET_URL}")
    latency = ping_test(TARGET_URL)
    if latency:
        logger.info(f"Average latency to {TARGET_URL} is: {latency} ms")
    logger.info("------------------------------------------------------------")

    # Trace Route
    logger.info(f"Trace Route to {TARGET_URL}")
    traceroute_hops = trace_route(TARGET_URL)

    ip_address_location_dict = get_locations(traceroute_hops) 
    logger.info("------------------------------------------------------------")
    
    logger.info("List of hops identified and their locations: ")
    for ip_address, location in ip_address_location_dict.items():
        logger.info(f"{ip_address} : {location}")
    logger.info("------------------------------------------------------------")
    # Analyse IXPs (Exact IP Matching)
    # with open("ixs_202307.jsonl") as ixp_jsonl: 
    # print("List of IXP found: ")
    # ixs = parseJSONL("ixs_202307.jsonl")
    # printIXs(traceroute_hops, ixs)

    # Analyse IXPs (Longest Prefix Matching)
    # prefix_dict = extract_ipv4_name_dict_from("ixs_202307.jsonl")

    # for ip_address in traceroute_hops:
    #     print(longest_prefix_match(ip_address, prefix_dict))


    # Find out the organization which the ip address belongs to. 
    logger.info("List of hops identified and their organization: ")
    for ip_address in traceroute_hops: 
        logger.info(f"IP Address: {ip_address} : Organization: {get_organization(ip_address)}")
    logger.info("------------------------------------------------------------")

if __name__ == "__main__":
    try: 
        main()
    # Graceful exit with keyboard interruption 
    except KeyboardInterrupt:
        logger.error("Keyboard Interrupted. Exiting the program. ")
        logger.info("============================================================")

        exit(0)