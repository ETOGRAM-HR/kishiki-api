from fastapi import FastAPI
import json
from datetime import datetime

app = FastAPI()

with open("lookup_data_1.json", encoding="utf-8") as f:
    data1 = json.load(f)

with open("lookup_data_2.json", encoding="utf-8") as f:
    data2 = json.load(f)

data = data1 + data2

def normalize_date(value: str) -> str:
    value = value.replace("-", "/")
    dt = datetime.strptime(value, "%Y/%m/%d")
    return f"{dt.year}/{dt.month:02d}/{dt.day:02d}"

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/meishiki")
def get_meishiki(birth_date: str):
    try:
        target = normalize_date(birth_date)
    except Exception:
        return {"error": "invalid date format"}

    results = []

    for d in data:
        if "生年月日" not in d:
            continue

        try:
            row_date = normalize_date(d["生年月日"])
        except Exception:
            continue

        if row_date == target:
            results.append(d)

    if len(results) != 1:
        return {"error": "not found or duplicate"}

    return results[0]
