import pandas as pd
from math import radians, sin, cos, sqrt, atan2


def haversine(lat1, lon1, lat2, lon2):
    R = 6371

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


class CandidateGenerator:

    def __init__(self, radius_km=1):
        self.radius = radius_km

    def get_candidates(self, hotel_a, supplier_b):

        candidates = []

        for _, hotel_b in supplier_b.iterrows():

            distance = haversine(
                hotel_a["lat"],
                hotel_a["lon"],
                hotel_b["lat"],
                hotel_b["lon"],
            )

            if distance <= self.radius:

                candidates.append(
                    {
                        "hotel": hotel_b,
                        "distance": distance,
                    }
                )

        return candidates