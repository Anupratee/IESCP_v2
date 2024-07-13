from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from connectora.models import db, User, users_schema, Influencer, influencers_schema, bcrypt
from connectora.models import Sponsor, sponsors_schema, Campaign, campaigns_schema, Ad, ads_schema, Category, categories_schema
from connectora.utils import DEFAULT_INFLUENCER_IMAGE, DEFAULT_SPONSOR_IMAGE


adsAPI = Blueprint("adsAPI", __name__)

@adsAPI.route("/ads", methods = ['GET'])
def get_all_ads():
    ads = Ad.query.all()
    ads_output = ads_schema.dump(ads)

    return jsonify({"ads": ads_output}), 200