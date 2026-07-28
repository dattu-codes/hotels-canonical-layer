from app.pipeline.merger import CanonicalMerger
from app.pipeline.ingestion import DataLoader
from app.pipeline.blocking import CandidateGenerator
from app.pipeline.hotel_matcher import HotelMatcher


loader = DataLoader()

supplier_a, supplier_b = loader.load_hotels()

generator = CandidateGenerator(radius_km=1)

matcher = HotelMatcher()
merger = CanonicalMerger()


canonical_hotels = []

for _, hotel_a in supplier_a.iterrows():

    print(f"Processing: {hotel_a['name']}")
    print(f"\nTesting Hotel: {hotel_a['name']}")
    print("=" * 80)

    candidates = generator.get_candidates(hotel_a, supplier_b)

    best_candidate = None
    best_result = None
    highest_confidence = -1

    for candidate in candidates:

        hotel_b = candidate["hotel"]
        distance = candidate["distance"]

        result = matcher.calculate_confidence(
            hotel_a,
            hotel_b,
            distance
        )

        if result["confidence"] > highest_confidence:
            highest_confidence = result["confidence"]
            best_candidate = candidate
            best_result = result

    if best_candidate is None:
        continue

    canonical = merger.merge(
        hotel_a,
        best_candidate["hotel"],
        best_result["confidence"]
    )

    
    canonical_hotels.append(canonical)
    
print("\nProcessing Complete!")
print(f"Total Canonical Hotels: {len(canonical_hotels)}")

import json

with open("output/canonical_hotels.json", "w", encoding="utf-8") as f:
    json.dump(canonical_hotels, f, indent=4, default=str)

print("Saved to output/canonical_hotels.json")