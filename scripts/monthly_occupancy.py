import pandas as pd

# Cargar datasets

old_df = pd.read_csv("data/raw/calendar-previo.csv.gz", compression="gzip")
new_df = pd.read_csv("data/raw/calendar.csv.gz", compression="gzip")

# Convertir a fecha
old_df["date"] = pd.to_datetime(old_df["date"])
new_df["date"] = pd.to_datetime(new_df["date"])

# Filtrar rangos de cada dataset
old_filtered = old_df[
    (old_df["date"] >= "2025-06-25") &
    (old_df["date"] <= "2025-09-20")
]

new_filtered = new_df[
    (new_df["date"] >= "2025-09-21") &
    (new_df["date"] <= "2026-06-24")
]

# Concatenar datasets
calendar_df = pd.concat(
    [old_filtered, new_filtered],
    ignore_index=True
)

# Transformar available en bool
calendar_df["available"] = (
    calendar_df["available"]
    .astype(str)
    .str.lower()
    .map({
        "t": True,
        "f": False
    })
)

# Crear variable occupied
calendar_df["occupied"] = ~calendar_df["available"]

# Crear variables mes
calendar_df["month_num"] = (
    calendar_df["date"]
    .dt.month
)

months_es = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre"
}


calendar_df["month"] = (
    calendar_df["month_num"]
    .map(months_es)
)

# Agrupar por mes
monthly_occupancy = (
    calendar_df
    .groupby(["month_num", "month"])["occupied"]
    .mean()
    .reset_index()
)

# Calcular tasa de ocupación
monthly_occupancy["occupancy_rate"] = (
    monthly_occupancy["occupied"] * 100
)

monthly_occupancy = (
    monthly_occupancy
    .sort_values("month_num")
)

# Guardar dataset
monthly_occupancy.to_csv(
    "data/monthly_occupancy.csv",
    index=False
)
