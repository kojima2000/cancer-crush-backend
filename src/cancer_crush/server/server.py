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
from falcon_auth import FalconAuthMiddleware, JWTAuthBackend
from ..config.config_loader import ConfigLoader
from ..database.setupMySqlDatabase import SetupMySqlDatabase
from ..endpoints.quizQuestions import QuizQuestions

class TestResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override
        resp.text = ('Test Endpoint')

def start_server(socket="", port=8080):
    config = ConfigLoader()
    mySql_db = SetupMySqlDatabase();
    user_loader = lambda username, password: { 'username': username }
    jwt_auth = JWTAuthBackend(user_loader, ConfigLoader().data['JWT']['Secret'])

    auth_middleware = FalconAuthMiddleware(jwt_auth, exempt_routes=['/test', '/login', '/questions'])
    app = falcon.App(middleware=[auth_middleware])
    mySql_db.setup_db()
    test = TestResource()
    questions = QuizQuestions()
    app.add_route('/test', test)
    app.add_route('/questions', questions)

    if not socket:
        serve(app, port=port)
    else:
        serve(app, unix_socket=socket)

    mySql_db.disconnect_db()

   
    

# ================================================== #
#                        EOF                         #
# ================================================== #
