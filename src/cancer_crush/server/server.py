# ================================================== #
#                      SERVER                        #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 09/20/2022                                #
# Last Edited: 09/20/2022                            #
# ================================================== #
#                                                    #
# ================================================== #

from waitress import serve
import falcon

class TestResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override
        resp.text = ('Test Endpoint')

def start_server(socket="", port=8080):
    app = falcon.App()
    test = TestResource()
    app.add_route('/test', test)

    if not socket:
        serve(app, port=port)
    else:
        serve(app, unix_socket=socket)


# ================================================== #
#                        EOF                         #
# ================================================== #
