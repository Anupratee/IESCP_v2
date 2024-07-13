from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from connectora.models import db, User, user_schema, users_schema, Influencer, influencers_schema, bcrypt
from connectora.models import Sponsor, sponsors_schema, Campaign, campaigns_schema, Ad, ads_schema, Category, categories_schema

usersAPI = Blueprint("usersAPI", __name__)

@usersAPI.route("/users", methods = ['GET'])
def get_all_users():
    users = User.query.all()
    users_output = users_schema.dump(users)

    return jsonify({"users": users_output}), 200