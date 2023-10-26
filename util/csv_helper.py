import csv

def write_to_csv(data: list[dict], filename:str)-> None:
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