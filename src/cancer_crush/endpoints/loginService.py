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
from ..config.config_loader import ConfigLoader
from datetime import timedelta, datetime

class LoginService:
    def __init__(self):
        pass

    def login(self, req, resp):
        req_params = json.loads(req.stream.read())

        if not req_params or not req_params["Username"] or not req_params["Password"]:
            raise falcon.HTTPBadRequest("Bad Request", "Please enter valid username and password.")
        else:
            self._authenticate(req_params["Username"], req_params["Password"], req, resp)

    def _authenticate(self, username, password, req, resp):
        if not username or not password:
            raise falcon.HTTPBadRequest("Bad Request", "Please enter valid username and password.")
        else:
            # TODO: DB connection and user verification

            current_time = datetime.utcnow()
            payload = { "user_id": "RETRIEVED USER ID",
                        "iat": current_time,
                        "nbf": current_time,
                        "exp": current_time + (24 * 60 * 60)}
            token = jwt.encode(payload=payload,
                               key=ConfigLoader()["JWT"]["Secret"],
                               algorithm="HS256",
                               json_encoder=ExtendedJSONEncoder)
            resp.media = {
                "JWT token": token.decode("utf-8")
            }
            resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        self.login(req, resp)

# ================================================== #
#                        EOF                         #
# ================================================== #
