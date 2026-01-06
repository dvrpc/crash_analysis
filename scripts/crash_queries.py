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
	
