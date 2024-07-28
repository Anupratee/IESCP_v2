from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from connectora.models import db, User, users_schema, Influencer, influencers_schema, bcrypt, Request, ad_schema
from connectora.models import Sponsor, sponsors_schema, Campaign, campaigns_schema, Ad, ads_schema, Category, categories_schema
from connectora.utils import DEFAULT_INFLUENCER_IMAGE, DEFAULT_SPONSOR_IMAGE


adsAPI = Blueprint("adsAPI", __name__)

@adsAPI.route("/ads", methods = ['GET'])
def get_all_ads():
    ads = Ad.query.all()
    ads_output = ads_schema.dump(ads)

    return jsonify({"ads": ads_output}), 200


@adsAPI.route("/get_ads_by_campaign/<int:campaign_id>", methods=["GET"])
def get_ads_by_campaign(campaign_id):
    ads = Ad.query.filter_by(campaign_id=campaign_id).all()
    ads_output = ads_schema.dump(ads)

    return jsonify({"ads": ads_output}), 200


@adsAPI.route("/get_ad_by_id/<int:ad_id>", methods=["GET"])
def get_ad_by_id(ad_id):
    ad = Ad.query.get(ad_id)
    ad_output = ad_schema.dump(ad)

    return jsonify({"ad":ad_output}), 200


@adsAPI.route("/create_ad/<int:campaign_id>", methods=["POST"])
@jwt_required()
def create_ad(campaign_id):
    this_user = get_jwt_identity()
    user = User.query.get(this_user["id"])

    if user.role != "sponsor":
        return jsonify({"error":"Only sponsors can make ads"}), 400
    
    sponsor_id = user.id

    sponsor = Sponsor.query.get(sponsor_id)

    if not sponsor.is_approved:
        return jsonify({"error":"You need to be approved to create this resource"}), 403
    
    name = request.form.get("name")
    description = request.form.get("description")
    budget = request.form.get("budget")
    status = False
    
    if not name:
        return jsonify({"error":"Required fields can't be empty"}), 400
    
    new_ad = Ad(campaign_id=campaign_id,
                name=name,
                description=description,
                budget=budget,
                status=status)
    
    try:
        db.session.add(new_ad)
        db.session.commit()
        return jsonify({"message":"Ad created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':f'{str(e)}.'}), 409


@adsAPI.route("/update_ad/<int:ad_id>", methods=["PUT"])
@jwt_required()
def update_ad(ad_id):
    this_user = get_jwt_identity()
    user = User.query.get(this_user["id"])

    ad = Ad.query.get(ad_id)

    if not ad:
        return jsonify({'error':'Ad doesn\'t exist'}), 404
    
    campaign = Campaign.query.get(ad.campaign_id)

    if campaign.sponsor_id != user.id:
        return jsonify({'error':'Unauthorized. You can\'t update an Ad you don\'t own.'}), 403
    
    update_name = request.form.get("update_name")
    update_description = request.form.get("update_description")
    update_budget = request.form.get("update_budget")
    update_status = request.form.get("update_status")

    if update_status:
        if update_status == "true" or update_status == "True":
            update_status = True
        else:
            update_status = False

    if not update_name:
        return jsonify({'error':'Required fields can\'t be empty!'}), 400
    
    ad.name = update_name
    ad.description = update_description
    ad.budget = update_budget
    ad.status = update_status

    try:
        db.session.commit()
        return jsonify({"message":"Ad updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':f'{str(e)}.'}), 409

    
@adsAPI.route("/delete_ad/<int:ad_id>", methods=["DELETE"])
@jwt_required()
def delete_ad(ad_id):
    this_user = get_jwt_identity()
    user = User.query.get(this_user["id"])

    ad = Ad.query.get(ad_id)

    if not ad:
        return jsonify({'error':'Ad doesn\'t exist'}), 404
    
    campaign = Campaign.query.get(ad.campaign_id)

    if campaign.sponsor_id != user.id:
        return jsonify({'error':'Unauthorized. You can\'t delete an Ad you don\'t own.'}), 403
    
    requests = Request.query.filter_by(ad_id=ad_id).all()

    for influencer in ad.influencers:
            ad.influencers.remove(influencer)

    try:
        for request in requests:
            db.session.delete(request)
        db.session.delete(ad)
        db.session.commit()
        return jsonify({"message":"Ad deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':f'{str(e)}.'}), 409
        
    