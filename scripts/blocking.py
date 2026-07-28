import pandas as pd
from math import radians, sin, cos, sqrt, atan2
from rapidfuzz import fuzz

# Load hotel datasets
supplier_a = pd.read_csv("data/supplier_a.csv")
supplier_b = pd.read_csv("data/supplier_b.csv")


# Haversine distance (in kilometers)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


# Test only the first hotel from Supplier A
hotel_a = supplier_a.iloc[0]

print(f"\nHotel A: {hotel_a['name']}")
print("-" * 60)

count = 0

for _, hotel_b in supplier_b.iterrows():

    distance = haversine(
        hotel_a["lat"],
        hotel_a["lon"],
        hotel_b["lat"],
        hotel_b["lon"],
    )

    if distance <= 1:
        count +=1
    

        similarity = fuzz.token_sort_ratio(
            hotel_a["name"],
            hotel_b["name"]
        )
        
        distance_score = max(0, 100 - (distance * 100))
        confidence = (distance_score * 0.4) + (similarity * 0.6)

        print(
            f"{hotel_b['name']} | "
            f"Distance: {distance:.2f} km | "
            f"Name Similarity: {similarity:.1f}% |"
            f"Confidence: {confidence:.1f}"
        )

print(f"\nNearby Candidate Hotels: {count}")