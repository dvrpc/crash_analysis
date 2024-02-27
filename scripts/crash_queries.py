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



############### for SLS work
#percentage of speeding related crashes in philadelhpia by year
select speeding_related, count(*)
from flag_data fd 
where fd.crn in (
	select crn from crash_data cd where crash_year = '2022' )
group by speeding_related 


#percentage of speeding related crashes in philadelphia by functional class
with tblA as(
	select *
	from crash_data cd 
	inner join roadway_data rd 
	on cd.crn = rd.crn
	inner join flag_data fd
	on cd.crn  = fd.crn
	)
select speeding_related, dvrpcfc, count(*)
from tblA
group by speeding_related, dvrpcfc

#summarize speeding related crashes by state owned road
with tblA as(
	select *
	from crash_data cd 
	inner join roadway_data rd 
	on cd.crn = rd.crn
	inner join flag_data fd
	on cd.crn  = fd.crn
	),
tblB as(
	select route, segment, count(*)
	from tblA a
	where speeding_related = 1
	and road_owner = 2
	group by route, segment
	)
create table test_join as(
	select b.*, pr.shape
	from tblB b
	inner join penndot_roads pr 
	on b.route = pr.st_rt_no
	and  LPAD(b.segment, 4, '0') = pr.seg_no
);

# summarize percent of speeding realted crashes on state owned roads
with tblA as(
	select *
	from crash_data cd 
	inner join roadway_data rd 
	on cd.crn = rd.crn
	inner join flag_data fd
	on cd.crn  = fd.crn
	),
tblB as(
	select route, segment, count(*) as num_sr
	from tblA a
	where speeding_related = 1
	and road_owner = 2
    and crash_year = 2022
	group by route, segment
	),
tblC as(
	select route, segment, count(*) as num_not_sr
	from tblA a
	where speeding_related = 0
	and road_owner = 2
    and crash_year = 2022
	group by route, segment
)
select b.route, b.segment, b.num_sr, c.num_not_sr
from tblb b
inner join tblC c
on b.route = c.route
and b.segment = c.segment


#expanded and joined to more stuff
with tblA as(
	select *
	from crash_data cd 
	inner join roadway_data rd 
	on cd.crn = rd.crn
	inner join flag_data fd
	on cd.crn  = fd.crn
	),
tblB as(
	select route, segment, count(*) as num_sr
	from tblA a
	where speeding_related = 1
	and road_owner = 2
	and crash_year = 2022
	group by route, segment
	),
tblC as(
	select route, segment, count(*) as num_not_sr
	from tblA a
	where speeding_related = 0
	and road_owner = 2
	and crash_year = 2022
	group by route, segment
),
	tblD as(
	select b.route, b.segment, b.num_sr, c.num_not_sr
	from tblb b
	inner join tblC c
	on b.route = c.route
	and b.segment = c.segment
),
tblE as(
select d.*, pr.shape
from tblD d
inner join penndot_roads pr 
on d.route = pr.st_rt_no
and  LPAD(d.segment, 4, '0') = pr.seg_no 
)
select e.*, r.dvrpcfc 
from tblE e
inner join roadway_data r
on e.route = r.route
and e.segment = r.segment

