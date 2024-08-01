from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from connectora.models import db, User, users_schema, Influencer, influencers_schema, bcrypt, Request, ad_schema
from connectora.models import Sponsor, sponsors_schema, Campaign, campaigns_schema, Ad, ads_schema, Category, categories_schema
from connectora.utils import DEFAULT_INFLUENCER_IMAGE, DEFAULT_SPONSOR_IMAGE


adsAPI = Blueprint("adsAPI", __name__)

@adsAPI.route("/ads", methods = ['GET'])
def get_all_ads():
    ads = db.session.query(Ad, Campaign, User).join(Campaign, Ad.campaign_id == Campaign.id).join(Sponsor, Campaign.sponsor_id == Sponsor.user_id).join(User, Sponsor.user_id == User.id).all()
    
    ad_list = []
    for ad, campaign, user in ads:
        ad_data = {
            'id': ad.id,
            'name': ad.name,
            'description': ad.description,
            'budget': ad.budget,
            'status': 'Completed' if ad.status else 'Incomplete',
            'campaign_name': campaign.name,
            'sponsor_name': user.name  
        }
        ad_list.append(ad_data)
        
    return jsonify({'ads': ad_list})


@adsAPI.route("/get_ads_by_campaign/<int:campaign_id>", methods=["GET"])
def get_ads_by_campaign(campaign_id):
    ads = db.session.query(Ad, Campaign, User).join(Campaign, Ad.campaign_id == Campaign.id).join(Sponsor, Campaign.sponsor_id == Sponsor.user_id).join(User, Sponsor.user_id == User.id).filter(Ad.campaign_id == campaign_id).all()
    
    ads_output = []
    for ad, campaign, user in ads:
        ad_output = {
            'id': ad.id,
            'campaign_id': ad.campaign_id,
            'name': ad.name,
            'description': ad.description,
            'budget': ad.budget,
            'status': 'Completed' if ad.status else 'Incomplete',
            'campaign_name': campaign.name,
            'sponsor_name': user.name
        }
        ads_output.append(ad_output)
    
    return jsonify({"ads": ads_output}), 200


@adsAPI.route("/get_ad_by_id/<int:ad_id>", methods=["GET"])
def get_ad_by_id(ad_id):
    ad = db.session.query(Ad, Campaign, User).join(Campaign, Ad.campaign_id == Campaign.id).join(Sponsor, Campaign.sponsor_id == Sponsor.user_id).join(User, Sponsor.user_id == User.id).filter(Ad.id == ad_id).first()
    
    if ad:
        ad_data, campaign, user = ad
        ad_output = {
            'id': ad_data.id,
            'campaign_id': ad_data.campaign_id,
            'name': ad_data.name,
            'description': ad_data.description,
            'budget': ad_data.budget,
            'status': 'Completed' if ad_data.status else 'Incomplete',
            'campaign_name': campaign.name,
            'sponsor_name': user.name
        }
        return jsonify({"ad": ad_output}), 200
    return jsonify({"error": "Ad not found"}), 404


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
        
    