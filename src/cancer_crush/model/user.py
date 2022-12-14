# ================================================== #
#                     USER MODEL                     #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 09/21/2022                                #
# Last Edited: 09/21/2022                            #
# ================================================== #
#                                                    #
# ================================================== #

import bcrypt
import falcon
from ..config.configLoader import ConfigLoader
from ..database.setupMySqlDatabase import SetupMySqlDatabase

class User:
    """Class defining user model"""
    def __init__(self):
        """
        Initializes User object
        """
        self.connection = SetupMySqlDatabase().getConnection();

    def get_user(self, email, password):
        """
        Retrieves user data and authenticates the user
        :param email: user email
        :param password: user password
        """
        # Get user data and authenticate user
        try:
            cursor = self.connection.cursor()
            db_query = "USE {};".format(ConfigLoader().data['Database']['Name'])
            cursor.execute(db_query)
            cursor.execute("SELECT * FROM Users WHERE Email='{email}'".format(email=email))
            user = cursor.fetchone()
            if user is None:
                print ("Bad Request: User not found.")
                return []
            elif not bcrypt.checkpw(password.encode("utf-8"), user[4].encode("utf-8")):
                return []
            else:
                return user
        except:
            print("Could not retrieve user")
            return []

    def add_user(self,
                 first_name,
                 last_name,
                 email,
                 password,
                 npi,
                 field,
                 practice,
                 area_code
                 ):
         """
         Adds a new user to the database
         :param first_name: user first name
         :param last_name: user last name
         :param email: user email
         :param password: user password
         :param npi: user NPI number
         :param field: user field of study
         :param practice: user medical practice
         :param area_code: user area code
         """
         try:
            # Verify user email not already in use (DB should already enforce unique status, but we still check just in case)
            cursor = self.connection.cursor()
            db_query = "USE {};".format(ConfigLoader().data['Database']['Name'])
            cursor.execute(db_query)
            cursor.execute("SELECT Email FROM Users")
            emails = cursor.fetchall()

            if email in [x[0] for x in emails]:
                print("User with that email already exists")
                return []

            # Hash password for storage
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)

            # Add user to DB
            query = "INSERT INTO Users (First_Name, Last_Name, Email, Password, NPI, Field, Practice, Area_Code) VALUES ('{first_name}', '{last_name}', '{email}', '{password}', '{npi}', '{field}', '{practice}', {area_code})".format(
            first_name=first_name, last_name=last_name,
            email=email, password=password_hash.decode("utf-8"), npi=npi, field=field,
            practice=practice, area_code=area_code)
            cursor.execute(query)
            self.connection.commit()
            print("New user added")
            cursor.execute("SELECT Id FROM Users WHERE Email='{email}'".format(email=email))
            return cursor.fetchone()
         except:
            print("Could not add user")
            return []

# ================================================== #
#                        EOF                         #
# ================================================== #
