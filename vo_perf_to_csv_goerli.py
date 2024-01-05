import csv
import requests
from datetime import datetime


def fetch_and_filter_data(url, ids):
    data = requests.get(url).json()
    performance_data = {}

    for operator in data["operators"]:
        if operator["id"] in ids:
            performance_data[operator["id"]] = operator["performance"]["24h"]

    return performance_data


# Read the existing CSV file and store the data
existing_data = []
operator_ids = set()
with open("operators_goerli.csv", "r", newline="") as csvfile:
    csvreader = csv.reader(csvfile)
    existing_data = [row for row in csvreader]
    # Extract operator IDs from the first column, skipping the header
    for row in existing_data[1:]:
        operator_ids.add(int(row[0]))

# Fetch and filter the data
url = "https://api.ssv.network/api/v4/goerli/operators/?page=1&perPage=1000&validatorsCount=true"
new_performance_data = fetch_and_filter_data(url, operator_ids)

# Append the new performance data to the existing data
today = datetime.now().strftime("%Y-%m-%d")
header = existing_data[0]
header.append("Performance (24h) as of " + today)

for row in existing_data[1:]:
    operator_id = int(row[0])
    performance = new_performance_data.get(operator_id, "N/A")
    row.append(performance)

# Write the updated data back to the CSV file
with open("operators_goerli.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(existing_data)

print("Data updated in operators_goerli.csv")
