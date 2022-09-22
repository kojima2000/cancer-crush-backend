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
from ..config.configLoader import ConfigLoader
from ..database.setupMySqlDatabase import SetupMySqlDatabase
from ..endpoints.quizQuestions import QuizQuestions
from ..endpoints.loginService import LoginService
from ..endpoints.registrationService import RegistrationService
from ..endpoints.testService import TestService
from ..endpoints.progressService import ProgressService

def start_server(socket="", port=8080):
    """
    Function to serve up API via waitress WSGI server
    :param socket: specifies a UNIX socket to serve API on
    :param port: specifies port to serve API on
    """
    # Load config and DB
    config = ConfigLoader().data
    mySql_db = SetupMySqlDatabase();
    mySql_db.setup_db()

    # Setup middleware
    user_loader = lambda id: { 'Id': id }
    jwt_auth = JWTAuthBackend(user_loader, config['JWT']['Secret'])
    auth_middleware = FalconAuthMiddleware(jwt_auth, exempt_routes=['/test', '/login', '/register'])
    app = falcon.App(middleware=[auth_middleware])

    # Setup endpoints
    test = TestService()
    questions = QuizQuestions()
    login = LoginService()
    register = RegistrationService()
    progress = ProgressService()
    app.add_route('/test', test)
    app.add_route('/questions', questions)
    app.add_route('/login', login)
    app.add_route('/register', register)
    app.add_route('/progress', progress)

    # Serve up API
    if not socket:
        serve(app, port=port)
    else:
        serve(app, unix_socket=socket)

    mySql_db.disconnect_db()

# ================================================== #
#                        EOF                         #
# ================================================== #
