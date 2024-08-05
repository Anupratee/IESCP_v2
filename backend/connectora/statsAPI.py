from flask import Blueprint, request, jsonify, send_file, Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from connectora.models import db, User, user_schema, users_schema, Influencer, influencers_schema, bcrypt, Request
from connectora.models import Sponsor, sponsors_schema, Campaign, campaigns_schema, Ad, ads_schema, Category, categories_schema
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import pandas as pd

statsAPI = Blueprint("statsAPI", __name__)

@statsAPI.route("/total_stats", methods=["GET"])
def get_total_stats():
    total_users = User.query.count()-1
    total_sponsors = Sponsor.query.count()
    total_influencers = Influencer.query.count()
    total_campaigns = Campaign.query.count()
    total_ads = Ad.query.count()
    total_requests = Request.query.count()

    total_stats = {
        "total_users": total_users,
        "total_sponsors": total_sponsors,
        "total_influencers": total_influencers,
        "total_campaigns": total_campaigns,
        "total_ads": total_ads,
        "total_requests": total_requests
    }
    return jsonify(total_stats), 200


@statsAPI.route('/pie_chart/sponsors_influencers')
def chart_sponsors_influencers():
    try:
        sponsor_count = Sponsor.query.count()
        influencer_count = Influencer.query.count()

        # Handle the case where there are no sponsors or influencers
        if sponsor_count == 0 and influencer_count == 0:
            return jsonify({"message": "No data available to generate chart."}), 204

        labels = ['Sponsors', 'Influencers']
        sizes = [sponsor_count, influencer_count]
        colors = ['#ff9999', '#66b3ff']

        # Create pie chart
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                startangle=140, textprops={'fontsize': 14})
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

        # Save pie chart to a BytesIO object
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        # Return image as response
        return send_file(img, mimetype='image/png')

    except Exception as e:
        return jsonify({"error": str(e)}), 500
