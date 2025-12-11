"""
data_setup.py
------------------
This script pulls the latest crash datatable from the GIS database.
Data is pulled based on a pre-identified list of CRNs.
The crash data subset necessary for tables and charts is then written to a local posgres DB for forther anlaysis.
"""

import geopandas as gpd
import pandas as pd
from sqlalchemy_utils import database_exists, create_database
import env_vars as ev
import csv
from env_vars import GIS_ENGINE, ENGINE
from typing import List, Tuple

#Crash Data Query
###this query should be broad and include everything needed to generate tables/charts
query= """select 
                cp.crn,
                crash_year, 
                county, 
                fatal_count , 
                susp_serious_inj_count, 
                susp_minor_inj_count,
                ped_count,
                ped_susp_serious_inj_count,
                ped_death_count,
                bicycle_count,
                bicycle_susp_serious_inj_count,
                bicycle_death_count,
                collision_type,
                max_severity_level,
                hour_of_day,
                illumination,
                road_condition,
                heavy_truck_count, 
                small_truck_count,
                shape
            from transportation.crash_pennsylvania cp 
            where crn = ANY(%s);"""

def read_crn_from_csv (filename: str, column_name: str = 'crn')-> List[int]:
    crn_list = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            crn = row.get(column_name, '').strip()
            if crn and crn.isdigit():
                crn_list.append(int(crn))
    return crn_list

def query_database(crn_list: List[int]) -> List[Tuple]:

    #create database and enable postgis
    if not database_exists(ENGINE.url):
        create_database(ENGINE.url)
    ENGINE.execute("CREATE EXTENSION IF NOT EXISTS postgis;")

    #Crash Data Query
    ###this query should be broad and include everything needed to generate tables/charts
    query= """select 
                    cp.crn,
                    crash_year, 
                    county, 
                    fatal_count , 
                    susp_serious_inj_count, 
                    susp_minor_inj_count,
                    ped_count,
                    ped_susp_serious_inj_count,
                    ped_death_count,
                    bicycle_count,
                    bicycle_susp_serious_inj_count,
                    bicycle_death_count,
                    collision_type,
                    max_severity_level,
                    hour_of_day,
                    illumination,
                    road_condition,
                    heavy_truck_count, 
                    small_truck_count,
                    shape
                from transportation.crash_pennsylvania cp 
                where crn = ANY(%s);"""

    #read crash data from gis database
    crash_data = gpd.GeoDataFrame.from_postgis(
        query, 
        con = GIS_ENGINE,
        geom_col = "shape",
    )
    #write to postgis
    print("Writing crash data subset to local DB")
    crash_data.to_postgis('crash_data', con=ENGINE, if_exists="replace")

def main():
    # Configuration
    csv_file = 'LincolnHwy-crns.csv'        # Your CSV file
    crn_column = 'crn'                # Column name containing CRNs
    
    # Read CRN list from CSV
    print(f"Reading CRN numbers from {csv_file}...")
    crn_list = read_crn_from_csv(csv_file, crn_column)
    print(f"Found {len(crn_list)} CRN numbers: {crn_list}")
    
    # Query database
    print(f"\nQuerying GIS database...")
    query_database(crn_list)


if __name__ == "__main__":
    main()
