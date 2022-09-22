# ================================================== #
#                 PROGRESS SERVICE                   #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 09/20/2022                                #
# Last Edited: 09/20/2022                            #
# ================================================== #
#                                                    #
# ================================================== #

import json
import falcon
from ..config.configLoader import ConfigLoader
from ..model.progress import Progress

class ProgressService:
    """Class defining login endpoint"""
    def __init__(self):
        pass

    def on_post(self, req, resp):
        """
        POST endpoint for user progress
        :param req: HTTP request
        :param resp: HTTP response
        """
        if not req:
            raise falcon.HTTPBadRequest(description="Missing required field(s).")
        try:
            req_params = json.loads(req.stream.read())
        except:
            raise falcon.HTTPBadRequest(description="Improperly formed JSON.")

        if not req_params or "User_Id" not in req_params or "Question_Id" not in req_params or "Status" not in req_params:
            raise falcon.HTTPBadRequest(description="Missing required field(s).")
        else:
            if Progress().add_progress(req_params["User_Id"], req_params["Question_Id"], req_params["Status"]):
                resp.status = falcon.HTTP_200
            else:
                print("Error: Could not add progress")
                resp.status = falcon.HTTP_500

    def on_get(self, req, resp):
        """
        GET endpoint for user progress
        :param req: HTTP request
        :param resp: HTTP response
        """
        if not req:
            raise falcon.HTTPBadRequest(description="Missing required field(s).")
        try:
            req_params = json.loads(req.stream.read())
        except:
            raise falcon.HTTPBadRequest(description="Improperly formed JSON.")

        if not req_params or "User_Id" not in req_params:
            raise falcon.HTTPBadRequest(description="Missing User ID.")
        else:
            progress = Progress().get_progress(req_params["User_Id"])
            if progress:
                resp.text = json.dumps(progress)
                resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_500

# ================================================== #
#                        EOF                         #
# ================================================== #
