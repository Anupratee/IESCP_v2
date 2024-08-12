from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from models import db, User, users_schema, Influencer, influencers_schema, bcrypt, Request, influencer_ads_association
from models import Sponsor, sponsors_schema, Campaign, campaigns_schema, Ad, ads_schema, Category, categories_schema
from utils import DEFAULT_INFLUENCER_IMAGE, DEFAULT_SPONSOR_IMAGE
import task as task
from task import generate_csv


adrequestsAPI = Blueprint("adrequestsAPI", __name__)


#TEST
@adrequestsAPI.route("/meow")
def meow():
    # csv_data = generate_csv()
    # return Response(csv_data, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=meow.csv"}
    return "helo"


@adrequestsAPI.route("/influencer_ad_requests", methods=["GET"])
@jwt_required()
def influencer_ad_requests():
    this_user = get_jwt_identity()
    user = User.query.get(this_user["id"])

    if user.role != "influencer":
        return jsonify({"error": "Only influencers can access this resource"}), 400

    requests = db.session.query(
        Request,
        Ad.name.label('ad_name'),
        Ad.description.label('ad_description'),
        Ad.status.label('ad_status'),
        Campaign.name.label('campaign_name'),
        User.name.label('sponsor_name')
    ).join(Ad, Request.ad_id == Ad.id
    ).join(Campaign, Ad.campaign_id == Campaign.id
    ).join(Sponsor, Request.sponsor_id == Sponsor.user_id
    ).join(User, Sponsor.user_id == User.id
    ).filter(Request.influencer_id == user.id 
    ).all()
    
    request_list = []
    for req, ad_name, ad_description, ad_status, campaign_name, sponsor_name in requests:
        request_data = {
            "id": req.id,
            "ad_name": ad_name,
            "ad_description": ad_description,
            "payment_amount": req.payment_amount,
            'ad_status': 'Completed' if ad_status else 'Incomplete',
            "campaign_name": campaign_name,
            "sponsor_name": sponsor_name,
            "from_who": req.from_who,
        }
        request_list.append(request_data)
    
    return jsonify({"requests": request_list}), 200


@adrequestsAPI.route("/sponsor_ad_requests", methods=["GET"])
@jwt_required()
def sponsor_ad_requests():
    this_user = get_jwt_identity()
    user = User.query.get(this_user["id"])

    if user.role != "sponsor":
        return jsonify({"error": "Only sponsors can access this resource"}), 400

    requests = db.session.query(
        Request,
        Ad.name.label('ad_name'),
        Ad.description.label('ad_description'),
        Ad.status.label('ad_status'),
        Campaign.name.label('campaign_name'),
        User.id.label('influencer_id'),
        User.name.label('influencer_name'),
        User.email.label('influencer_email'),
        User.image.label('influencer_image'),
        User.description.label('influencer_description'),
        User.location.label('influencer_location'),
        User.flag.label('influencer_flag'),
        Influencer.followers.label('influencer_followers'),
        Influencer.platforms.label('influencer_platforms')
    ).join(Ad, Request.ad_id == Ad.id
    ).join(Campaign, Ad.campaign_id == Campaign.id
    ).join(Influencer, Request.influencer_id == Influencer.user_id
    ).join(User, Influencer.user_id == User.id
    ).filter(Request.sponsor_id == user.id
    ).all()
    
    request_list = []
    for req, ad_name, ad_description, ad_status, campaign_name, influencer_id, influencer_name, influencer_email, influencer_image, influencer_description, influencer_location, influencer_flag, influencer_followers, influencer_platforms in requests:
        request_data = {
            "id": req.id,
            "ad_name": ad_name,
            "ad_description": ad_description,
            "payment_amount": req.payment_amount,
            'ad_status': 'Completed' if ad_status else 'Incomplete',
            "campaign_name": campaign_name,
            "influencer_id": influencer_id,
            "influencer_name": influencer_name,
            "influencer_email": influencer_email,
            "influencer_image": influencer_image,
            "influencer_description": influencer_description,
            "influencer_location": influencer_location,
            "influencer_flag": influencer_flag,
            "influencer_followers": influencer_followers,
            "influencer_platforms": influencer_platforms,
            "from_who": req.from_who,
        }
        request_list.append(request_data)
    
    return jsonify({"requests": request_list}), 200



@adrequestsAPI.route("sponsor_create_request/<int:ad_id>/<int:influencer_id>", methods=["POST"])
@jwt_required()
def sponsor_create_request(ad_id, influencer_id):
    this_user = get_jwt_identity()
    user = User.query.get(this_user["id"])

    if user.role != "sponsor":
        return jsonify({"error":"You must be a sponsor to send this request"}), 400

    from_who = "sponsor"
    influencer_id = influencer_id
    ad_id = ad_id
    sponsor_id = user.id
    payment_amount = request.form.get("payment_amount")

    if not payment_amount:
        return jsonify({"error":"Required fields can't be empty"}), 400
    
    existing_request = Request.query.filter_by(influencer_id=influencer_id, ad_id=ad_id).first()
    if existing_request:
        return jsonify({"error": "You have already sent this influencer a request for this ad"}), 400
    
    existing_association = db.session.query(influencer_ads_association).filter_by(influencer_id=influencer_id, ad_id=ad_id).first()
    if existing_association:
        return jsonify({"error": "Influencer already associated with this ad"}), 400

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
    


