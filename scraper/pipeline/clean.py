from pathlib import Path
import pandas as pd
import json

folder = Path(__file__).resolve().parent / "../scrapers/data/raw/adzuna"
latest = max(folder.glob("*.json"))

with open(latest) as f:
    data = json.load(f)

df = pd.json_normalize(data["results"])
pd.set_option('display.max_columns', None)


print(df.columns.tolist())
print(df)
