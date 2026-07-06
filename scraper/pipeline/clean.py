import json
import pandas
from pathlib import Path

import pandas as pd

folder = Path(__file__).resolve().parent / "../scrapers/data/raw/adzuna"
latest = max(folder.glob("*.json"))

print(latest)

with open(latest) as f:
    data = json.load(f)
df = pd.json_normalize(data["results"])
data_set = pd.DataFrame(df)

print(data_set)