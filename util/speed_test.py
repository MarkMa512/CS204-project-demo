import subprocess
import speedtest

import logging

logger:logging.Logger = logging.getLogger(__name__)

def ping_test(target_url:str, count:int=4):
    """
    Get the latency to the target URL 
    """
    try:
        response = subprocess.check_output(
            ['ping', '-c', str(count), target_url],
            stderr=subprocess.STDOUT,  # Redirect error output to standard output
            universal_newlines=True  # Needed for the output to be a string
        )
        
        # Extract the average latency from the ping output
        avg_latency = response.split('/')[-3]
        return avg_latency
    
    except subprocess.CalledProcessError:
        logger.error(f"Ping to {target_url} failed!")
        return None

def speed_test():
    """
    Test the download/upload speed of current network
    """
    st = speedtest.Speedtest()
    st.get_best_server()  # Selects the best server for testing
    
    download_speed = st.download() / (10**6)  # Convert bits per second to megabits per second
    upload_speed = st.upload() / (10**6)
    
    return download_speed, upload_speed