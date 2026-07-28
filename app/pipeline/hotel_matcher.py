from rapidfuzz import fuzz


class HotelMatcher:

    def calculate_confidence(self, hotel_a, hotel_b, distance):

        # Name similarity (0–100)
        name_similarity = fuzz.token_sort_ratio(
            hotel_a["name"],
            hotel_b["name"]
        )

        # Distance score (0–100)
        distance_score = max(0, 100 - (distance * 100))

        # Star rating score
        if hotel_a["stars"] == hotel_b["stars"]:
            star_score = 100
        else:
            star_score = 50

        # Final confidence
        confidence = (
            0.45 * name_similarity +
            0.45 * distance_score +
            0.10 * star_score
        )

        return {
            "confidence": round(confidence, 2),
            "name_similarity": round(name_similarity, 2),
            "distance_score": round(distance_score, 2),
            "star_score": star_score,
        }