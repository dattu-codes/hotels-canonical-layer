import pandas as pd

# Load hotel datasets
supplier_a = pd.read_csv("data/supplier_a.csv")
supplier_b = pd.read_csv("data/supplier_b.csv")

# Load room datasets
rooms_a = pd.read_csv("data/rooms_a.csv")
rooms_b = pd.read_csv("data/rooms_b.csv")

# Print basic information
print("=" * 60)
print("SUPPLIER A")
print("=" * 60)
print(supplier_a.info())

print("\nFirst 5 Hotels:")
print(supplier_a.head())

print("\nMissing Values:")
print(supplier_a.isnull().sum())

print("\n")

print("=" * 60)
print("SUPPLIER B")
print("=" * 60)
print(supplier_b.info())

print("\nFirst 5 Hotels:")
print(supplier_b.head())

print("\nMissing Values:")
print(supplier_b.isnull().sum())

print("\n")

print("=" * 60)
print("ROOMS A")
print("=" * 60)
print(rooms_a.info())

print("\nFirst 5 Rooms:")
print(rooms_a.head())

print("\nMissing Values:")
print(rooms_a.isnull().sum())

print("\n")

print("=" * 60)
print("ROOMS B")
print("=" * 60)
print(rooms_b.info())

print("\nFirst 5 Rooms:")
print(rooms_b.head())

print("\nMissing Values:")
print(rooms_b.isnull().sum())
print("\n" + "=" * 60)
print("SAMPLE HOTELS - SUPPLIER A")
print("=" * 60)

print(supplier_a[["id","name", "address"]].head(20))


print("\n" + "=" * 60)
print("SAMPLE HOTELS - SUPPLIER B")
print("=" * 60)

print(supplier_b[["id","name", "address"]].head(20))