from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from connectora.models import db, User, users_schema, Influencer, influencers_schema, bcrypt
from connectora.models import Sponsor, sponsors_schema, Campaign, campaigns_schema, Ad, ads_schema, Category, categories_schema
from connectora.utils import DEFAULT_INFLUENCER_IMAGE, DEFAULT_SPONSOR_IMAGE


sponsorsAPI = Blueprint("sponsorsAPI", __name__)

@sponsorsAPI.route("/sponsors", methods = ['GET'])
def get_all_sponsors():
    sponsors = Sponsor.query.all()
    sponsors_output = sponsors_schema.dump(sponsors)

    return jsonify({"sponsors": sponsors_output}), 200