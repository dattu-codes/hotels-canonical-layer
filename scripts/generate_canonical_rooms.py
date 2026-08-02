import json

from app.pipeline.ingestion import DataLoader
from app.pipeline.room_matcher import RoomMatcher
from app.pipeline.room_canonicalizer import RoomCanonicalizer


def main():

    loader = DataLoader()

    rooms_a, rooms_b = loader.load_rooms()

    with open(
        "output/canonical_hotels.json",
        "r",
        encoding="utf-8"
    ) as f:
        canonical_hotels = json.load(f)

    normalizer = RoomMatcher()

    canonicalizer = RoomCanonicalizer(
        normalizer
    )

    all_rooms = []

    matched_hotels = [
        hotel
        for hotel in canonical_hotels
        if hotel["supplier_a_id"] is not None
        and hotel["supplier_b_id"] is not None
    ]

    for hotel in matched_hotels:

        hotel_rooms_a = rooms_a[
            rooms_a["hotel_id"] == hotel["supplier_a_id"]
        ]

        hotel_rooms_b = rooms_b[
            rooms_b["hotel_id"] == hotel["supplier_b_id"]
        ]

        records = canonicalizer.canonicalize_hotel_rooms(
            hotel["canonical_id"],
            hotel_rooms_a,
            hotel_rooms_b
        )

        all_rooms.extend(records)

    with open(
        "output/canonical_rooms.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            all_rooms,
            f,
            indent=2,
            default=str
        )

    print(
        f"Generated {len(all_rooms)} canonical rooms."
    )


if __name__ == "__main__":
    main()