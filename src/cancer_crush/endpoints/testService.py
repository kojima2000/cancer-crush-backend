# ================================================== #
#                    TEST SERVICE                    #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 09/20/2022                                #
# Last Edited: 09/21/2022                            #
# ================================================== #
#                                                    #
# ================================================== #

import falcon

class TestService:
    """Class defining test endpoint"""
    def __init__(self):
        pass

    def on_get(self, req, resp):
        """
        Handles GET requests to test endpoint.
        :param req: HTTP request
        :param resp: HTTP response
        """
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = ('Test Endpoint')

# ================================================== #
#                        EOF                         #
# ================================================== #
