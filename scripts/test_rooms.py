from app.pipeline.ingestion import DataLoader
from app.pipeline.room_matcher import RoomMatcher

loader = DataLoader()

rooms_a, rooms_b = loader.load_rooms()

matcher = RoomMatcher()

print("=" * 80)
print("ROOM NORMALIZATION TEST")
print("=" * 80)

for i in range(10):

    room = rooms_a.iloc[i]

    normalized = matcher.normalize_room(room)

    print("\nOriginal Room:")
    print(room["name"])

    print("\nAmenities:")
    print(room["amenities"])

    print("\nNormalized:")
    print(normalized)

    print("-" * 80)