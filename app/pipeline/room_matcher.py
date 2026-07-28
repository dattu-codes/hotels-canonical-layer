import re


class RoomMatcher:

    def normalize_room(self, room):

        text = f"{room['name']} {room.get('amenities', '')}".lower()

        attributes = {
            "bed_type": None,
            "occupancy": None,
            "meal_plan": None,
            "view": None,
        }

        # Bed Type
        if "king" in text:
            attributes["bed_type"] = "King"
        elif "queen" in text:
            attributes["bed_type"] = "Queen"
        elif "twin" in text:
            attributes["bed_type"] = "Twin"
        elif "double" in text:
            attributes["bed_type"] = "Double"
        elif "single" in text:
            attributes["bed_type"] = "Single"

        # Occupancy
        match = re.search(r"(\d+)\s*(guest|adult)", text)

        if match:
            attributes["occupancy"] = int(match.group(1))

        # Meal Plan
        if "breakfast" in text:
            attributes["meal_plan"] = "Breakfast Included"

        # View
        if "city view" in text:
            attributes["view"] = "City View"

        return attributes