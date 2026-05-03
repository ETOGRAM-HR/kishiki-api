from fastapi import FastAPI
import json

app = FastAPI()

# 1つ目のJSON
with open("lookup_data_1.json", encoding="utf-8") as f:
    data1 = json.load(f)

# 2つ目のJSON
with open("lookup_data_2.json", encoding="utf-8") as f:
    data2 = json.load(f)

# 結合（ここが重要）
data = data1 + data2

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/meishiki")
def get_meishiki(birth_date: str):
    results = [d for d in data if d["生年月日"] == birth_date]

    if len(results) != 1:
        return {"error": "not found or duplicate"}

    return results[0]