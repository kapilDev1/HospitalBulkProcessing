import csv
from io import TextIOWrapper


REQUIRED_COLUMNS={'name','address'}
MAX_ROWS=20

def validate_and_parse_csv(file):
    try:
        wrapper = TextIOWrapper(file,encoding='utf-8')
        reader = csv.DictReader(wrapper)
    except Exception:
        raise ValueError('Invalid csv file')
    
    if not reader.fieldnames:
        raise ValueError('CSV file has no headers')

    missing = REQUIRED_COLUMNS - set(reader.fieldnames)

    if missing:
        raise ValueError(f"Missing columns :{', '.join(missing)}")
    
    rows = list(reader)

    if len(rows)> MAX_ROWS:
        raise ValueError("CSV exceeds maximum of 20 hospitals")
    
    parsed = []
    for idx,row in enumerate(rows,start=1):
        name = row.get("name","").strip()
        address = row.get("address","").strip()

        if not name or not address:
            raise ValueError(f"Row {idx}: name and address are required")

        parsed.append({
            "name":name,
            "address":address,
            "phone":row.get("phone","").strip() or None
        })
    
    return parsed