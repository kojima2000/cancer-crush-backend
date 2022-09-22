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
from falcon_auth.serializer import ExtendedJSONEncoder
from ..config.configLoader import ConfigLoader
from ..model.user import User
from datetime import timedelta, datetime

class LoginService:
    """Class defining login endpoint"""
    def __init__(self):
        pass

    def login(self, req, resp):
        """
        Logs an existing user in the database
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

        if not req_params or "Email" not in req_params or "Password" not in req_params:
            raise falcon.HTTPBadRequest(description="Please enter a valid email and password.")
        else:
            # Authenticate user
            self._authenticate(req_params["Email"], req_params["Password"], req, resp)

    def _authenticate(self, email, password, req, resp):
        """
        Authenticates a user using the provided credentials
        :param email: user provided email
        :param password: user provided password
        :param req: HTTP request
        :param resp: HTTP response
        """
        # Validate fields
        if not email or not password:
            raise falcon.HTTPBadRequest(description="Please enter a valid email and password.")
        else:
            # Verify user exists
            user = User().get_user(email, password)
            if not user:
                raise falcon.HTTPUnauthorized(description="The password you entered was incorrect. Please try again.")

            # Generate JWT token
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
        POST endpoint for login
        :param req: HTTP request
        :param resp: HTTP response
        """
        self.login(req, resp)

# ================================================== #
#                        EOF                         #
# ================================================== #
