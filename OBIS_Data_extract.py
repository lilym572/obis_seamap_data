## Script to convert OBIS TSV to geopackage

#python -m venv \ns-gis.win.duke.edu\StudentData\2026\lm572

#cd path/to/your/project

import arcpy
from pathlib import Path
#python -m venv venv
import pandas as pd
#import geopandas as gpd
import matplotlib.pyplot as plt
#import geopandas as gpd

## Read the TSV
df = pd.read_csv(r"M:\emperor_seamounts\GIS\Data\OBIS\Occurrence.tsv", sep="\t")

## Schema
print(df.dtypes)


## Expor to geopackage
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df["decimalLongitude"], df["decimalLatitude"]),
    crs="EPSG:4326"
)

gdf.to_file(r"V:/emperor_seamounts/GIS/Data/OBIS/OBIS.gpkg", layer="occurrence", driver="GPKG")




## count unique taxon rank
counts = df["taxonRank"].value_counts(dropna=False)

ax = counts.plot.bar(figsize=(10, 5), color="steelblue")
ax.set(
    xlabel="Taxonomic rank",
    ylabel="Number of records",
    title="Records by taxonomic rank"
)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


## Table of most observed species
top_species = (
    df["species"]
    .value_counts()
    .rename_axis("species")
    .reset_index(name="observations")
)

top_species.head(20)

## Benthic species??
benthic = df[
    df["phylum"].isin([
        "Porifera",
        "Cnidaria",
        "Echinodermata",
        "Bryozoa",
        "Mollusca",
        "Arthropoda"       # crustaceans are commonly stored under Arthropoda
    ])
].copy()

# Count records by phylum
benthic["phylum"].value_counts().head(20)

# Count records by species
benthic["species"].value_counts().head(20)