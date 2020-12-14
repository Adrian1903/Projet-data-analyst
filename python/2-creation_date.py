# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 21:05:53 2020

@author: rodri

Problème : Il existe qu'une date, qui est mise à jour à chaque modification. Il faut reconstruire la date de création.
Hypothèse : Avec un fiche sur 5 dont la date a été modifié, il est possible de reconstruire la date de création de la fiche à partir des références voisines

STEP 1 : Creation date rebuilt
a. Création de la colonne créationDate en base (ALTER TABLE `db_lelivre_pro`.`livresv2` ADD COLUMN `CreationDate` INT(10) UNSIGNED NULL AFTER `Binding`)
b. Création d'une plage de référence autour d'une référence cible
c. Récupération de la date la plus fréquente (ou la date minimale)
d. Intégration de la valeur dans CreationDate dans la base de données
"""


import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host='***',
                                         database='***',
                                         user='***',
                                         password='***',
                                         port='***')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.execute("SELECT ref, date, creationdate FROM db_lelivre_pro.livresv2 where length(date) = 8 order by ref desc;")
        #cursor.execute("SELECT ref, date, creationdate FROM db_lelivre_pro.livresv2 where length(date) = 8 and CreationDate IS NULL order by ref desc;")
        dataset = cursor.fetchall()
        # Pour chacune des références, je vais chercher en base la date de création en explorant les références avant et après
        print("GO !")
        for line in dataset:
            ref = line[0]

            ###### PHASE 1 ###### CONSTRUCTION DES REFERENCES MIN ET MAX / Conversion String -> integer -> string
            nb = int(ref[-7:])
            nb_max = str(nb + 40)
            nb_min = nb - 5
            # Je choisis un nb_min faible pour limiter le décalage de 1 jour sur les références de début de journée 
            # (Dû à la sélection MIN() de la seconde requête)
            if nb_min < 0:
                nb_min = str(0)
            else: nb_min = str(nb_min)
            # Je recompose les zéros disparus au passage en integer
            for i in range(7 - len(nb_max)):
                nb_max = "0" + nb_max
            for i in range(7 - len(nb_min)):
                nb_min = "0" + nb_min
            # Je remonte les reférences
            ref_max = ref[:3] + nb_max
            ref_min = ref[:3] + nb_min

            ###### PHASE 2 ###### EXTRACTION DE LA DATE MINIMALE
            cursor.execute("SELECT MIN(date) FROM db_lelivre_pro.livresv2 where ref > \"" + ref_min + "\" and ref < \"" + ref_max + "\"")
            line2 = cursor.fetchone()

            ###### PHASE 3 ###### MISE A JOUR DE CREATIONDATE
            cursor.execute("UPDATE `db_lelivre_pro`.`livresv2` SET `CreationDate` = '" + str(line2[0]) + "' WHERE (`REF` = '" + ref + "');")
        cursor.close()
        connection.close()
        print("MySQL connection is closed")