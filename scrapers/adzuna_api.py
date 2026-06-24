import requests
import json
import .env

base_url = 'https://api.adzuna.com/v1/api'

# example final call - https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={YOUR_APP_ID}&app_key={YOUR_APP_KEY}

resp = requests.get(f"{base_url}")