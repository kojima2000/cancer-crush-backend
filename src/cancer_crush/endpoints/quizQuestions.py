# ================================================== #
#                   LOGIN SERVICE                    #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 09/20/2022                                #
# Last Edited: 09/20/2022                            #
# ================================================== #
#                                                    #
# ================================================== #

import jwt
import json
import falcon
import msgpack
from falcon_auth.serializer import ExtendedJSONEncoder
from ..config.config_loader import ConfigLoader
from ..database.setupMySqlDatabase import SetupMySqlDatabase
from datetime import timedelta, datetime
from mysql.connector import Error

class QuizQuestions:
    def __init__(self):
        self.connection = SetupMySqlDatabase().getConnection();

    def on_get(self, req, resp):
        curs = self.connection.cursor()
        try:
            curs.execute("SELECT * FROM quizQuestions")
            result = curs.fetchall()
            resp.data = msgpack.packb(result, use_bin_type=True)
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_200
        except Error as e:
            print("Error while getting questions from MySql", e)
        
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override
        resp.text = ('Question Endpoint')

# ================================================== #
#                        EOF                         #
# ================================================== #
