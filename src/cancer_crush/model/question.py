# ================================================== #
#                   QUESTION MODEL                   #
# ================================================== #
# Author: Niharika Tippabhatla                       #
# Created: 09/21/2022                                #
# Last Edited: 09/21/2022                            #
# ================================================== #
#                                                    #
# ================================================== #

from ..config.configLoader import ConfigLoader
from ..database.setupMySqlDatabase import SetupMySqlDatabase

class Question:
    """Class defining question model"""
    def __init__(self):
        """
        Initializes question object
        """
        self.connection = SetupMySqlDatabase().getConnection();

    def get_questions(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("USE {};".format(ConfigLoader().data['Database']['Name']))
            cursor.execute("SELECT * FROM QuizQuestions" )
            questions = cursor.fetchall()
            return [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in questions]
        except:
            print("Could not retrieve questions")
            return []

    def add_question (self,patient_age,patient_sex,question,patient_history,correct_answer,choice_A,choice_B,choice_C,choice_D,answer_details):
        try:
            cursor = self.connection.cursor()
            cursor.execute("USE {};".format(ConfigLoader().data['Database']['Name']))
            cursor.execute(
                "INSERT INTO `QuizQuestions`  (`Patient_age`,`Patient_sex`,`Question`,`Patient_history`,`Correct_answer`,`Choice_A`, `Choice_B`,`Choice_C`,`Choice_D`,`Answer_details`) VALUES (%s,	%s,	%s, %s, %s, %s, %s, %s, %s, %s)",
                (patient_age,patient_sex,question,patient_history,correct_answer,choice_A,choice_B,choice_C,choice_D,answer_details))
            self.connection.commit()
            return True
        except:
            print("Could not add question")
            return False

# ================================================== #
#                        EOF                         #
# ================================================== #
