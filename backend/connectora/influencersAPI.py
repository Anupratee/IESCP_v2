from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from connectora.models import db, User, user_schema, users_schema, Influencer, influencers_schema, bcrypt
from connectora.models import Sponsor, sponsors_schema, Campaign, campaigns_schema, Ad, ads_schema, Category, categories_schema

influencersAPI = Blueprint("influencersAPI", __name__)

@influencersAPI.route("/influencers", methods = ['GET'])
def get_all_influencers():
    influencers = Influencer.query.all()
    influencers_output = influencers_schema.dump(influencers)

    return jsonify({"influencers": influencers_output}), 200