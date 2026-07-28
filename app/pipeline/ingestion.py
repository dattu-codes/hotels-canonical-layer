import pandas as pd


class DataLoader:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir

    def load_hotels(self):
        supplier_a = pd.read_csv(f"{self.data_dir}/supplier_a.csv")
        supplier_b = pd.read_csv(f"{self.data_dir}/supplier_b.csv")
        return supplier_a, supplier_b

    def load_rooms(self):
        rooms_a = pd.read_csv(f"{self.data_dir}/rooms_a.csv")
        rooms_b = pd.read_csv(f"{self.data_dir}/rooms_b.csv")
        return rooms_a, rooms_b