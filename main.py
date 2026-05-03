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
    value = value.replace("\\/", "/")
    value = value.replace("￥", "")
    value = value.replace("\\", "")
    value = value.replace("-", "/")
    value = value.split(" ")[0]

    parts = value.split("/")
    if len(parts) == 3:
        return f"{parts[0]}/{parts[1].zfill(2)}/{parts[2].zfill(2)}"
    return value

@app.get("/")
def root():
    return {"message": "API is running", "version": "debug-20260504"}

@app.get("/meishiki")
def get_meishiki(birth_date: str):
    target = normalize_date(birth_date)

    results = []
    for row in data:
        raw = row.get("生年月日", "") or row.get("西暦", "")
        row_date = normalize_date(raw)

        if row_date == target:
            results.append(row)

    if len(results) != 1:
        return {
            "error": "not found or duplicate",
            "searched": target,
            "count": len(results),
            "sample_keys": list(data[0].keys())[:5],
            "sample_date_1": data[0].get("生年月日", "") or data[0].get("西暦", ""),
            "sample_date_2": data1[-1].get("生年月日", "") or data1[-1].get("西暦", ""),
            "sample_date_3": data2[0].get("生年月日", "") or data2[0].get("西暦", "")
        }

    return results[0]
