
### queries run in DBeaver and QGIS; results analyzed and visualized in sheets and Q


#percentage of speeding related crashes in philadelhpia by year (used to create summary chart)
q_sr_by_year = """
    select speeding_related, count(*)
    from flag_data fd 
    where fd.crn in (
        select crn from crash_data cd where crash_year = '2022' )
    group by speeding_related;
	"""


#percentage of speeding related crashes in philadelphia by functional class (used to create summary chart)
q_sr_by_fc = """
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
    group by speeding_related, dvrpcfc;
"""


# summarize speeding realted and not speeding related crashes on state owned roads (building block/interim query)
q_sr_summary = """
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
    and b.segment = c.segment;
"""

#expanded and joined to more stuff; used to map segments with  "majority" speeding related crashes
q_sr_by_seg_fcjoin = """
    with tblA as(
        select *
        from crash_data cd 
        inner join roadway_data rd 
        on cd.crn = rd.crn
        inner join flag_data fd
        on cd.crn  = fd.crn
        ),
    tblB as(
        select route, segment, count(*) as num_sr, dvrpcfc, speed_limit
        from tblA a
        where speeding_related = 1
        and road_owner = 2
        and crash_year = 2022
        group by route, segment, dvrpcfc, speed_limit
        ),
    tblC as(
        select route, segment, count(*) as num_not_sr, dvrpcfc, speed_limit
        from tblA a
        where speeding_related = 0
        and road_owner = 2
        and crash_year = 2022
        group by route, segment, dvrpcfc, speed_limit
    ),
    tblD as(
        select b.route, b.segment, b.num_sr, c.num_not_sr, b.dvrpcfc, b.speed_limit
        from tblb b
        inner join tblC c
        on b.route = c.route
        and b.segment = c.segment
    )
    select d.*, pr.shape
    from tblD d
    inner join penndot_roads pr 
    on d.route = pr.st_rt_no
    and  LPAD(d.segment, 4, '0') = pr.seg_no;
    """