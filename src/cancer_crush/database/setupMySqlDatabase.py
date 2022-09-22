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
                                             database=ConfigLoader().data['Database']['Name'],
                                             user=ConfigLoader().data['Database']['Username'],
                                             password=ConfigLoader().data['Database']['Password'])

    def setup_db(self):
        try:
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = self.connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)

                mySql_Create_Table_QuizQuestions = """CREATE TABLE IF NOT EXISTS QuizQuestions (
                                 Id int(11) NOT NULL AUTO_INCREMENT,
                                 Patient_history varchar(500) ,
                                 Patient_age int(11) ,
                                 Patient_sex varchar(250),
                                 Question varchar(250) NOT NULL,
                                 Correct_answer varchar(12) NOT NULL,
                                 Answer_details varchar(1000) NOT NULL,
                                 Choice_A varchar(250),
                                 Choice_B varchar(250),
                                 Choice_C varchar(250),
                                 Choice_D varchar(250),
                                 PRIMARY KEY (Id)) """

                mySql_Create_Table_Users = """CREATE TABLE IF NOT EXISTS Users (
                                 Id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                 First_Name varchar(256) NOT NULL,
                                 Last_Name varchar(256) NOT NULL,
                                 Email varchar(256) NOT NULL UNIQUE,
                                 Password varchar(256) NOT NULL,
                                 NPI varchar(256) NOT NULL,
                                 Field varchar(256) NOT NULL,
                                 Practice varchar(256) NOT NULL,
                                 Area_Code int(11) NOT NULL,
                                 UNIQUE (email)) """

                mySql_Create_Table_Progress = """CREATE TABLE IF NOT EXISTS Progress (
                                 Id int(11) NOT NULL AUTO_INCREMENT,
                                 User_id int(11) NOT NULL,
                                 Question_id int(11) NOT NULL,
                                 Status varchar(2) NOT NULL,
                                 PRIMARY KEY (Id),
                                 FOREIGN KEY (User_id) REFERENCES Users (Id),
                                 FOREIGN KEY (Question_id) REFERENCES QuizQuestions (Id)) """

                mySql_Create_Table_Score = """CREATE TABLE IF NOT EXISTS Score (
                                 Id int(11) NOT NULL AUTO_INCREMENT,
                                 User_id int(11) NOT NULL,
                                 Score int(11) NOT NULL,
                                 PRIMARY KEY (Id),
                                 FOREIGN KEY (User_id) REFERENCES Users (Id)) """

                cursor.execute(mySql_Create_Table_QuizQuestions)
                cursor.execute(mySql_Create_Table_Users)
                cursor.execute(mySql_Create_Table_Score)
                cursor.execute(mySql_Create_Table_Progress)


        except Error as e:
            print("Error while setting up MySQL", e)



    def getConnection(self):
        return self.connection



    def disconnect_db(self):
        if self.connection.is_connected():
            self.connection.cursor().close()
            self.connection.close()
            print("MySQL connection is closed")

# ================================================== #
#                        EOF                         #
# ================================================== #