@adrequestsAPI.route("/create_request/<int:ad_id>", methods=["POST"])
@jwt_required()
def create_request(ad_id):
    this_user = get_jwt_identity()
    user = User.query.get(this_user["id"])

    if user.role != "influencer":
        return jsonify({"error":"You must be an influencer to send this request"}), 400

    from_who = "influencer"

    influencer_id = user.id
    ad_id = ad_id

    ad = Ad.query.get(ad_id)
    campaign_id = ad.campaign_id
    campaign = Campaign.query.get(campaign_id)
    sponsor_id = campaign.sponsor_id
    payment_amount = request.form.get("payment_amount")

    if not payment_amount:
        return jsonify({"error":"Required fields can't be empty"}), 400
    
    existing_request = Request.query.filter_by(influencer_id=influencer_id, ad_id=ad_id).first()
    if existing_request:
        return jsonify({"error": "You have already sent a request for this ad"}), 400
    
    existing_association = db.session.query(influencer_ads_association).filter_by(influencer_id=influencer_id, ad_id=ad_id).first()
    if existing_association:
        return jsonify({"error": "You are already associated with this ad"}), 400

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
    

@adrequestsAPI.route("/accept_request/<int:request_id>", methods=["POST"])
@jwt_required()
def accept_request(request_id):
    this_user = get_jwt_identity()
    user = User.query.get(this_user["id"])

    request = Request.query.get(request_id)
    influencer_id = request.influencer_id
    ad_id = request.ad_id
    ad = Ad.query.get(ad_id)
    campaign_id = ad.campaign_id
    campaign = Campaign.query.get(campaign_id)
    sponsor_id = campaign.sponsor_id

    if user.role == "influencer":
        if user.id != influencer_id:
            return jsonify({"error":"unauthorized access"}), 401
    
    if user.role == "sponsor":
        if user.id != sponsor_id:
            return jsonify({"error":"unauthorized access"}), 401

    if user.role == "influencer" and request.from_who == "influencer":
        return jsonify({"error":"You can't accept your own request"}), 400
    
    if user.role == "sponsor" and request.from_who == "sponsor":
        return jsonify({"error":"You can't accept your own request"}), 400
    
    try:
        new_association = influencer_ads_association.insert().values(
            influencer_id=request.influencer_id,
            ad_id=request.ad_id,
            payment_amount=request.payment_amount
        )

        db.session.execute(new_association)
        db.session.delete(request)
        db.session.commit()
        
        return jsonify({"message": "Request accepted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':f'{str(e)}.'}), 409


@adrequestsAPI.route("/reject_request/<int:request_id>", methods=["DELETE"])
@jwt_required()
def reject_request(request_id):
    this_user = get_jwt_identity()
    user = User.query.get(this_user["id"])

    request = Request.query.get(request_id)
    influencer_id = request.influencer_id
    ad_id = request.ad_id
    ad = Ad.query.get(ad_id)
    campaign_id = ad.campaign_id
    campaign = Campaign.query.get(campaign_id)
    sponsor_id = campaign.sponsor_id

    if user.role == "influencer":
        if user.id != influencer_id:
            return jsonify({"error":"Unauthorized access"}), 401
    
    if user.role == "sponsor":
        if user.id != sponsor_id:
            return jsonify({"error":"Unauthorized access"}), 401
    
    try:
        db.session.delete(request)
        db.session.commit()
        return jsonify({"message":"Request deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':f'{str(e)}.'}), 409
    

@adrequestsAPI.route("/update_request/<int:request_id>", methods=["PUT"])
@jwt_required()
def update_request(request_id):
    this_user = get_jwt_identity()
    user = User.query.get(this_user["id"])

    ad_request = Request.query.get(request_id)
    influencer_id = ad_request.influencer_id
    ad_id = ad_request.ad_id
    ad = Ad.query.get(ad_id)
    campaign_id = ad.campaign_id
    campaign = Campaign.query.get(campaign_id)
    sponsor_id = campaign.sponsor_id

    if user.role == "influencer":
        if user.id != influencer_id:
            return jsonify({"error":"Unauthorized access"}), 401
    
    if user.role == "sponsor":
        if user.id != sponsor_id:
            return jsonify({"error":"Unauthorized access"}), 401
        
    payment_amount = request.form.get("payment_amount")
    
    if user.role == "influencer" and ad_request.from_who == "influencer":
        ad_request.from_who = "influencer"
        ad_request.payment_amount = payment_amount

        try: 
            db.session.commit()
            return jsonify({"message":"Request updated successfully!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error':f'{str(e)}.'}), 409
    
    if user.role == "sponsor" and ad_request.from_who == "sponsor":
        ad_request.from_who = "sponsor"
        ad_request.payment_amount = payment_amount

        try: 
            db.session.commit()
            return jsonify({"message":"Request updated successfully!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error':f'{str(e)}.'}), 409
        
    if user.role == "sponsor" and ad_request.from_who == "influencer":
        ad_request.from_who = "sponsor"
        ad_request.payment_amount = payment_amount

        try: 
            db.session.commit()
            return jsonify({"message":"Request updated successfully!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error':f'{str(e)}.'}), 409
        
    if user.role == "influencer" and ad_request.from_who == "sponsor":
        ad_request.from_who = "influencer"
        ad_request.payment_amount = payment_amount

        try: 
            db.session.commit()
            return jsonify({"message":"Request updated successfully!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error':f'{str(e)}.'}), 409
        








    