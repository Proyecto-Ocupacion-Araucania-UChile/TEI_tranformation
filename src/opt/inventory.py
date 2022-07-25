import pandas as pd

class Inventory:
    csv = "data/database/araucania_inventory.csv"
    df = pd.read_csv(csv, encoding="utf-8")

