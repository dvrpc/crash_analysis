sa_name = "lincoln-hwy"

#crashes by mode and severity
q_mode_severity = fr""" 
	SELECT 
		mode,
		SUM(CASE WHEN max_severity = 'ksi' THEN crash_count ELSE 0 END) AS "KSI",
		SUM(CASE WHEN max_severity = 'non-ksi-inj' THEN crash_count ELSE 0 END) AS "Non-KSI Injury",
		SUM(CASE WHEN max_severity = 'pdo' THEN crash_count ELSE 0 END) AS "PDO",
		SUM(crash_count) AS "Total"
	FROM (
		SELECT 
			COUNT(crn) AS crash_count,
			CASE
				WHEN ped_count::integer > 0 THEN 'Pedestrian-involved'
				WHEN bicycle_count::integer > 0 THEN 'Bicyclist-involved'
				ELSE 'Vehicle Occupants Only'
			END AS Mode,
			CASE
				WHEN max_severity_level::integer = 0 THEN 'pdo'
				WHEN max_severity_level::integer IN(1,2) THEN 'ksi'
				WHEN max_severity_level::integer IN (3,4,8,9) THEN 'non-ksi-inj'
			END AS max_severity
		FROM crash_data
		GROUP BY mode, max_severity
	) AS subquery
	GROUP BY mode

	UNION ALL

	SELECT 
		'Total' AS Mode,
		SUM(CASE WHEN max_severity = 'ksi' THEN crash_count ELSE 0 END) AS "KSI",
		SUM(CASE WHEN max_severity = 'non-ksi-inj' THEN crash_count ELSE 0 END) AS "Non-KSI Injury",
		SUM(CASE WHEN max_severity = 'pdo' THEN crash_count ELSE 0 END) AS "PDO",
		SUM(crash_count) AS "Total"
	FROM (
		SELECT 
			COUNT(crn) AS crash_count,
			CASE
				WHEN ped_count::integer > 0 THEN 'Pedestrian-involved'
				WHEN bicycle_count::integer > 0 THEN 'Bicyclist-involved'
				ELSE 'Vehicle Occupants Only'
			END AS mode,
			CASE
				WHEN max_severity_level::integer = 0 THEN 'pdo'
				WHEN max_severity_level::integer IN(1,2) THEN 'ksi'
				WHEN max_severity_level::integer IN (3,4,8,9) THEN 'non-ksi-inj'
			END AS max_severity
		FROM crash_data
		GROUP BY mode, max_severity
	) AS subquery;
    """
	
#Crashes by year with KSI breakout 
q_total_and_ksi_by_year = fr"""
SELECT 
    crash_year AS year,
    SUM(CASE WHEN max_severity = 'ksi' THEN crash_count ELSE 0 END) AS "KSI",
    SUM(crash_count) AS "Total Crashes"
FROM (
    SELECT 
        COUNT(crn) AS crash_count,
        crash_year,
        CASE
            WHEN max_severity_level::integer = 0 THEN 'pdo'
            WHEN max_severity_level::integer IN(1,2) THEN 'ksi'
            WHEN max_severity_level::integer IN (3,4,8,9) THEN 'non-ksi-inj'
        END AS max_severity
    FROM crash_data
    GROUP BY crash_year, max_severity_level
) AS subquery
GROUP BY crash_year
ORDER BY crash_year; """
	
#Crashes by collision type and severity
q_crashes_by_type = fr"""
select * from (
SELECT
    collision_type,
    SUM(CASE WHEN max_severity = 'pdo' THEN crash_count ELSE 0 END) AS "PDO",
    SUM(CASE WHEN max_severity = 'ksi' THEN crash_count ELSE 0 END) AS "KSI",
    SUM(CASE WHEN max_severity = 'non-ksi-inj' THEN crash_count ELSE 0 END) AS "Non-KSI Injury",
    SUM(crash_count) AS "Total"
FROM (
    SELECT
        COUNT(cd.crn) AS crash_count,
        cd.collision_type AS collision_type,
        CASE
            WHEN max_severity_level::integer = 0 THEN 'pdo'
            WHEN max_severity_level::integer IN(1,2) THEN 'ksi'
            WHEN max_severity_level::integer IN (3,4,8,9) THEN 'non-ksi-inj'
        END AS max_severity
    FROM crash_data cd
    GROUP BY collision_type, max_severity
) AS subquery
GROUP BY collision_type
UNION ALL
SELECT
    'Total' AS collision_type,
    SUM(CASE WHEN max_severity = 'pdo' THEN crash_count ELSE 0 END) AS "PDO",
    SUM(CASE WHEN max_severity = 'ksi' THEN crash_count ELSE 0 END) AS "KSI",
    SUM(CASE WHEN max_severity = 'non-ksi-inj' THEN crash_count ELSE 0 END) AS "Non-KSI Injury",
    SUM(crash_count) AS "Total"
FROM (
    SELECT
        COUNT(cd.crn) AS crash_count,
        cd.collision_type,
        CASE
            WHEN max_severity_level::integer = 0 THEN 'pdo'
            WHEN max_severity_level::integer IN(1,2) THEN 'ksi'
            WHEN max_severity_level::integer IN (3,4,8,9) THEN 'non-ksi-inj'
        END AS max_severity
    FROM crash_data cd
    GROUP BY cd.collision_type, max_severity
) AS subquery
) as final_result
ORDER BY 
    CASE WHEN collision_type = 'Total' THEN 1 ELSE 0 END,
    collision_type;"""


