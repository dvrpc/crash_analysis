sa_name = "hunting_park"

#Non-PDO Crashes by year 
q_nonpdo_by_year = fr""" 
select count (crash_table), crash_table.crash_year
	from {sa_name}_crashes as crash_table 
	where not (crash_table.max_severity_level = '0')
	group by crash_table.crash_year; 
    """
	
#KSI Crashes by year 
q_ksi_by_year = fr"""
select count (crash_table), crash_table.crash_year
	from {sa_name}_crashes as crash_table 
	where (crash_table.max_severity_level = '1' or crash_table.max_severity_level = '2')
	group by crash_table.crash_year """
	
#Non-PDO Crashes by collision type 
q_nonpdo_by_type = fr"""
select count (crash_table), crash_table.collision_type
	from {sa_name}_crashes as crash_table 
	where not (crash_table.max_severity_level = '0')
	group by crash_table.collision_type """

#KSI Crashes by collision type 
q_ksi_by_type = fr"""
select count (crash_table), crash_table.collision_type
	from {sa_name}_crashes as crash_table 
	where (crash_table.max_severity_level = '1' or crash_table.max_severity_level = '2')
	group by crash_table.collision_type"""
	
#Non-PDO Crashes by hour 
q_nonpdo_by_hour = fr"""
select count (crash_table), crash_table.hour_of_day 
	from {sa_name}_crashes as crash_table 
	where not (crash_table.max_severity_level = '0')
	group by crash_table.hour_of_day"""

#KSI Crashes by hour 
q_ksi_by_hour = fr"""
select count (crash_table), crash_table.hour_of_day 
	from {sa_name}_crashes as crash_table 
	where (crash_table.max_severity_level = '1' or crash_table.max_severity_level = '2')
	group by crash_table.hour_of_day"""
	
#Non-PDO Crashes by Illumination 
q_nonpdo_by_light = fr"""
select count (crash_table), crash_table.illumination 
	from {sa_name}_crashes as crash_table 
	where not (crash_table.max_severity_level = '0')
	group by crash_table.illumination"""

#KSI Crashes by Illumination 
q_ksi_by_light = fr"""
select count (crash_table), crash_table.illumination 
	from {sa_name}_crashes as crash_table 
	where (crash_table.max_severity_level = '1' or crash_table.max_severity_level = '2')
	group by crash_table.illumination"""
	
#Non-PDO Crashes by Weather Conditions 
q_nonpdo_by_condition = fr"""
select count (crash_table), crash_table.road_condition 
	from {sa_name}_crashes as crash_table 
	where not (crash_table.max_severity_level = '0')
	group by crash_table.road_condition"""

#KSI Crashes by Weather Conditions  
q_ksi_by_condition = fr"""
select count (crash_table), crash_table.road_condition 
	from crash_penn{sa_name}_crashessylvania as crash_table 
	where (crash_table.max_severity_level = '1' or crash_table.max_severity_level = '2')
	group by crash_table.road_condition"""

#People Injured in Crashes (non-PDO) (Bicyclists) **NEEDS TO BE UPDATED IN DATA SETUP
#WHAT KIND OF CHART IS THIS GOING TO MAKE? OR DO YOU ONLY NEED THE NUMBER
q_injured_bicyclists = fr"""
select count (person_table)
    from crash_pa_person as person_table
    left join crash_pa_vehicle as vehicle_table on (concat(text(person_table.crn), text(person_table.unit_num)) = concat(text(vehicle_table.crn), text(vehicle_table.unit_num)))
    where vehicle_table.unit_type = '11'
    and not (person_table.inj_severity = '0')"""