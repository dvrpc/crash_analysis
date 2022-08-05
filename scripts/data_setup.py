"""
get_data.py
------------------
This script pulls the latest crash datatable from the GIS database.
It then clips that data to the a 100 ft buffer around the linear study area.
If the study area is a polygon instead and no buffer is needed, update lines...
Results are written to shapefile and postgres
"""

import csv
from datetime import date
import pandas as pd
import geopandas as gpd
from sqlalchemy_utils import database_exists, create_database
import env_vars as ev
from env_vars import GIS_ENGINE, ENGINE

sa_shape = "Hunting_Park_Study_Area_"
sa_name = "Hunting_Park"

def main():

    #read study area shapefile and create buffer
    study_area = gpd.GeoDataFrame.read_file(fr"{ev.DATA_ROOT}/{sa_shape}.shp")
    sa_buffer = study_area.buffer(100)


    #read crash data from gis database

    crash_data = gpd.GeoDataFrame.from_postgis(
        #this query should be broad and include everything you would want for generating charts
        #joins to other tables should happen before or within this querey
        #this simple query is here is an example
        fr"""select 
                crash_year, 
                county, 
                fatal_count , 
                maj_inj_count, 
                shape 
            from crash_pennsylvania cp 
            where district = '06'
            and crash_year = '2019'
            and county = '67';""", 
        con = GIS_ENGINE
        geom_col = "shape",
    )

    #clip crash data to buffer
    sa_crashes = gpd.clip(crash_data, sa_buffer)

    #export clipped crash data to shapefile
    sa_crashes.to_file(fr"{ev.DATA_ROOT}/{sa_name}_crashes.shp")
    print("To shapefile: Complete")

    #create database
    if not database_exists(ENGINE.url):
        create_database(ENGINE.url)
    ENGINE.execute("CREATE EXTENSION IF NOT EXISTS postgis;")

    #write dataframe to postgres database
    sa_crashes.to_postgis(fr"{sa_name}_crashes", con=ENGINE, if_exists="replace")


if __name__ == "__main__":
    main()