# crashes by mode, injury severity, and illuminaton
	"""SELECT 
		mode,
		illumination,
		SUM(CASE WHEN max_severity = 'ksi' THEN crash_count ELSE 0 END) AS "KSI",
		SUM(CASE WHEN max_severity = 'non-ksi-inj' THEN crash_count ELSE 0 END) AS "Non-KSI Injury",
		SUM(CASE WHEN max_severity = 'pdo' THEN crash_count ELSE 0 END) AS "PDO",
		SUM(crash_count) AS "Total"
	FROM (
		SELECT 
			COUNT(crn) AS crash_count,
			illumination,
			CASE
				WHEN ped_count::integer > 0 THEN 'Pedestrian-involved'
				WHEN bicycle_count::integer > 0 THEN 'Bicyclist-involved'
				ELSE 'Vehicle Occupants Only'
			END AS Mode,
			CASE
				WHEN max_severity_level = 'Property Damage Only' THEN 'pdo'
				WHEN max_severity_level IN('Fatal','Suspected Serious Injury') THEN 'ksi'
				WHEN max_severity_level IN ('Suspected Minor Injury','Possible Injury','Injury - Unknown Severity','Unknown if Injured') THEN 'non-ksi-inj'
			END AS max_severity
		FROM corridor_crashes
		GROUP BY mode, max_severity, illumination 
	) AS subquery
	GROUP BY mode, illumination
	order by mode desc, illumination"""


#number of persons involved by mode and injury severity
#from person table in main gis db; uses provided list of crns for corridor
"""select
			CASE
		WHEN cpp.person_type   IN('1', '2') THEN 'vehicle occupant'
		WHEN cpp.person_type   = '4' THEN 'bicyclist'
		WHEN cpp.person_type   = '7' THEN 'pedestrian'
		WHEN cpp.person_type   = '8' THEN 'other'
	END AS mode, 
    COUNT(CASE WHEN cpp.inj_severity = '0' THEN 1 END) AS pdo,
    COUNT(CASE WHEN cpp.inj_severity IN('1','2') THEN 1 END) AS ksi,
    COUNT(CASE WHEN cpp.inj_severity IN('3','4','8','9') THEN 1 END) AS non_ksi_inj
from crash_pa_person cpp 
where cpp.crn in ( '2020018589', 
 '2020021621', 
 '2020014758',
 '2020033970',
 '2020036516',
 '2020076163',
 '2020052692',
 '2020012506',
 '2020038909',
 '2020066032',
 '2020031109',
 '2020048580',
 '2020042580',
 '2020034734',
 '2020025043',
 '2020019724',
 '2020094542',
 '2020059570',
 '2020092160',
 '2020062300',
 '2020100187',
 '2020105672',
 '2020103742',
 '2020094791',
 '2020086525',
 '2020104806',
 '2020079635',
 '2020110055',
 '2020111759',
 '2021019330',
 '2021031564',
 '2021019337',
 '2021017478',
 '2021020194',
 '2021042848',
 '2021036928',
 '2021035865',
 '2021000641',
 '2021022069',
 '2021026276',
 '2021055405',
 '2021053451',
 '2021045557',
 '2021038576',
 '2021101296',
 '2021100826',
 '2021078890',
 '2021093475',
 '2021036587',
 '2021082142',
 '2021044910',
 '2021043838',
 '2021092397',
 '2021045000',
 '2021095621',
 '2021079246',
 '2021078570',
 '2021080149',
 '2021090117',
 '2021061345',
 '2021060590',
 '2021063717',
 '2021063533',
 '2021073376',
 '2021110509',
 '2021075362',
 '2021104629',
 '2021107241',
 '2021102244',
 '2021126708',
 '2021037721',
 '2021067397',
 '2021092772',
 '2021122248',
 '2022013300',
 '2022022569',
 '2022030398',
 '2022006989',
 '2022008199',
 '2022002488',
 '2022052122',
 '2022031985',
 '2022049803',
 '2022035436',
 '2022052107',
 '2022052382',
 '2022067278',
 '2022058918',
 '2022054421',
 '2022078205',
 '2022064647',
 '2022066025',
 '2022100264',
 '2022081044',
 '2022077421',
 '2022085564',
 '2022088956',
 '2022073266',
 '2022100846',
 '2022107836',
 '2022093074',
 '2022111235',
 '2022111708',
 '2022119313',
 '2022108918',
 '2022108631',
 '2022109683',
 '2022121786',
 '2022091924',
 '2022096154',
 '2022093491',
 '2022099202',
 '2022095505',
 '2022123735',
 '2022124718',
 '2022027480',
 '2022015633',
 '2022049078',
 '2022125127',
 '2023012798',
 '2023004059',
 '2023018231',
 '2023005879',
 '2023037997',
 '2023026937',
 '2023037015',
 '2023036671',
 '2023032503',
 '2023036262',
 '2023020715',
 '2023031307',
 '2023053461',
 '2023052818',
 '2023055790',
 '2023066592',
 '2023082202',
 '2023086729',
 '2023091402',
 '2023097677',
 '2023107902',
 '2023107792',
 '2023107190',
 '2023098133',
 '2023103406',
 '2023101914',
 '2023104684',
 '2023035501',
 '2024091940',
 '2024012540',
 '2024013950',
 '2024017964',
 '2024017585',
 '2024015094',
 '2024011198',
 '2024027516',
 '2024034058',
 '2024035209',
 '2024031270',
 '2024042856',
 '2024043635',
 '2024062686',
 '2024012069',
 '2024005457',
 '2024019592',
 '2024052271',
 '2024056843',
 '2024048250',
 '2024084147',
 '2024067011',
 '2024066778',
 '2024064334',
 '2024063860',
 '2024084664',
 '2024081257',
 '2024113483',
 '2024115729',
 '2024111162',
 '2024115736',
 '2024101016',
 '2024107604',
 '2024111612',
 '2024116023')
group by mode
order by mode desc """