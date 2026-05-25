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

df["price_per_person"] = (
    df["price"] / df["accommodates"]
)

# Seleccionar variables relevantes
columns_clean = [

    # IDs
    "id",
    "host_id",

    # Localización
    "neighbourhood_cleansed",
    "latitude",
    "longitude",

    # Temporal
    "host_since",

    # Precio
    "price",
    "price_category",
    "price_per_person",

    # Tipo alojamiento
    "room_type",
    "property_type",
    "accommodates",

    # Profesionalización
    "host_total_listings_count",
    "host_professional",
    "host_scope",

    # Reviews / calidad
    "number_of_reviews",
    "review_scores_rating",
    "review_scores_accuracy",
    "review_scores_cleanliness",
    "review_scores_checkin",
    "review_scores_communication",
    "review_scores_location",
    "review_scores_value",
    "reviews_per_month",

    # Superhost
    "host_is_superhost",

    # Ganancias
    "estimated_revenue_l365d",

    # Ocupación
    "estimated_occupancy_l365d"
]

# Guardar dataset limpio
df_clean = df[columns_clean]

df_clean.to_csv(
    "data/listings_clean.csv",
    index=False
)