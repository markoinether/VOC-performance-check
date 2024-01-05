import json
import requests
from prettytable import PrettyTable

ids = [i for i in range(1, 61)]

def fetch_and_filter_data(url):
    data = requests.get(url).json()

    # Filter based on hardcoded IDs and extract desired information
    filtered_data = []
    for operator in data['operators']:
        if operator['id'] in ids:
            filtered_data.append({
                'Operator ID': operator['id'],
                'Operator Name': operator['name'],
                'Performance (24h)': operator['performance']['24h'],
                'Validator Count': operator['validators_count'],
                'Status': "OK" if operator['validators_count'] >= 10 and operator['performance']['24h'] >= 99.0 else "Not OK"
            })

    filtered_data.sort(key=lambda row: row["Status"])
    return filtered_data

rows = fetch_and_filter_data('https://api.ssv.network/api/v4/mainnet/operators/?page=1&perPage=1000&validatorsCount=true')

# Convert the sorted list of rows to a PrettyTable
table = PrettyTable()
table.field_names = ["Operator ID", "Operator Name", "Validator Count", "Performance (24h)", "Status"]
for row in rows:
    table.add_row([row["Operator ID"], row["Operator Name"], row["Validator Count"], row["Performance (24h)"], row["Status"]])

# Print the table
print(table)
