from pathlib import Path
import pandas as pd
import json

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def clean_latest(raw_path):
    with open(raw_path) as f:
        data = json.load(f)

    df = pd.json_normalize(data["results"])
    df = df.drop_duplicates(subset='id')

    # print(df.columns.tolist())
    df = (df[['id', 'title', 'description', 'company.display_name', 'salary_min', 'salary_max', 'salary_is_predicted',
              'contract_type', 'contract_time', 'category.label', 'latitude', 'longitude',
              'location.display_name', 'location.area', 'redirect_url', 'adref', 'created']])

    df = df.rename(columns={
        'company.display_name': 'company_name',
        'category.label': 'category_label',
        'location.display_name': 'location_display',
        'location.area': 'location_area',
    })
    df = df.astype(object).where(df.notna(), None)  # without astype(object) pandas converts None back to NaN
    print(f"File Used For Clean: {raw_path}")
    print(f"Rows Cleaned: {len(df.index)}")
    return df


if __name__ == "__main__":
    clean_latest()
