from rapidfuzz import fuzz

MATCH_THRESHOLD = 70


class RoomCanonicalizer:

    def __init__(self, normalizer):
        self.normalizer = normalizer

    def merge_attributes(self, attr_a, attr_b):

        merged = {}
        conflicts = {}

        for key in attr_a:

            value_a = attr_a.get(key)
            value_b = attr_b.get(key)

            if value_a is not None and value_b is not None:

                merged[key] = value_a

                if value_a != value_b:
                    conflicts[key] = {
                        "supplier_a": value_a,
                        "supplier_b": value_b
                    }

            else:
                merged[key] = (
                    value_a
                    if value_a is not None
                    else value_b
                )

        return merged, conflicts

    def canonicalize_hotel_rooms(
        self,
        canonical_hotel_id,
        rooms_a,
        rooms_b
    ):

        records = []

        used_b_rooms = set()
        seen_b_rooms = set()

        rooms_b_list = rooms_b.to_dict("records")

        for _, room_a in rooms_a.iterrows():

            best_room = None
            best_score = -1

            for room_b in rooms_b_list:

                if room_b["room_id"] in used_b_rooms:
                    continue

                score = fuzz.token_sort_ratio(
                    str(room_a["name"]),
                    str(room_b["name"])
                )

                if score > best_score:
                    best_score = score
                    best_room = room_b

            attr_a = self.normalizer.normalize_room(room_a)

            record = {
                "canonical_room_id": f"CANROOM-{room_a['room_id']}",
                "canonical_hotel_id": canonical_hotel_id,

                "supplier_a_room_id": room_a["room_id"],
                "supplier_b_room_id": None,

                "supplier_a_room_name": room_a["name"],
                "supplier_b_room_name": None,

                "normalized_attributes": attr_a,

                "confidence": None,
                "status": "unmatched_a"
            }

            if best_room is not None:

                seen_b_rooms.add(best_room["room_id"])

                attr_b = self.normalizer.normalize_room(best_room)

                merged_attributes, conflicts = self.merge_attributes(
                    attr_a,
                    attr_b
                )

                record.update({
                    "canonical_room_id":
                        f"CANROOM-{room_a['room_id']}-{best_room['room_id']}",
                    "supplier_b_room_id": best_room["room_id"],
                    "supplier_b_room_name": best_room["name"],
                    "normalized_attributes": merged_attributes,
                    "confidence": round(best_score, 2)
                })

                if conflicts:
                    record["attribute_conflicts"] = conflicts

                if best_score >= MATCH_THRESHOLD:
                    record["status"] = "matched"
                    used_b_rooms.add(best_room["room_id"])
                else:
                    record["status"] = "near_miss"

            records.append(record)

        # Add Supplier B rooms that were never selected
        for room_b in rooms_b_list:

            if room_b["room_id"] in seen_b_rooms:
                continue

            attr_b = self.normalizer.normalize_room(room_b)

            records.append({

                "canonical_room_id": f"CANROOM-{room_b['room_id']}",
                "canonical_hotel_id": canonical_hotel_id,

                "supplier_a_room_id": None,
                "supplier_b_room_id": room_b["room_id"],

                "supplier_a_room_name": None,
                "supplier_b_room_name": room_b["name"],

                "normalized_attributes": attr_b,

                "confidence": None,
                "status": "unmatched_b"
            })

        return records