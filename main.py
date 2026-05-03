from fastapi import FastAPI
import json

app = FastAPI()

with open("lookup_data_1.json", encoding="utf-8") as f:
    data1 = json.load(f)

with open("lookup_data_2.json", encoding="utf-8") as f:
    data2 = json.load(f)

data = data1 + data2

def normalize_date(value):
    value = str(value).strip()
    value = value.replace("-", "/")
    parts = value.split("/")

    if len(parts) != 3:
        return value

    year = parts[0]
    month = parts[1].zfill(2)
    day = parts[2].zfill(2)

    return f"{year}/{month}/{day}"

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/meishiki")
def get_meishiki(birth_date: str):
    target = normalize_date(birth_date)

    results = []
    for d in data:
        row_date = normalize_date(d.get("生年月日", ""))
        if row_date == target:
            results.append(d)

    if len(results) != 1:
        return {
            "error": "not found or duplicate",
            "searched": target,
            "count": len(results)
        }

    return results[0]
