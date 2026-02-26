import re
import json

with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

prices = re.findall(r"\d[\d\s]*,\d{2}", text)

clean_prices = []
for price in prices:
    p = price.replace(" ", "").replace(",", ".")
    clean_prices.append(float(p))

date_match = re.search(r"\d{2}\.\d{2}\.\d{4}", text)
date = date_match.group() if date_match else "Not found"

time_match = re.search(r"\d{2}:\d{2}:\d{2}", text)
time = time_match.group() if time_match else "Not found"

payment_match = re.search(r"Банковская карта", text)
payment_method = "Bank card" if payment_match else "Not found"

products = re.findall(r"\d+\.\n(.+)", text)

total = sum(clean_prices)

receipt_data = {
    "date": date,
    "time": time,
    "payment_method": payment_method,
    "total_calculated": total,
    "products": products,
    "prices": clean_prices
}

print(json.dumps(receipt_data, indent=4, ensure_ascii=False))