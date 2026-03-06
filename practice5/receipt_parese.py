import re
import json


def parse_receipt(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()


    datetime_match = re.search(
        r'Время:\s+(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})',
        data
    )

    date = datetime_match.group(1) if datetime_match else "Unknown"
    time = datetime_match.group(2) if datetime_match else "Unknown"


    item_pattern = re.findall(
        r'\d+\.\s*\n'               
        r'(.+?)\n'                       
        r'(\d+,\d+)\s*x\s*'              
        r'([\d\s]+,\d{2})\n'               
        r'([\d\s]+,\d{2})',                
        data
    )

    items = []

    for match in item_pattern:
        name = match[0].strip()
        quantity = float(match[1].replace(",", "."))
        unit_price = float(match[2].replace(" ", "").replace(",", "."))
        total_price = float(match[3].replace(" ", "").replace(",", "."))

        items.append({
            "product": name,
            "quantity": quantity,
            "unit_price": unit_price,
            "total_price": total_price
        })


    total_match = re.search(
        r'ИТОГО:\s*\n([\d\s]+,\d{2})',
        data
    )

    grand_total = (
        float(total_match.group(1).replace(" ", "").replace(",", "."))
        if total_match else 0.0
    )


    if re.search(r'Банковская карта:', data):
        payment_method = "Card"
    else:
        payment_method = "Unknown"


    receipt_json = {
        "store": "EUROPHARMA",
        "date": date,
        "time": time,
        "items": items,
        "summary": {
            "total_items": len(items),
            "grand_total": grand_total,
            "payment_method": payment_method
        }
    }

    return receipt_json

if __name__ == "__main__":
    result = parse_receipt("raw.txt")
    print(json.dumps(result, indent=4, ensure_ascii=False))