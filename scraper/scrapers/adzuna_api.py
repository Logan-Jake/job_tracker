import requests
import json
import os
from dotenv import load_dotenv

load_dotenv('.env')

base_url = 'https://api.adzuna.com/v1/api'
adzuna_api_id = os.getenv('adzuna_api_id')
adzuna_api_key = os.getenv('adzuna_api_key')
# example final call - https://api.adzuna.com/v1/api/jobs/gb/search/1?api_id={YOUR_api_id}&api_key={YOUR_api_key}

resp = requests.get(
    f"{base_url}/jobs/gb/history",
    params={"api_id": adzuna_api_id, "api_key": adzuna_api_key,
            "what": "accountant", "location0": "UK"},
    timeout=10,
)
data = resp.json()

# 1. Reach into the structure
months = data["month"]          # the inner dict: {"2025-12": 42000, ...}

# 2. Loop over it (.items() gives you key + value pairs)
for month, salary in months.items():
    print(f"{month}: £{salary:,.0f}")

# 3. Sort chronologically (dict order isn't guaranteed to be sorted)
for month in sorted(months):
    print(month, months[month])

# 4. Do something useful with the numbers
values = list(months.values())
print("Average:", sum(values) / len(values))
print("Highest:", max(values))
print("Lowest:", min(values))

# 5. Find the most recent month
latest = max(months)            # max of "2025-12" style strings works
print(f"Most recent ({latest}): £{months[latest]:,.0f}")