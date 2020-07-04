from flask import jsonify
from flask_restful import Resource,reqparse
from models import UserModel
from models import RevokedTokenModel
from flask_jwt_extended import(create_access_token,create_refresh_token,
jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt)
parser=reqparse.RequestParser()
parser.add_argument('username',help='This field cannot be blank',required=True)
parser.add_argument('password',help='This field cannot be blank',required=True)
class UserRegistration(Resource):
    def post(self):
        data=parser.parse_args()
        new_user=UserModel(data['username'], UserModel.generate_hash(data['password']))
        if UserModel.find_username(data['username']):
            return jsonify({'Message':"{} user already exists".format(data['username'])})
        
        try:
            new_user.save_to_db()
            access_token=create_access_token(identity=data['username'])
            refresh_token=create_refresh_token(identity=data['username'])

            return jsonify(
                {"Message":"{} who is a new user has been added.".format(data['username']),
                "access_token":access_token,
                "refresh_token":refresh_token})
        except:
            return jsonify({'Message':"There was an error adding the user"})
class UserLogin(Resource):
    def post(self):
        data=parser.parse_args()
        current_user=UserModel.find_username(data['username'])
        if not current_user:
            return jsonify({"Message":"User {} not found".format(data['username'])})
        if UserModel.verify_hash(data['password'],current_user.password):
            access_token=create_access_token(identity=data['username'])
            refresh_token=create_refresh_token(identity=data['username'])
            return jsonify({'Message':'Login of user {} is successful'.format(data['username']),
            "access_token":access_token,
            "refresh_token":refresh_token})
        else:
            return jsonify({'Message':'wrong credentials'})

class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        try:
            jti=get_raw_jwt()['jti']
            revoked=RevokedTokenModel(jti)
            revoked.add()
            return {"Message":'User Logout,Token was revoked successfully'}
        except:
            return{'There was an error in revoking the token'}

class UserLogoutRefresh(Resource):
    def post(self):
        try:
            jti=get_raw_jwt()['jti']
            revoked=RevokedTokenModel(jti)
            revoked.add()
            return {"Message":'User Logout,Token was revoked successfully'}
        except:
            return{'There was an error in revoking the token'}
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user=get_jwt_identity()
        access_token=create_access_token(identity=current_user)
        return {'message':'Token Refresh',
        "access_token":access_token}
class AllUsers(Resource):
    def get(self):
        return jsonify(UserModel.return_all())
    def delete(self):
        return jsonify(UserModel.delete_all())
#this method required jwt to access pass jwt secret key to access this data.
class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {'answer':42}