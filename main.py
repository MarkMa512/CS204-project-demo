from datetime import datetime
import logging
import argparse

from util.speed_test import ping_test, speed_test
from util.trace_route import trace_route, get_locations
from util.network import get_wifi_info_macos
from util.gpt_whois import identify_org_details, filter_private_ips, integrate_ip_info
from util.csv_helper import write_summary_stats_to, write_ip_info

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
    identified_hops, hop_count = trace_route(target_url)

    # filter out the private ip addresses 
    public_ip_address_list = filter_private_ips(identified_hops)

    ip_address_location_list = get_locations(public_ip_address_list) 
    logger.info("------------------------------------------------------------")
    
    logger.info("List of hops identified and their locations: ")
    for ip_address, location in ip_address_location_list:
        logger.info(f"{ip_address} : {location}")

    # Write summary stats into csv file
    write_summary_stats_to(f"{output_filename}summary.csv", download, upload, latency, hop_count)

    logger.info("------------------------------------------------------------")

    """
    Analyse IXPs between orgs (Deduce from `whois` query)
    """
    # Find out the organization which the ip address belongs to. 
    logger.info("List of hops identified and their organization with whois and GPT: ")

    org_detail_list = identify_org_details(public_ip_address_list)

    logger.info(f"Recording the organizations found to a {output_filename}")

    data: list[list[str]] = integrate_ip_info(ip_address_location_list, org_detail_list)
    
    write_ip_info(f"{output_filename}summary.csv", data)
    
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