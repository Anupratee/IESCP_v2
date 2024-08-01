from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from connectora.models import db, User, user_schema, users_schema, Influencer, influencers_schema, bcrypt
from connectora.models import Sponsor, sponsors_schema, Campaign, campaigns_schema, Ad, ads_schema, Category, categories_schema

statsAPI = Blueprint("statsAPI", __name__)

@statsAPI.route("/total_stats", methods=["GET"])
def get_total_stats():
    total_users=User.query.count()-1
    total_campaigns=Campaign.query.count()
    total_ads=Ad.query.count()

    total_stats = {
        "total_users": total_users,
        "total_campaigns": total_campaigns,
        "total_ads": total_ads
    }
    return jsonify(total_stats), 200