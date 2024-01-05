import csv
import json
import requests
from datetime import date
from prettytable import PrettyTable

ids = [i for i in range(1, 61)]


def fetch_and_filter_data(url):
    data = requests.get(url).json()

    # Filter based on hardcoded IDs and extract desired information
    filtered_data = []
    for operator in data["operators"]:
        if operator["id"] in ids:
            filtered_data.append(
                {
                    "Operator ID": operator["id"],
                    "Operator Name": operator["name"],
                    "Performance (24h)": operator["performance"]["24h"],
                    "Validator Count": operator["validators_count"],
                    "Status": "OK"
                    if operator["validators_count"] >= 10
                    and operator["performance"]["24h"] >= 99.0
                    else "Not OK",
                }
            )

    filtered_data.sort(key=lambda row: row["Status"])
    return filtered_data


rows = fetch_and_filter_data(
    "https://api.ssv.network/api/v4/mainnet/operators/?page=1&perPage=1000&validatorsCount=true"
)

# Get the current date
today = date.today().strftime("%m/%d/%Y")

# Read the CSV file to get all operator IDs
with open("operators.csv", "r") as f:
    reader = csv.reader(f)
    ids = next(reader)

# Create a new column with the operator performance
for row in rows:
    row["Performance (24h)"] = row["performance"]["24h"]
del row["performance"]

# Write the data to a new CSV file
with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Date"] + ids)
    writer.writerow([today] + [row["Performance (24h)"] for row in rows])
