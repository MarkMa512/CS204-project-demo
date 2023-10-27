import csv

def write_whois_data_to(data: list[dict], filename:str)-> None:
    """
    Write a list of dictionaries to a CSV file.

    :param data: List of dictionaries containing data.
    :param filename: Name of the output CSV file.
    """
    
    # Get the keys (headings) from the first dictionary in the list
    # all dictionaries in the list have the same keys
    headings = data[0].keys()

    # Write data to CSV
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headings)
        writer.writeheader()  # writes the headings
        for row in data:
            writer.writerow(row)


def write_ip_location_to(data:dict[str, str], header: tuple[str, str], filename:str)->None: 
    """
    Write a dictionary to a CSV file with header specified in header tuple(header_for_key, header_for_value)

    :param data: dictionaries containing data.
    :param header: header of csv file
    :param filename: Name of the output CSV file.
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write the header to the CSV file
        writer.writerow(header)
        
        # Write each key-value pair to the CSV file
        for key, value in data.items():
            writer.writerow([key, value])


def write_summary_stats_to(download:str, upload:str, latency:str, hop_count:int, filename:str)->None: 
    """
    Write download speed, upload speed, and ping latency in to a CSV file with following format 

    Download Speed,`download`,Mbps
    Upload Speed,`upload`,Mbps
    Average Latency,`ping`,ms
    """
    rows = [
        ("Download Speed", download, "Mbps"),
        ("Upload Speed", upload, "Mbps"),
        ("Average Latency", latency, "ms"), 
        ("number of Hops", hop_count, "hops")
    ]
    
    # Write to CSV
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)