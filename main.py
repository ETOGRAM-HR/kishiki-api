@app.get("/meishiki")
def get_meishiki(birth_date: str):
    target = str(birth_date).replace("-", "/").strip()

    results = []

    for d in data:
        raw = str(d.get("生年月日", "")).strip()

        # 時刻削除
        raw = raw.split(" ")[0]

        # ★ここ追加
        raw = raw.replace("\\/", "/")

        # 区切り統一
        raw = raw.replace("-", "/")

        # ゼロ埋め揃え
        parts = raw.split("/")
        if len(parts) == 3:
            y = parts[0]
            m = parts[1].zfill(2)
            d_ = parts[2].zfill(2)
            raw = f"{y}/{m}/{d_}"

        if raw == target:
            results.append(d)

    if len(results) != 1:
        return {
            "error": "not found or duplicate",
            "searched": target,
            "count": len(results)
        }

    return results[0]
