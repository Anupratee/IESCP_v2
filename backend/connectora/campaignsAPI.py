from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from datetime import datetime
from connectora.models import db, User, user_schema, users_schema, Influencer, influencers_schema, bcrypt
from connectora.models import Sponsor, sponsors_schema, Campaign, campaigns_schema, Ad, ads_schema, Category, categories_schema
from connectora.utils import DEFAULT_CAMPAIGN_IMAGE, API_KEY, API_SECRET, CLOUD_NAME

campaignsAPI = Blueprint("campaignsAPI", __name__)

@campaignsAPI.route("/campaigns", methods = ['GET'])
def get_all_campaigns():
    campaigns = Campaign.query.all()
    campaigns_output = campaigns_schema.dump(campaigns)

    return jsonify({"campaigns": campaigns_output}), 200


@campaignsAPI.route("/create_campaign", methods=["POST"])
@jwt_required()
def create_campaign():
    this_user = get_jwt_identity()
    user = User.query.get(this_user["id"])

    if user.role != "sponsor":
        return jsonify({"error":"Only sponsors can make campaigns"}), 400
    
    sponsor_id = user.id

    category_name = request.form.get("category_name")
    if not category_name:
        category_id = 1
    else:
        category = Category.query.filter_by(name = category_name).first()
        if not category:
            return jsonify({"error":"Category doesn't exist"}), 400
    
        category_id = category.id

    name = request.form.get("name")
    description = request.form.get("description")
    status = False
    
    image = None

    if "image" in request.files:
        image = request.files["image"]
        if image:
            if not image.filename.endswith(('.jpg', '.jpeg', '.png')):
                return jsonify({'error':'Playlist image must be an image file'}), 400
            uploaded_image = cloudinary.uploader.upload(image, 
                                                        api_key = API_KEY, 
                                                        api_secret = API_SECRET, 
                                                        cloud_name = CLOUD_NAME)
            image_url = uploaded_image['secure_url']
    else:
        image_url = DEFAULT_CAMPAIGN_IMAGE

    if not name:
        return jsonify({'error':'Required fields can\'t be empty!'}), 400
        
    new_campaign = Campaign(sponsor_id=sponsor_id,
                            category_id=category_id,
                            name=name,
                            description=description,
                            status=status,
                            image=image_url)
        
    try:
        db.session.add(new_campaign)
        db.session.commit()
        return jsonify({"message":"Campaign created successfully"}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':f'{str(e)}.'}), 409


@campaignsAPI.route("/update_campaign/<int:campaign_id>", methods=["POST"])
@jwt_required()
def update_campaign(campaign_id):
    this_user = get_jwt_identity()
    user = User.query.get(this_user["id"])
