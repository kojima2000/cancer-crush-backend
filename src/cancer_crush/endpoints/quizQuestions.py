# ================================================== #
#                  QUIZ QUESTIONS                    #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 09/20/2022                                #
# Last Edited: 09/21/2022                            #
# ================================================== #
#                                                    #
# ================================================== #

import json
import falcon
import msgpack
from ..database.setupMySqlDatabase import SetupMySqlDatabase
from mysql.connector import Error

class QuizQuestions:
    def __init__(self):
        self.connection = SetupMySqlDatabase().getConnection();

    def on_get(self, req, resp):
        curs = self.connection.cursor()
        try:
            curs.execute("SELECT * FROM quizQuestions")
            record = curs.fetchall()
            r = [dict((curs.description[i][0], value) \
               for i, value in enumerate(row)) for row in record]
            resp.text = json.dumps(r)
            resp.status = falcon.HTTP_200
        except Error as e:
            print("Error while getting questions from MySql", e)

# ================================================== #
#                        EOF                         #
# ================================================== #
