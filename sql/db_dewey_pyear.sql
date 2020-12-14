SELECT ref as sku, type as dewey, printingyear as printing_year 
FROM db_lelivre_pro.livresv2 
-- INTO OUTFILE 'C:\Adrian - GDrive\Professionnel\Formation\Informatique - Digital\Data University\Projet certification\src\db_dewey_pyear.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';