# FDS_backend.py
import pandas as pd

# -----------------------------------------------------------
# Load and clean COVID-19 data
# -----------------------------------------------------------
def load_data(path: str = "country_wise_latest_covid.csv") -> pd.DataFrame:
    df = pd.read_csv(path)

    # Normalize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Deduplicate column names (fix for pandas 3.x)
    df = df.loc[:, ~df.columns.duplicated()].copy()

    # --- Flexible column renaming ---
    # Identify possible country column variants
    country_col_candidates = [c for c in df.columns if "country" in c or "location" in c or "region" in c]
    if country_col_candidates:
        df.rename(columns={country_col_candidates[0]: "country"}, inplace=True)
    else:
        raise KeyError("❌ Could not find a column representing 'country' or 'location' in the dataset.")

    # Optional: if 'region' not found, create placeholder
    if "region" not in df.columns:
        df["region"] = "Unknown"

    # Derived metrics
    if "confirmed" in df.columns and "recovered" in df.columns:
        df["recovery_rate"] = (df["recovered"] / df["confirmed"] * 100).round(2)
    else:
        df["recovery_rate"] = 0

    if "confirmed" in df.columns and "deaths" in df.columns:
        df["death_rate"] = (df["deaths"] / df["confirmed"] * 100).round(2)
    else:
        df["death_rate"] = 0

    df.fillna(0, inplace=True)
    return df


# -----------------------------------------------------------
# Compute KPIs
# -----------------------------------------------------------
def compute_kpis(df: pd.DataFrame) -> dict:
    return {
        "Total Confirmed Cases": int(df["confirmed"].sum()) if "confirmed" in df.columns else 0,
        "Total Deaths": int(df["deaths"].sum()) if "deaths" in df.columns else 0,
        "Total Recovered": int(df["recovered"].sum()) if "recovered" in df.columns else 0,
    }


# -----------------------------------------------------------
# Get Top N Countries by a Metric
# -----------------------------------------------------------
def top_n_countries(df: pd.DataFrame, column: str, n: int = 10) -> pd.DataFrame:
    if column not in df.columns:
        return pd.DataFrame()
    top_df = df.nlargest(n, column)[["country", column]].copy()
    top_df = top_df.loc[:, ~top_df.columns.duplicated()]
    return top_df


# -----------------------------------------------------------
# Region Summary (Pie Chart)
# -----------------------------------------------------------
def region_summary(df: pd.DataFrame) -> pd.DataFrame:
    if "region" not in df.columns:
        return pd.DataFrame()
    region_df = df.groupby("region", as_index=False)["confirmed"].sum().sort_values("confirmed", ascending=False)
    return region_df


# -----------------------------------------------------------
# Filtering logic
# -----------------------------------------------------------
def filter_data(
    df: pd.DataFrame,
    country_list=None,
    region_list=None,
    min_cases: int = 0,
    max_cases: int | None = None,
    search_term: str | None = None,
) -> pd.DataFrame:
    filtered = df.copy()

    if country_list:
        filtered = filtered[filtered["country"].isin(country_list)]

    if region_list and "region" in filtered.columns:
        filtered = filtered[filtered["region"].isin(region_list)]

    if min_cases:
        filtered = filtered[filtered["confirmed"] >= min_cases]

    if max_cases:
        filtered = filtered[filtered["confirmed"] <= max_cases]

    if search_term:
        filtered = filtered[filtered["country"].str.contains(search_term, case=False, na=False)]

    filtered = filtered.loc[:, ~filtered.columns.duplicated()]
    return filtered
