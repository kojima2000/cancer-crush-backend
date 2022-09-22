# ================================================== #
#                   SCORE MODEL                   #
# ================================================== #
# Author: Aishwarya Danoji                       #
# Created: 09/22/2022                                #
# Last Edited: 09/22/2022                            #
# ================================================== #
#                                                    #
# ================================================== #

import bcrypt
import falcon
from ..config.configLoader import ConfigLoader
from ..database.setupMySqlDatabase import SetupMySqlDatabase

class Score:
    """Class defining score model"""
    def __init__(self):
        """
        Initializes score object
        """
        self.connection = SetupMySqlDatabase().getConnection();

    def get_score(self, email):
            cursor = self.connection.cursor()
            sql = "SELECT * FROM score WHERE Email = %s"
            cursor.execute(sql,(email,))
            score = cursor.fetchall()
            r = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in score]
            return r;

    def add_or_update_score(self,email,score):
         # Check for required fields
         if not email or not score :
            print("Bad Request: Missing required fields.")
            return []
         else:
            cursor = self.connection.cursor()
            cursor.execute("Select Id from Users where Email =  %s", (email,))
            userId = cursor.fetchone()
            print(userId[0])
            cursor.execute(
                    "INSERT INTO `Score`  (`User_id`,`Email`,`Score`) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE Score = %s",
                    (userId[0],email,score, score))
            self.connection.commit()
            print("Scores for user updated successfully!")

# ================================================== #
#                        EOF                         #
# ================================================== #
