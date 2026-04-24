import re
import json

with open("raw.txt", encoding="utf-8") as f:
   text = f.read()

is_duplicate = "ДУБЛИКАТ" in text

products = re.findall(r"\d+\.\n(.+?)\n\d", text, re.DOTALL)

prices_raw = re.findall(r"Стоимость\n([\d\s,]+)\n", text)

prices = [float(p.replace(" ", "").replace(",", ".")) for p in prices_raw]

total_match = re.search(r"ИТОГО:\n([\d\s,]+)", text)
total = None
if total_match:
   total = float(total_match.group(1).replace(" ", "").replace(",", "."))

datetime_match = re.search(r"Время:\s(.+)", text)
datetime_value = datetime_match.group(1) if datetime_match else None

payment_match = re.search(r"(Банковская карта|Наличные)", text)
payment_method = payment_match.group(1) if payment_match else None

data = {
   "is_duplicate": is_duplicate,
   "products": products,
   "prices": prices,
   "total": total,
   "datetime": datetime_value,
   "payment_method": payment_method
}

print(json.dumps(data, ensure_ascii=False, indent=4))