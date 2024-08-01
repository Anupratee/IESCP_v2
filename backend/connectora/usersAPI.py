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


@usersAPI.route("/get_user",  methods=["GET"])
@jwt_required()
def get_user():
    this_user = get_jwt_identity()
    logged_in_user = User.query.get(this_user["id"])
    if not logged_in_user:
        return jsonify({"error":"user not found"}), 401
    user_output = user_schema.dump(logged_in_user)
    return jsonify(user_output), 200