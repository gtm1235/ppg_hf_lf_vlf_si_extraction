import os

def get_csv_files():
    """Get list of directories with ppg csv files"""
    # Get the current working directory
    current_dir = os.getcwd()

    # Create an empty list to store the CSV file paths
    csv_files = []

    # Loop through all the items in the current directory
    for item in os.listdir(current_dir):
        # Check if the item is a directory and contains the string "csv"
        if os.path.isdir(item) and "csv" in item.lower():
            # If it does, loop through all the files in the directory
            for filename in os.listdir(item):
                # Check if the file ends with ".csv"
                if filename.endswith(".csv"):
                    # If it does, append the relative location and filename to the csv_files list
                    csv_files.append(os.path.join(item, filename))

    # Print out the list of CSV file paths
    #print(csv_files)
    return csv_files