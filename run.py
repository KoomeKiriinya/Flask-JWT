# import the required files
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
app= Flask(__name__)
#set 
app.config['JWT_SECRET_STRING']='jwt_secret_string'
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
app.config['SECRET_KEY'] ="Secret_key"
app.config['JWT_BLACKLIST_ENABLED']=True
app.config['JWT_BLACKLIST_TOKEN_CHECKS']=['access','refresh']
jwt=JWTManager(app)
db=SQLAlchemy(app)
@jwt.token_in_blacklist_loader
def check_in_blacklist(decrypted_token):
    jti=decrypted_token['jti']
    return models.RevokedTokenModel.jti_is_blacklist(jti)

@app.before_first_request
def create_tables():
    db.create_all()

api=Api(app)
import views,resources,models
#add the required endpoints which are in resources.py
api.add_resource(resources.UserRegistration,"/registration")
api.add_resource(resources.UserLogin,"/login")
api.add_resource(resources.UserLogoutAccess,"/logout/access")
api.add_resource(resources.UserLogoutRefresh,"/logout/refresh")
api.add_resource(resources.TokenRefresh,"/token/refresh")
api.add_resource(resources.AllUsers,"/users")
api.add_resource(resources.SecretResource,"/secret")

