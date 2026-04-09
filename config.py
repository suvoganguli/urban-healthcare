from pathlib import Path
from datetime import datetime

import geopandas as gpd
from shapely.geometry import box

# =========================================================
# PATHS
# =========================================================
BASE_DIR = Path(__file__).resolve().parent

PATHS = {
    "data_raw": BASE_DIR / "data" / "raw",
    "data_processed": BASE_DIR / "data" / "processed",
    "figures": BASE_DIR / "outputs" / "figures",
    "tables": BASE_DIR / "outputs" / "tables",
}

# =========================================================
# FILES
# =========================================================
FILES = {
    "hrsl_raw": PATHS["data_raw"] / "population" / "hrsl_kenya.tif",
    "hrsl_clipped": PATHS["data_processed"] / "hrsl_clipped_nairobi.tif",
    "grid": PATHS["data_processed"] / "grid.parquet",
    "grid_population": PATHS["data_processed"] / "grid_population.parquet",
    "hospitals": PATHS["data_processed"] / "hospitals.parquet",
    "roads_graphml": PATHS["data_processed"] / "roads.graphml",
    "nearest_access": PATHS["data_processed"] / "nearest_access.parquet",
    "multi_access": PATHS["data_processed"] / "multi_hospital_access.parquet",
    "hospital_burden": PATHS["data_processed"] / "hospital_burden.parquet",
    "effective_access": PATHS["data_processed"] / "effective_access.parquet",
    "archetypes": PATHS["data_processed"] / "archetypes.parquet",
}

# =========================================================
# STUDY AREA — NAIROBI
# =========================================================
CITY_NAME = "Nairobi"

# Covers Nairobi urban area with a reasonable surrounding buffer
BBOX = {
    "lon_min": 36.60,
    "lat_min": -1.50,
    "lon_max": 37.10,
    "lat_max": -1.10,
}

# =========================================================
# CRS
# =========================================================
CRS_WGS84 = "EPSG:4326"
CRS_PROJECTED = "EPSG:3857"

# =========================================================
# ANALYSIS SETTINGS
# =========================================================
GRID_SIZE_METERS = 1000
TOP_K_HOSPITALS = 3

DISTANCE_DECAY_ALPHA = 1.5
BURDEN_BETA = 1.0
EPSILON = 1e-6

# =========================================================
# HELPERS
# =========================================================
def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def ensure_project_dirs() -> None:
    for p in PATHS.values():
        ensure_dir(p)

def get_bbox_polygon():
    return box(
        BBOX["lon_min"],
        BBOX["lat_min"],
        BBOX["lon_max"],
        BBOX["lat_max"],
    )

def get_bbox_gdf():
    return gpd.GeoDataFrame(
        {"city": [CITY_NAME]},
        geometry=[get_bbox_polygon()],
        crs=CRS_WGS84,
    )

def savefig(fig, filename: str, dpi: int = 300):
    ensure_dir(PATHS["figures"])
    path = PATHS["figures"] / filename
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    print(f"Saved: {path}")
    return path

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def print_config_summary():
    print("===== CONFIG =====")
    print(f"City: {CITY_NAME}")
    print(f"BBOX: {BBOX}")
    print(f"Grid Size: {GRID_SIZE_METERS} m")
    print(f"Top-K Hospitals: {TOP_K_HOSPITALS}")
    print(f"Alpha: {DISTANCE_DECAY_ALPHA}")
    print(f"Beta: {BURDEN_BETA}")
    print(f"HRSL Path: {FILES['hrsl_raw']}")