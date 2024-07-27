from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from connectora.models import db, User, users_schema, Influencer, influencers_schema, bcrypt, Request
from connectora.models import Sponsor, sponsors_schema, Campaign, campaigns_schema, Ad, ads_schema, Category, categories_schema
from connectora.utils import DEFAULT_INFLUENCER_IMAGE, DEFAULT_SPONSOR_IMAGE


adrequestsAPI = Blueprint("adrequestsAPI", __name__)


@adrequestsAPI.route("/influencer_request/<int:ad_id>", methods=["POST"])
@jwt_required()
def influencer_request(ad_id):
    this_user = get_jwt_identity()
    user = User.query.get(this_user["id"])

    if user.role != "influencer":
        return jsonify({"error":"Only influencers can make this request"}), 400
    
    influencer_id = user.id
    ad_id = ad_id

    ad = Ad.query.get(ad_id)
    campaign_id = ad.campaign_id
    campaign = Campaign.query.get(campaign_id)
    sponsor_id = campaign.sponsor_id

    from_who = "influencer"
    payment_amount = request.form.get("payment_amount")

    if not payment_amount:
        return jsonify({"error":"Required fields can't be empty"}), 400

    new_request = Request(influencer_id=influencer_id,
                          sponsor_id=sponsor_id,
                          ad_id=ad_id,
                          from_who=from_who,
                          payment_amount=payment_amount)
    
    try:
        db.session.add(new_request)
        db.session.commit()
        return jsonify({"message":"Request created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':f'{str(e)}.'}), 409
    