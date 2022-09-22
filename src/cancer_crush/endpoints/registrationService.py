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
            raise falcon.HTTPBadRequest(description="Missing required field(s).")
        try:
            req_params = json.loads(req.stream.read())
        except:
            raise falcon.HTTPBadRequest(description="Improperly formed JSON.")
        if (not req_params or "Email" not in req_params or "Password" not in
        req_params or "First_Name" not in req_params or "Last_Name" not in
        req_params or "NPI" not in req_params or "Field" not in req_params or
        "Practice" not in req_params or "Area_Code" not in req_params):
            raise falcon.HTTPBadRequest(description="Missing required field(s).")
        else:
            # Add user to DB
            user = User().add_user(req_params["First_Name"],
                         req_params["Last_Name"],
                         req_params["Email"],
                         req_params["Password"],
                         req_params["NPI"],
                         req_params["Field"],
                         req_params["Practice"],
                         req_params["Area_Code"])

            # Check if user was successfully added
            if not user:
                raise falcon.HTTPBadRequest(description="Could not add user.")

            # Create JWT token
            current_time = datetime.utcnow()
            payload = { "user": {'Id': user[0]},
                        "iat": current_time,
                        "nbf": current_time,
                        "exp": current_time + timedelta(seconds=(8 * 60 * 60))}
            token = jwt.encode(payload=payload,
                               key=ConfigLoader().data["JWT"]["Secret"],
                               algorithm="HS256",
                               json_encoder=ExtendedJSONEncoder)

           # Return token and status
            resp.media = {
                "access_token": token,
                "user_id": user[0]
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
