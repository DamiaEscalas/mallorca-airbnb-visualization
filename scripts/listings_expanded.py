import pandas as pd

# Cargar dataset 
df = pd.read_csv("data/raw/listings.csv")

# Crear variables compuestas
df["host_professional"] = df["host_total_listings_count"] > 3

df["price"] = (
    df["price"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .astype(float)
)

df["price_category"] = pd.cut(
    df["price"],
    bins=[0, 100, 200, 400, 1000, float("inf")],
    labels=[
        "Budget",
        "Mid-range",
        "Premium",
        "Luxury",
        "Ultra Luxury"
    ]
)

df["host_local_ratio"] = (
    df["calculated_host_listings_count"] /
    df["host_total_listings_count"]
)

def classify_scope(ratio):

    if ratio >= 0.9:
        return "Local"

    elif ratio >= 0.3:
        return "Mixed"

    else:
        return "Global"

df["host_scope"] = df["host_local_ratio"].apply(classify_scope)

# Seleccionar variables relevantes
columns = [
    "id",
    "latitude",
    "longitude",
    "host_since",
    "price",
    "price_category",
    "room_type",
    "host_professional",
    "host_scope",
    "neighbourhood_cleansed"
]

df = df[columns]

# Convertir fecha
df["host_since"] = pd.to_datetime(df["host_since"], errors="coerce")

# Extraer año
df["host_year"] = df["host_since"].dt.year

# Quitar nulos
df = df.dropna(subset=["host_year"])

# Convertir a int
df["host_year"] = df["host_year"].astype(int)

# Año máximo
MAX_YEAR = 2025

# Crear filas duplicadas
expanded_rows = []

for _, row in df.iterrows():

    for year in range(row["host_year"], MAX_YEAR + 1):

        new_row = row.copy()
        new_row["current_year"] = year

        expanded_rows.append(new_row)

# Nuevo dataframe
expanded_df = pd.DataFrame(expanded_rows)

# Eliminar nulos
expanded_df = expanded_df.dropna()

# Guardar
expanded_df.to_csv("data/listings_expanded.csv", index=False)