SELECT 'table_name', 'table_columns', 'table_rows'
UNION ALL
	SELECT INFORMATION_SCHEMA.TABLES.table_name, count(column_name), INFORMATION_SCHEMA.TABLES.table_rows
	FROM INFORMATION_SCHEMA.TABLES 
	JOIN INFORMATION_SCHEMA.COLUMNS on INFORMATION_SCHEMA.COLUMNS.TABLE_NAME = INFORMATION_SCHEMA.TABLES.TABLE_NAME
	WHERE INFORMATION_SCHEMA.COLUMNS.table_schema = 'db_lelivre_pro'
	GROUP BY table_name
	-- INTO OUTFILE 'C:/Adrian - GDrive/Formation/Informatique - Digital/Data University/Projet certification/LVDL/db_information.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';