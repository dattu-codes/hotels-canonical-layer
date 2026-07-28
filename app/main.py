from fastapi import FastAPI, HTTPException
from typing import Optional
import json
import pandas as pd
from app.pipeline.room_alignment import RoomAligner

aligner = RoomAligner()

app = FastAPI(
    title="Hotels Canonical Layer API",
    version="1.0.0"
)


with open("output/canonical_hotels.json", "r", encoding="utf-8") as f:
    canonical_hotels = json.load(f)
    
supplier_a = pd.read_csv("data/supplier_a.csv")
supplier_b = pd.read_csv("data/supplier_b.csv")
rooms_a = pd.read_csv("data/rooms_a.csv")
rooms_b = pd.read_csv("data/rooms_b.csv")


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
            
            supplier_a_record = supplier_a[
                supplier_a["id"] == hotel["supplier_a_id"]
            ].iloc[0].to_dict()

            supplier_b_record = supplier_b[
                supplier_b["id"] == hotel["supplier_b_id"]
            ].iloc[0].to_dict()
            
            hotel_rooms_a = rooms_a[
                rooms_a["hotel_id"] == hotel["supplier_a_id"]
            ]

            hotel_rooms_b = rooms_b[
                rooms_b["hotel_id"] == hotel["supplier_b_id"]
            ]

            room_results = aligner.match_rooms(
                hotel_rooms_a,
                hotel_rooms_b
            )

            matched_rooms = room_results["matched_rooms"]
            near_miss_candidates = room_results["near_misses"]

            return {
                "canonical_hotel": hotel,
                "supplier_a": supplier_a_record,
                "supplier_b": supplier_b_record,
                "matched_rooms": matched_rooms,
                "near_miss_candidates": near_miss_candidates,
                "hotel_confidence": hotel["confidence"]
            }

    raise HTTPException(
        status_code=404,
        detail="Hotel not found"
    )