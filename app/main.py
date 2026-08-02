from fastapi import FastAPI, HTTPException
from typing import Optional
import json
import pandas as pd

app = FastAPI(
    title="Hotels Canonical Layer API",
    version="1.0.0"
)

# Load canonical hotel artifact
with open("output/canonical_hotels.json", "r", encoding="utf-8") as f:
    canonical_hotels = json.load(f)

# Load canonical room artifact
with open("output/canonical_rooms.json", "r", encoding="utf-8") as f:
    canonical_rooms = json.load(f)

# Load supplier source data
supplier_a = pd.read_csv("data/supplier_a.csv")
supplier_b = pd.read_csv("data/supplier_b.csv")


@app.get("/")
def home():
    return {
        "message": "Hotels Canonical Layer API is running"
    }


@app.get("/hotels")
def get_hotels(
    search: Optional[str] = None,
    min_confidence: float = 0,
    limit: int = 20,
    offset: int = 0
):

    hotels = canonical_hotels

    if search:
        hotels = [
            h for h in hotels
            if search.lower() in h["name"].lower()
        ]

    hotels = [
        h for h in hotels
        if h["confidence"] >= min_confidence
    ]

    return {
        "total": len(hotels),
        "limit": limit,
        "offset": offset,
        "data": hotels[offset:offset + limit]
    }


@app.get("/hotels/{canonical_id}")
def get_hotel(canonical_id: str):

    for hotel in canonical_hotels:

        if hotel["canonical_id"] == canonical_id:

            supplier_a_record = None

            if hotel["supplier_a_id"] is not None:

                a_match = supplier_a[
                    supplier_a["id"] == hotel["supplier_a_id"]
                ]

                if not a_match.empty:
                    supplier_a_record = a_match.iloc[0].to_dict()

            supplier_b_record = None

            if hotel["supplier_b_id"] is not None:

                b_match = supplier_b[
                    supplier_b["id"] == hotel["supplier_b_id"]
                ]

                if not b_match.empty:
                    supplier_b_record = b_match.iloc[0].to_dict()

            matched_rooms = [
                room
                for room in canonical_rooms
                if room["canonical_hotel_id"] == canonical_id
                and room["status"] == "matched"
            ]

            near_miss_candidates = [
                room
                for room in canonical_rooms
                if room["canonical_hotel_id"] == canonical_id
                and room["status"] == "near_miss"
            ]

            unmatched_supplier_a = [
                room
                for room in canonical_rooms
                if room["canonical_hotel_id"] == canonical_id
                and room["status"] == "unmatched_a"
            ]

            unmatched_supplier_b = [
                room
                for room in canonical_rooms
                if room["canonical_hotel_id"] == canonical_id
                and room["status"] == "unmatched_b"
            ]

            return {
                "canonical_hotel": hotel,
                "supplier_a": supplier_a_record,
                "supplier_b": supplier_b_record,
                "matched_rooms": matched_rooms,
                "near_miss_candidates": near_miss_candidates,
                "unmatched_supplier_a": unmatched_supplier_a,
                "unmatched_supplier_b": unmatched_supplier_b,
                "hotel_confidence": hotel["confidence"]
            }

    raise HTTPException(
        status_code=404,
        detail="Hotel not found"
    )