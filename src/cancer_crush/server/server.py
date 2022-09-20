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
import mysql.connector
from mysql.connector import Error

class TestResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override
        resp.text = ('Test Endpoint')
        return resp

class QuizQuestion:
    def on_get(self, req, resp):
        connection = connect_db()

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override
        resp.text = ('Question Endpoint')

def connect_db():
    return  mysql.connector.connect(host='localhost',
                                             database=' CancerCrush',
                                             user='root',
                                             password='Microsoft123$')
def setup_db():
    try:
        connection = connect_db()

        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

            mySql_Create_Table_Query = """CREATE TABLE QuizQuestion ( 
                             Id int(11) NOT NULL,
                             Patient_history varchar(250) NOT NULL,
                             Patient_age int(11) NOT NULL,
                             Patient_sex varchar(250) NOT NULL,
                             Question varchar(250) NOT NULL,
                             Correct_answer varchar(250) NOT NULL,
                             Incorrect_answer_A varchar(250) NOT NULL,
                             Incorrect_answer_B varchar(250) NOT NULL,
                             Incorrect_answer_C varchar(250) NOT NULL,
                             PRIMARY KEY (Id)) """

            cursor = connection.cursor()
            result = cursor.execute(mySql_Create_Table_Query)
            print("QuizQuestion Table created successfully ")
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)

def end_db(connection):
    if connection.is_connected():
        connection.cursor().close()
        connection.close()
        print("MySQL connection is closed")

def start_server(socket="", port=8080):
    config = ConfigLoader()
    user_loader = lambda username, password: { 'username': username }
    jwt_auth = JWTAuthBackend(user_loader, ConfigLoader().data['JWT']['Secret'])

    auth_middleware = FalconAuthMiddleware(jwt_auth, exempt_routes=['/test', '/login'])
    app = falcon.App(middleware=[auth_middleware])
    connection = setup_db()
    test = TestResource()
    questions = QuizQuestion()
    app.add_route('/test', test)
    app.add_route('/questions', questions)

    if not socket:
        serve(app, port=port)
    else:
        serve(app, unix_socket=socket)

    end_db(connection)

   
    

# ================================================== #
#                        EOF                         #
# ================================================== #
