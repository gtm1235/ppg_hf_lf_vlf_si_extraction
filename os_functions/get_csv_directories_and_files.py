import os


def get_csv_files():
    """Get list of directories with ppg csv files"""

    current_dir = os.getcwd()

    csv_files = []

    for item in os.listdir(current_dir):
        if os.path.isdir(item) and "csv" in item.lower():
            for filename in os.listdir(item):
                if filename.endswith(".csv"):
                    csv_files.append(os.path.join(item, filename))

    return csv_files
