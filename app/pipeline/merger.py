class CanonicalMerger:

    def merge(self, hotel_a, hotel_b, confidence):

        canonical = {
            "canonical_id": f"CAN-{hotel_a['id']}-{hotel_b['id']}",

            "name": hotel_a["name"]
            if len(hotel_a["name"]) >= len(hotel_b["name"])
            else hotel_b["name"],

            "address": hotel_a["address"]
            if len(hotel_a["address"]) >= len(hotel_b["address"])
            else hotel_b["address"],

            "latitude": hotel_a["lat"],
            "longitude": hotel_a["lon"],

            "stars": hotel_a["stars"]
            if hotel_a["stars"] == hotel_a["stars"]
            else hotel_b["stars"],

            "supplier_a_id": hotel_a["id"],
            "supplier_b_id": hotel_b["id"],

            "confidence": confidence
        }

        return canonical
    def merge_single_source(self, hotel, source):

        return {
            "canonical_id": f"CAN-{source}-{hotel['id']}",
            "name": hotel["name"],
            "address": hotel["address"],

            "latitude": hotel["lat"],
            "longitude": hotel["lon"],

            "stars": hotel["stars"],

            "supplier_a_id": hotel["id"] if source == "A" else None,
            "supplier_b_id": hotel["id"] if source == "B" else None,

            "confidence": 100.0
        }