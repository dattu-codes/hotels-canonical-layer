from rapidfuzz import fuzz


class RoomAligner:

    def match_rooms(self, rooms_a, rooms_b):

        matched_rooms = []
        near_misses = []
        used_rooms = set()

        for _, room_a in rooms_a.iterrows():

            best_room = None
            best_score = -1

            for _, room_b in rooms_b.iterrows():

                if room_b["room_id"] in used_rooms:
                    continue

                score = fuzz.token_sort_ratio(
                    room_a["name"],
                    room_b["name"]
                )

                if score > best_score:
                    best_score = score
                    best_room = room_b

            if best_room is not None:
                
                if best_score >= 70:

                    used_rooms.add(best_room["room_id"])

                    matched_rooms.append({
                        "supplier_a_room": {
                            "room_id": room_a["room_id"],
                            "name": room_a["name"],
                            "amenities": "" if str(room_a["amenities"]) == "nan" else room_a["amenities"]
                        },
                        "supplier_b_room": {
                            "room_id": best_room["room_id"],
                            "name": best_room["name"],
                            "amenities": "" if str(best_room["amenities"]) == "nan" else best_room["amenities"]
                        },
                        "confidence": round(best_score, 2)
                    })

                else:

                    near_misses.append({
                        "supplier_a_room": room_a["name"],
                        "supplier_b_room": best_room["name"],
                        "confidence": round(best_score, 2)
                    })

        return {
            "matched_rooms": matched_rooms,
            "near_misses": near_misses
        }