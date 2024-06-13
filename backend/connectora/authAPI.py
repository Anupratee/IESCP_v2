from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from connectora.models import User, user_schema, users_schema, Influencer, influencers_schema, Sponsor, sponsors_schema, Campaign, campaigns_schema, Ad, ads_schema, Category, categories_schema

authAPI = Blueprint("authAPI", __name__)

@authAPI.route("/", methods = ["GET"])
def login():
    return "hello"

@authAPI.route("/users", methods = ['GET'])
def get_all_users():
    users = User.query.all()
    users_output = users_schema.dump(users)

    return jsonify({"users": users_output}), 200

@authAPI.route("/influencers", methods = ['GET'])
def get_all_influencers():
    influencers = Influencer.query.all()
    influencers_output = influencers_schema.dump(influencers)

    return jsonify({"influencers": influencers_output}), 200

@authAPI.route("/sponsors", methods = ['GET'])
def get_all_sponsors():
    sponsors = Sponsor.query.all()
    sponsors_output = sponsors_schema.dump(sponsors)

    return jsonify({"sponsors": sponsors_output}), 200

@authAPI.route("/campaigns", methods = ['GET'])
def get_all_campaigns():
    campaigns = Campaign.query.all()
    campaigns_output = campaigns_schema.dump(campaigns)

    return jsonify({"campaigns": campaigns_output}), 200

@authAPI.route("/ads", methods = ['GET'])
def get_all_ads():
    ads = Ad.query.all()
    ads_output = ads_schema.dump(ads)

    return jsonify({"ads": ads_output}), 200

@authAPI.route("/categories", methods = ['GET'])
def get_all_categories():
    categories = Category.query.all()
    categories_output = categories_schema.dump(categories)

    return jsonify({"categories": categories_output}), 200
