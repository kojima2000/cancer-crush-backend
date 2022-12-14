# ================================================== #
#                  SCORE SERVICE                    #
# ================================================== #
# Author: Aishwarya Danoji                              #
# Created: 09/22/2022                                #
# Last Edited: 09/22/2022                            #
# ================================================== #
#                                                    #
# ================================================== #

import json
from tkinter.messagebox import QUESTION
import falcon
import msgpack
from ..database.setupMySqlDatabase import SetupMySqlDatabase
from ..model.score import Score
from mysql.connector import Error

class ScoreService:
    def __init__(self):
        self.connection = SetupMySqlDatabase().getConnection();

    def on_get(self, req, resp):
        try:
            req_params = json.loads(req.stream.read())
            email = self.validate_string(req_params["Email"])
            r = Score().get_score(email)
            if r:
                resp.text = json.dumps(r)
                resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_500
        except Error as e:
            print("Error: Could not retrieve scores", e)
            resp.status = falcon.HTTP_500

    def on_post(self, req, resp):
        if not req:
            raise falcon.HTTPBadRequest(description="Missing required field(s).")
        try:
            req_params = json.loads(req.stream.read())
        except:
            raise falcon.HTTPBadRequest(description="Improperly formed JSON.")
        if (not req_params ):
            raise falcon.HTTPBadRequest(description="Missing required field(s).")
        else:
            email = self.validate_string(req_params["Email"])
            score = self.validate_string(req_params["Score"])
            # Add score to DB
            if Score().add_or_update_score(email, score):
                resp.text=("Inserted score into the database")
                resp.status = falcon.HTTP_200
            else:
                resp.text=("Error: Could not add scores")
                resp.status = falcon.HTTP_500

    # do validation and checks before insert
    def validate_string(self,val):
        if val != None:
            if type(val) is int:
                return str(val).encode('utf-8')
            else:
                return val
# ================================================== #
#                        EOF                         #
# ================================================== #
