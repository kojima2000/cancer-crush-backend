# ================================================== #
#                     DATABASE SETUP                 #
# ================================================== #
# Author: Aishwarya Danoji                           #
# Created: 09/20/2022                                #
# Last Edited: 09/20/2022                            #
# ================================================== #
#                                                    #
# ================================================== #

import jwt
import json
import falcon
from falcon_auth.serializer import ExtendedJSONEncoder
from ..config.configLoader import ConfigLoader
from datetime import timedelta, datetime
import mysql.connector
from mysql.connector import Error
import os, json

class SetupMySqlDatabase:
    def __init__(self):
        self.connection = mysql.connector.connect(host= ConfigLoader().data['Database']['Host'],
                                             user=ConfigLoader().data['Database']['Username'],
                                             password=ConfigLoader().data['Database']['Password'])

    def setup_db(self):
        try:
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version:", db_Info)
                cursor = self.connection.cursor()
                self.create_database(cursor)
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("Connected to database:", record[0])

                mySql_Create_Table_QuizQuestions = """CREATE TABLE IF NOT EXISTS QuizQuestions (
                                 Id INT NOT NULL AUTO_INCREMENT,
                                 Patient_history VARCHAR(512) ,
                                 Patient_age SMALLINT ,
                                 Patient_sex VARCHAR(32),
                                 Question VARCHAR(256) NOT NULL,
                                 Correct_answer VARCHAR(16) NOT NULL,
                                 Answer_details VARCHAR(1024) NOT NULL,
                                 Choice_A VARCHAR(256),
                                 Choice_B VARCHAR(256),
                                 Choice_C VARCHAR(256),
                                 Choice_D VARCHAR(256),
                                 PRIMARY KEY (Id));"""

                mySql_Create_Table_Users = """CREATE TABLE IF NOT EXISTS Users (
                                 Id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                 First_Name VARCHAR(64) NOT NULL,
                                 Last_Name VARCHAR(64) NOT NULL,
                                 Email VARCHAR(128) NOT NULL UNIQUE,
                                 Password VARCHAR(256) NOT NULL,
                                 NPI VARCHAR(32) NOT NULL,
                                 Field VARCHAR(64) NOT NULL,
                                 Practice VARCHAR(128) NOT NULL,
                                 Area_Code MEDIUMINT NOT NULL,
                                 UNIQUE (email));"""

                mySql_Create_Table_Progress = """CREATE TABLE IF NOT EXISTS Progress (
                                 Id INT NOT NULL AUTO_INCREMENT,
                                 User_id INT NOT NULL,
                                 Question_id INT NOT NULL,
                                 Status BIT NOT NULL,
                                 PRIMARY KEY (Id),
                                 FOREIGN KEY (User_id) REFERENCES Users (Id),
                                 FOREIGN KEY (Question_id) REFERENCES QuizQuestions (Id));"""

                mySql_Create_Table_Score = """CREATE TABLE IF NOT EXISTS Score (
                                 Id int(11) NOT NULL AUTO_INCREMENT,
                                 User_id int(11) NOT NULL,
                                 Email varchar(256) NOT NULL,
                                 Score int(11) NOT NULL,
                                 UNIQUE (email),
                                 PRIMARY KEY (Id),
                                 FOREIGN KEY (User_id) REFERENCES Users (Id));"""

                cursor.execute(mySql_Create_Table_QuizQuestions)
                cursor.execute(mySql_Create_Table_Users)
                cursor.execute(mySql_Create_Table_Score)
                cursor.execute(mySql_Create_Table_Progress)

                cursor.execute("USE {};".format(ConfigLoader().data['Database']['Name']))
                cursor.execute("SELECT * FROM QuizQuestions")
                if not cursor.fetchall():
                    with open("src\cancer_crush\config\questions.json") as question_file:
                        json_obj = json.loads(question_file.read(), strict=False)
                        for i, item in enumerate(json_obj):
                            patient_age = self.validate_string(item.get("Patient_age", None))
                            patient_sex = self.validate_string(item.get("Patient_sex", None))
                            question = self.validate_string(item.get("Question", None))
                            patient_history = self.validate_string(item.get("History", None))
                            correct_answer =  self.validate_string(item.get("Correct_answer", None))
                            choice_A =  self.validate_string(item.get("Choice_A", None))
                            choice_B =  self.validate_string(item.get("Choice_B", None))
                            choice_C =  self.validate_string(item.get("Choice_C", None))
                            choice_D =  self.validate_string(item.get("Choice_D", None))
                            answer_details = self.validate_string(item.get("Answer_details", None))
                            try:
                                cursor.execute("INSERT INTO `QuizQuestions`  (`Patient_age`,`Patient_sex`,`Question`,`Patient_history`,`Correct_answer`,`Choice_A`, `Choice_B`,`Choice_C`,`Choice_D`,`Answer_details`) VALUES (%s,	%s,	%s, %s, %s, %s, %s, %s, %s, %s);",
                                (patient_age,patient_sex,question,patient_history,correct_answer,choice_A,choice_B,choice_C,choice_D,answer_details))
                            except:
                                print("Could not pre-populate QuizQuestions table")
                    self.connection.commit()
                    print("Questions table pre-populated")

        except Error as e:
            print("Error: MySQL setup failed", e)

    def create_database(self, cursor):
        database_name = ConfigLoader().data['Database']['Name']
        try:
            cursor.execute("CREATE DATABASE IF NOT EXISTS {};".format(database_name))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))

        try:
            self.connection.database = database_name
        except mysql.connector.Error as err:
            print("Database {} does not exists".format(database_name))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                create_database(cursor)
                print("Database {} created successfully".format(database_name))
                self.connection.database = database_name
            else:
                print(err)

    def getConnection(self):
        return self.connection

    def disconnect_db(self):
        if self.connection.is_connected():
            self.connection.cursor().close()
            self.connection.close()
            print("Database connection terminated")

    def validate_string(self,val):
        if val != None:
            if type(val) is int:
                return str(val).encode('utf-8')
            else:
                return val

# ================================================== #
#                        EOF                         #
# ================================================== #
