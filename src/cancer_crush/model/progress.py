# ================================================== #
#                   PROGRESS MODEL                   #
# ================================================== #
# Author: Niharika Tippabhatla                       #
# Created: 09/21/2022                                #
# Last Edited: 09/21/2022                            #
# ================================================== #
#                                                    #
# ================================================== #

from ..config.configLoader import ConfigLoader
from ..database.setupMySqlDatabase import SetupMySqlDatabase

class Progress:
    """Class defining progress model"""
    def __init__(self):
        """
        Initializes progress object
        """
        self.connection = SetupMySqlDatabase().getConnection();

    def get_progress(self, user_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("USE {};".format(ConfigLoader().data['Database']['Name']))
            cursor.execute("SELECT * FROM Progress WHERE User_id='{}'".format(user_id))
            progress = cursor.fetchall()
            return [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in progress]
        except:
            print("Could not retrieve progress")
            return []

    def add_progress(self, user_id, question_id, status):
        if not user_id or not question_id or not status:
           print("Bad Request: Missing required field(s)")
           return False
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Progress WHERE User_Id={user_id} AND Question_Id={question_id}"
            .format(user_id=user_id, question_id=question_id))
            exists = cursor.fetchall()
            if exists:
                print("Progress for question already exists")
                return False
            cursor.execute("USE {};".format(ConfigLoader().data['Database']['Name']))
            cursor.execute(
                "INSERT INTO Progress (User_Id, Question_Id, Status) VALUES ({user_id}, {question_id}, {status})"
                .format(user_id=user_id, question_id=question_id, status=status))
            self.connection.commit()
            return True
        except:
            print("Could not add progress")
            return False

# ================================================== #
#                        EOF                         #
# ================================================== #
