"""
data_setup.py
------------------
This script pulls the latest crash datatable from the GIS database.
It then clips that data to a 100 ft buffer around a linear study area.
Assumes starting SRID of study area linework as 2272 (or something based in feet).
The result of this function is a geodataframe containing crashes within the study area.

TO UPDATE for different purposes/study areas: 
    -Crash Data Query
    -sa_shape
    -sa_name
"""

import geopandas as gpd
import pandas as pd
from sqlalchemy_utils import database_exists, create_database
import env_vars as ev
from env_vars import GIS_ENGINE, ENGINE

#Crash Data Query
###this query should be broad and include everything needed to generate charts
###joins to other tables should happen before or within this querey
Q_crash_data = """select 
                crn,
                crash_year, 
                county, 
                fatal_count , 
                maj_inj_count, 
                bicycle_count,
                ped_count,
                ped_death_count,
                bicycle_death_count,
                collision_type,
                max_severity_level,
                hour_of_day,
                illumination,
                road_condition,
                shape
            from transportation.crash_pennsylvania cp 
            where district = '06'
            and county = '67'
            and shape is not null;"""


Q_person_data = """select *
            from transportation.crash_pa_person p
            where p.crn in (
                select crn from transportation.crash_pennsylvania cp
                where county = '67'
            );"""
Q_vehicle_data = """select *
            from transportation.crash_pa_vehicle v
            where v.crn in (
                select crn from transportation.crash_pennsylvania cp
                where county = '67'
            );"""
Q_flag_data = """select *
            from transportation.crash_pa_flag f
            where f.crn in (
                select crn from transportation.crash_pennsylvania cp
                where county = '67'
            );"""
Q_road_data = """select *
            from transportation.crash_pa_roadway r
            where r.crn in (
                select crn from transportation.crash_pennsylvania cp
                where county = '67'
            );"""
Q_PennDOT_roads = """select *
            from transportation.padot_rms pr
            where cty_code = '67'
            ;"""
Q_local_roads = """select *
            from transportation.padot_localroads pl
            where cty_code = '67'
            ;"""
# Q_get_phila = """select cb.*
#             from boundaries.countyboundaries cb
#             where co_name = 'Philadelphia';"""

def clip_crashes():

    # sa_shape = "Hunting_Park_Study_Area_"
    sa_name = "phila"

    #create database and enable postgis
    if not database_exists(ENGINE.url):
        create_database(ENGINE.url)
    ENGINE.execute("CREATE EXTENSION IF NOT EXISTS postgis;")

    #read study area shapefile and write to postgres

    # study_area = gpd.GeoDataFrame.from_postgis(
    #     Q_get_phila,
    #     con = GIS_ENGINE,
    #     geom_col= "shape",
    # )
    # study_area.to_postgis('study_area', con=ENGINE, if_exists="replace")

    # study_area = gpd.read_file(fr"{ev.DATA_ROOT}/{sa_shape}.shp")
    # study_area.to_postgis('study_area', con=ENGINE, if_exists="replace")
 
    #create 100ft buffer around study area and save as new table
    # ENGINE.execute("""
    #     CREATE TABLE IF NOT EXISTS sa_buffer AS(
    #     select st_transform(st_buffer(st_linemerge(st_union(geometry)),100), 4326) as buff
    #     from study_area sa);""")

    #read crash data from gis database
    crash_data = gpd.GeoDataFrame.from_postgis(
        Q_crash_data, 
        con = GIS_ENGINE,
        geom_col = "shape",
    )
    #write to postgis
    crash_data.to_postgis('crash_data', con=ENGINE, if_exists="replace")

    # sa_crashes = gpd.GeoDataFrame.from_postgis(
    #     """SELECT cd.*
    #     FROM crash_data cd JOIN study_area sa ON ST_Intersects(cd.shape, sa.shape) """,
    #     con = ENGINE,
    #     geom_col= "shape"
    # )

    #export clipped crash data to shapefile
    # sa_crashes.to_file(fr"{ev.DATA_ROOT}/{sa_name}_crashes.shp")
    # print("To shapefile: Complete")

    #write dataframe to postgres database
    # sa_crashes.to_postgis(fr"{sa_name}_crashes", con=ENGINE, if_exists="replace")
    

    #read and write person data to be joined later
    person_data = pd.read_sql(
        Q_person_data,
        con = GIS_ENGINE
    )
    person_data.to_sql('person_data', ENGINE, if_exists="replace")

    #read and write vehicle data to be joined later
    vehicle_data = pd.read_sql(
        Q_vehicle_data,
        con = GIS_ENGINE
    )
    vehicle_data.to_sql('vehicle_data', ENGINE, if_exists="replace")

    #read and write flag data to be joined later
    flag_data = pd.read_sql(
        Q_flag_data,
        con = GIS_ENGINE
    )
    flag_data.to_sql('flag_data', ENGINE, if_exists="replace")

    #read and write roadway data to be joined later
    roadway_data = pd.read_sql(
        Q_road_data,
        con = GIS_ENGINE
    )
    roadway_data.to_sql('roadway_data', ENGINE, if_exists="replace")

    print("All data to postgis: Complete")

    #read and write penndot roads data to be joined later
    padot_roads = pd.read_sql(
        Q_PennDOT_roads,
        con = GIS_ENGINE
    )
    padot_roads.to_sql('penndot_roads', ENGINE, if_exists="replace")

    #read and write penndot roads data to be joined later
    local_roads = pd.read_sql(
        Q_local_roads,
        con = GIS_ENGINE
    )
    local_roads.to_sql('local_roads', ENGINE, if_exists="replace")


    #return sa_crashes

if __name__ == "__main__":
    clip_crashes()
