import json
from collections import Counter

with open("output/canonical_hotels.json", "r", encoding="utf-8") as f:
    hotels = json.load(f)

b_ids = [hotel["supplier_b_id"] for hotel in hotels]

counter = Counter(b_ids)

print("Total hotels:", len(hotels))
print("Unique Supplier B IDs:", len(counter))

duplicates = [(k, v) for k, v in counter.items() if v > 1]

print("Duplicate Supplier B IDs:", len(duplicates))

if duplicates:
    print("\nFirst 10 duplicates:")
    for k, v in duplicates[:10]:
        print(k, v)