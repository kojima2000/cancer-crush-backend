# ================================================== #
#               REGISTRATION SERVICE                 #
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
from falcon_auth.serializer import ExtendedJSONEncoder
from ..config.configLoader import ConfigLoader
from ..model.user import User
from datetime import timedelta, datetime

class RegistrationService:
    """Class defining registration endpoint"""
    def __init__(self):
        pass

    def register(self, req, resp):
        """
        Registers a new user in the database
        :param req: HTTP request
        :param resp: HTTP response
        """
        # Read in the request and validate fields
        if not req:
            raise falcon.HTTPBadRequest("Bad Request", "Missing required field(s).")
        req_params = json.loads(req.stream.read())
        if (not req_params or not req_params["Email"] or not req_params["Password"]
        or not req_params["First_Name"] or not req_params["Last_Name"]
        or not req_params["NPI"] or not req_params["Field"]
        or not req_params["Practice"] or not req_params["Area_Code"]):
            raise falcon.HTTPBadRequest("Bad Request", "Missing required field(s).")
        else:
            # Add user to DB
            self._authenticate(req_params["Email"], req_params["Password"], req, resp)
            User().add_user(req_params["First_Name"],
                         req_params["Last_Name"],
                         req_params["Email"],
                         req_params["Password"],
                         req_params["NPI"],
                         req_params["Field"],
                         req_params["Practice"],
                         req_params["Area_Code"])

            # Create JWT token
            current_time = datetime.utcnow()
            payload = { "user": {'Email': email, 'Password': password},
                        "iat": current_time,
                        "nbf": current_time,
                        "exp": current_time + timedelta(seconds=(8 * 60 * 60))}
            token = jwt.encode(payload=payload,
                               key=ConfigLoader().data["JWT"]["Secret"],
                               algorithm="HS256",
                               json_encoder=ExtendedJSONEncoder)

           # Return token and status
            resp.media = {
                "access_token": token
            }
            resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        """
        POST endpoint for registration
        :param req: HTTP request
        :param resp: HTTP response
        """
        self.register(req, resp)

# ================================================== #
#                        EOF                         #
# ================================================== #
