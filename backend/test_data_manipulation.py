import geopandas as gpd

def get_borough_coordinates():
    gdf = gpd.read_file('../arrondissements.geojson')

    borough_dict = {}
    for index, row in gdf.iterrows():

        borough_dict[row["NOM"]] = row["geometry"]

    print(borough_dict)
    return borough_dict


get_borough_coordinates()
