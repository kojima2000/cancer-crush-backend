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
from tkinter.messagebox import QUESTION
import falcon
import msgpack
from ..database.setupMySqlDatabase import SetupMySqlDatabase
from ..model.question import Question
from mysql.connector import Error

class QuizQuestions:
    def __init__(self):
        self.connection = SetupMySqlDatabase().getConnection();

    def on_get(self, req, resp):
        try:
            r = Question().get_questions()         
            resp.text = json.dumps(r)
            resp.status = falcon.HTTP_200
        except Error as e:
            print("Error while getting questions from MySql", e)

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
                           
            patient_age = self.validate_string(req_params["Patient_age"])
            patient_sex = self.validate_string(req_params["Patient_sex"])
            question = self.validate_string(req_params["Question"])
            patient_history = self.validate_string(req_params["Patient_history"])
            correct_answer =  self.validate_string(req_params["Correct_answer"])
            choice_A =  self.validate_string(req_params["Choice_A"])
            choice_B =  self.validate_string(req_params["Choice_B"])
            choice_C =  self.validate_string(req_params["Choice_C"])
            choice_D =  self.validate_string(req_params["Choice_D"])
            answer_details = self.validate_string(req_params["Answer_details"])
            # Add question to DB
            Question().add_question(
                        patient_age,patient_sex,question,patient_history,correct_answer,choice_A,choice_B,choice_C,choice_D,answer_details)

            resp.text=("Inserted into the database")
            resp.status = falcon.HTTP_200
 
   
    # do validation and checks before insert
    def validate_string(self,val):
        if val != None:
            if type(val) is int:
                #for x in val:
                #   print(x)
                return str(val).encode('utf-8')
            else:
                return val
# ================================================== #
#                        EOF                         #
# ================================================== #
